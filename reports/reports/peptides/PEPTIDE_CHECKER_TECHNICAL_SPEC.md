# Peptide Checker: Technical Architecture Specification

**Version:** 1.0
**Date:** 2026-03-24
**Author:** Reuben Bowlby / HUMMBL
**Classification:** Build Specification -- Ready for Implementation
**Based on:** PEPTIDE_CHECKER_BUSINESS_PLAN.md, DECISION_MATRIX_WHAT_TO_BUILD.md, consumer_health_tech_regulation_2026.md, PEPTIDE_PARTNERSHIP_STRATEGY.md, peptide_db.py, consumer_guide.md

---

## 1. Tech Stack Decision

### Recommendation: Next.js + Python FastAPI + SQLite + Vercel

| Layer | Choice | Rationale |
|-------|--------|-----------|
| **Frontend** | Next.js 14 (App Router) + Tailwind CSS | SSR/SSG for SEO (critical for organic traffic strategy); file-based routing; React ecosystem for future interactivity; Tailwind ships fast with no design system overhead |
| **Backend API** | Python FastAPI | Existing peptide_db.py is Python; FastAPI auto-generates OpenAPI docs; async performance; familiar stack for a solo Python developer |
| **Database** | SQLite (via `better-sqlite3` or `sqlite3`) on disk, migrating to Turso (hosted SQLite) for production | Zero config; no server to manage; existing JSON data migrates trivially; Turso provides hosted SQLite with edge replication when you need it |
| **Hosting** | Vercel (frontend) + Railway or Render (FastAPI backend) | Vercel has the best Next.js DX and free tier; Railway/Render deploy Python containers with zero config; total cost <$10/month at MVP scale |
| **File Storage** | Cloudflare R2 (for COA uploads) | S3-compatible, no egress fees, generous free tier (10 GB storage, 10M reads/month) |
| **Auth** | NextAuth.js (v5) with email magic links | No password management; free; built into Next.js; add OAuth providers later |
| **Payments** | Stripe (Phase 2, not MVP) | Industry standard; skip until subscription features launch |

### Why NOT the Alternatives

| Rejected | Reason |
|----------|--------|
| **Astro** | Better for pure static sites; Peptide Checker needs interactivity (search, filters, COA upload, storage calculator). Astro's island architecture adds complexity for these features. |
| **Plain HTML/Tailwind** | Ships fastest for page 1, but search/filtering/calculator features require JS anyway. Rebuilding what Next.js provides for free is wasted effort. |
| **Node.js backend** | Viable, but existing peptide_db.py and data pipeline logic is Python. Rewriting in Node is unnecessary work. |
| **PostgreSQL** | Overkill at launch. SQLite handles the data volume (hundreds of vendors, not millions of rows). Migrate when you hit edge cases SQLite cannot handle. |
| **Supabase** | Adds a dependency and abstraction layer over PostgreSQL. Direct SQLite is simpler and cheaper. Supabase auth is nice but NextAuth.js covers it. |
| **Cloudflare Workers/D1** | D1 is SQLite-compatible but still in beta. Workers runtime has limitations (no native Python, cold starts). The business plan mentioned Cloudflare, but Vercel + Railway is more mature and debuggable for a solo founder. |
| **Self-hosted** | Ops burden. You are one person. Let Vercel and Railway handle uptime. |

### Architecture Diagram

```
                          ┌─────────────────────┐
                          │   Vercel (Frontend)  │
                          │   Next.js 14 + TW    │
                          │   SSR/SSG pages       │
                          │   NextAuth.js         │
                          └──────────┬────────────┘
                                     │ HTTPS
                                     ▼
                          ┌─────────────────────┐
                          │  Railway (Backend)   │
                          │  Python FastAPI       │
                          │  SQLite (Turso)       │
                          └──────────┬────────────┘
                                     │
                          ┌──────────┴────────────┐
                          │                       │
                   ┌──────▼──────┐     ┌──────────▼──────────┐
                   │  Turso DB   │     │  Cloudflare R2      │
                   │  (SQLite)   │     │  (COA file storage)  │
                   └─────────────┘     └─────────────────────┘
```

---

## 2. Data Model

### 2.1 Database Tables

#### `peptides`

The canonical peptide reference table. One row per peptide compound.

```sql
CREATE TABLE peptides (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    name            TEXT NOT NULL UNIQUE,          -- "BPC-157", "Semaglutide"
    slug            TEXT NOT NULL UNIQUE,          -- "bpc-157", "semaglutide" (URL-safe)
    aliases         TEXT,                          -- JSON array: ["Bepecin","PL-10","PL-14736"]
    cas_number      TEXT,                          -- CAS Registry Number
    chembl_id       TEXT,                          -- "CHEMBL4297358"
    molecular_formula TEXT,                        -- "C62H98N16O22"
    molecular_weight REAL,                         -- 1419.56
    amino_acid_count INTEGER,                      -- 15
    sequence         TEXT,                         -- amino acid sequence if known
    category        TEXT NOT NULL,                 -- "research", "fda_approved", "compounded"
    description     TEXT,                          -- short plain-text description
    fda_status      TEXT NOT NULL DEFAULT 'not_approved',  -- "approved", "investigational", "not_approved"
    fda_category    TEXT,                          -- "category_1", "category_2", null
    wada_status     TEXT,                          -- "prohibited", "monitoring", "not_listed"
    wada_class      TEXT,                          -- WADA prohibition class
    max_clinical_phase INTEGER,                    -- 0-4
    evidence_tier   TEXT,                          -- "strong", "limited", "very_limited", "none"
    natural_product BOOLEAN DEFAULT FALSE,
    black_box_warning BOOLEAN DEFAULT FALSE,
    storage_lyophilized_days INTEGER,              -- shelf life lyophilized at recommended temp
    storage_reconstituted_days INTEGER,            -- shelf life reconstituted at 2-8C
    degradation_rate_per_day REAL,                 -- % potency loss per day at room temp (reconstituted)
    freeze_thaw_loss_percent REAL,                 -- % loss per freeze-thaw cycle
    created_at      TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at      TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX idx_peptides_slug ON peptides(slug);
CREATE INDEX idx_peptides_category ON peptides(category);
CREATE INDEX idx_peptides_fda_status ON peptides(fda_status);
```

#### `vendors`

Vendor/supplier entities. One row per vendor.

```sql
CREATE TABLE vendors (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    name            TEXT NOT NULL UNIQUE,
    slug            TEXT NOT NULL UNIQUE,          -- URL-safe
    website         TEXT,
    country         TEXT,                          -- "US", "CN", "CZ"
    vendor_type     TEXT NOT NULL DEFAULT 'research',  -- "research", "compounding_503a", "compounding_503b", "manufacturer"
    is_active       BOOLEAN DEFAULT TRUE,          -- FALSE = shut down (e.g., Peptide Sciences)
    shutdown_date   TEXT,                          -- date vendor ceased operations
    shutdown_reason TEXT,
    notes           TEXT,
    created_at      TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at      TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX idx_vendors_slug ON vendors(slug);
CREATE INDEX idx_vendors_active ON vendors(is_active);
```

#### `test_results`

Individual test result records. This is the core data table -- every Finnrick rating, Janoshik test, JMIR data point, and community submission is one row.

```sql
CREATE TABLE test_results (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    peptide_id      INTEGER NOT NULL REFERENCES peptides(id),
    vendor_id       INTEGER NOT NULL REFERENCES vendors(id),
    batch_id        TEXT,                          -- lot/batch number if known
    test_date       TEXT,                          -- YYYY-MM-DD
    test_lab        TEXT,                          -- "Janoshik", "Finnrick/Krause", "JMIR Study"
    test_method     TEXT,                          -- "HPLC", "HPLC-MS", "LC-MS/MS", "UHPLC"
    purity_percent  REAL,                          -- 0-100
    identity_confirmed BOOLEAN,
    endotoxin_eu_per_mg REAL,
    heavy_metals_ppm REAL,
    sterility_pass  BOOLEAN,
    degradation_products TEXT,                     -- JSON array of detected degradation products
    contaminants    TEXT,                          -- JSON object of contaminant:amount pairs
    grade           TEXT CHECK(grade IN ('A','B','C','D','E','U')),
    score           REAL,                          -- 0-10 (Finnrick-style composite)
    coa_file_key    TEXT,                          -- R2 object key for uploaded COA document
    coa_url         TEXT,                          -- external URL to original COA
    source          TEXT NOT NULL,                 -- "finnrick", "janoshik", "jmir_study", "peptide_test", "community", "manual"
    source_url      TEXT,
    tentative       BOOLEAN DEFAULT FALSE,         -- TRUE if <5 samples from this source
    notes           TEXT,
    created_at      TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX idx_test_results_peptide ON test_results(peptide_id);
CREATE INDEX idx_test_results_vendor ON test_results(vendor_id);
CREATE INDEX idx_test_results_grade ON test_results(grade);
CREATE INDEX idx_test_results_source ON test_results(source);
CREATE INDEX idx_test_results_date ON test_results(test_date);
```

#### `vendor_ratings`

Aggregated vendor quality ratings per peptide. Materialized from `test_results` via a scheduled job or trigger. This is what the frontend queries for vendor rankings.

```sql
CREATE TABLE vendor_ratings (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    vendor_id       INTEGER NOT NULL REFERENCES vendors(id),
    peptide_id      INTEGER NOT NULL REFERENCES peptides(id),
    overall_grade   TEXT CHECK(overall_grade IN ('A','B','C','D','E','U')),
    score_avg       REAL,
    score_min       REAL,
    score_max       REAL,
    total_tests     INTEGER DEFAULT 0,
    sources_count   INTEGER DEFAULT 0,            -- number of distinct test sources
    last_test_date  TEXT,
    has_ms_confirmation BOOLEAN DEFAULT FALSE,
    has_endotoxin_data BOOLEAN DEFAULT FALSE,
    has_coa_on_file BOOLEAN DEFAULT FALSE,
    confidence      TEXT DEFAULT 'low',           -- "low" (<3 tests), "medium" (3-9), "high" (10+)
    updated_at      TEXT NOT NULL DEFAULT (datetime('now')),
    UNIQUE(vendor_id, peptide_id)
);

CREATE INDEX idx_vendor_ratings_grade ON vendor_ratings(overall_grade);
CREATE INDEX idx_vendor_ratings_peptide ON vendor_ratings(peptide_id);
```

#### `regulatory_status`

Tracks regulatory status changes over time for each peptide across jurisdictions.

```sql
CREATE TABLE regulatory_status (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    peptide_id      INTEGER NOT NULL REFERENCES peptides(id),
    jurisdiction    TEXT NOT NULL,                 -- "fda", "wada", "state_ny", "state_ca", etc.
    status          TEXT NOT NULL,                 -- "approved", "category_1", "category_2", "prohibited", "monitoring", "no_action"
    effective_date  TEXT,                          -- YYYY-MM-DD
    source_url      TEXT,                          -- link to Federal Register, FDA notice, etc.
    notes           TEXT,
    created_at      TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX idx_regulatory_peptide ON regulatory_status(peptide_id);
CREATE INDEX idx_regulatory_jurisdiction ON regulatory_status(jurisdiction);
```

#### `users` (MVP: minimal, for future freemium)

```sql
CREATE TABLE users (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    email           TEXT NOT NULL UNIQUE,
    name            TEXT,
    tier            TEXT NOT NULL DEFAULT 'free',  -- "free", "premium"
    stripe_customer_id TEXT,
    created_at      TEXT NOT NULL DEFAULT (datetime('now')),
    last_login      TEXT
);
```

#### `coa_uploads` (MVP: basic)

```sql
CREATE TABLE coa_uploads (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id         INTEGER REFERENCES users(id), -- NULL for anonymous uploads
    file_key        TEXT NOT NULL,                 -- R2 object key
    file_name       TEXT NOT NULL,
    file_size       INTEGER,
    mime_type       TEXT,
    vendor_claimed  TEXT,                          -- vendor name on the COA
    peptide_claimed TEXT,                          -- peptide name on the COA
    purity_claimed  REAL,                          -- purity % claimed on the COA
    red_flags       TEXT,                          -- JSON array of detected red flags
    red_flag_count  INTEGER DEFAULT 0,
    status          TEXT DEFAULT 'pending',        -- "pending", "analyzed", "verified", "suspicious"
    created_at      TEXT NOT NULL DEFAULT (datetime('now'))
);
```

### 2.2 Data Relationships

```
peptides 1──────∞ test_results ∞──────1 vendors
    │                                      │
    │                                      │
    └──── 1──∞ vendor_ratings ∞──1 ────────┘
    │
    └──── 1──∞ regulatory_status
```

---

## 3. API Design

### 3.1 Base URL and Versioning

```
Production: https://api.peptidechecker.com/v1
Development: http://localhost:8000/v1
```

### 3.2 Endpoints

#### Peptides

```
GET /v1/peptides
    Query params: ?category=research&fda_status=investigational&limit=20&offset=0
    Response: { peptides: [...], total: 19, limit: 20, offset: 0 }

GET /v1/peptides/{slug}
    Response: Full peptide object with current regulatory status and aggregate stats
    Example: GET /v1/peptides/bpc-157
```

**Example response for `GET /v1/peptides/bpc-157`:**

```json
{
  "id": 3,
  "name": "BPC-157",
  "slug": "bpc-157",
  "aliases": ["Bepecin", "PL-10", "PL-14736", "PLD-116"],
  "cas_number": null,
  "chembl_id": "CHEMBL4297358",
  "molecular_formula": "C62H98N16O22",
  "molecular_weight": 1419.56,
  "category": "research",
  "fda_status": "not_approved",
  "fda_category": "category_2",
  "wada_status": "prohibited",
  "max_clinical_phase": 2,
  "evidence_tier": "very_limited",
  "storage": {
    "lyophilized_days": 730,
    "reconstituted_days": 14,
    "degradation_rate_per_day": 2.5,
    "freeze_thaw_loss_percent": 3.0,
    "recommended_temp_c": "2-8"
  },
  "vendor_stats": {
    "total_vendors_tested": 68,
    "grade_distribution": { "A": 4, "B": 8, "C": 15, "D": 22, "E": 19 },
    "avg_purity": 87.3
  },
  "current_regulatory": [
    { "jurisdiction": "fda", "status": "category_2", "effective_date": "2024-06-03" },
    { "jurisdiction": "wada", "status": "prohibited", "effective_date": "2026-01-01" }
  ]
}
```

#### Vendors

```
GET /v1/vendors
    Query params: ?peptide=bpc-157&grade=A,B&sort=score_avg&order=desc&limit=20&offset=0
    Response: { vendors: [...], total: 68, limit: 20, offset: 0 }

GET /v1/vendors/{slug}
    Response: Vendor profile with all peptide ratings and test history

GET /v1/vendors/{slug}/tests
    Query params: ?peptide=bpc-157&source=finnrick&limit=50
    Response: { tests: [...], total: 7 }
```

**Example response for `GET /v1/vendors?peptide=bpc-157&grade=A&sort=score_avg&order=desc`:**

```json
{
  "vendors": [
    {
      "name": "Peptide Partners",
      "slug": "peptide-partners",
      "is_active": true,
      "rating": {
        "peptide": "BPC-157",
        "overall_grade": "A",
        "score_avg": 8.0,
        "score_min": 6.9,
        "score_max": 10.0,
        "total_tests": 7,
        "confidence": "medium",
        "has_ms_confirmation": false,
        "has_endotoxin_data": false,
        "last_test_date": "2026-01-15"
      }
    }
  ],
  "total": 4,
  "limit": 20,
  "offset": 0
}
```

#### Search

```
GET /v1/search
    Query params: ?q=bpc&type=all (searches peptides, vendors, and content)
    Response: { peptides: [...], vendors: [...], pages: [...] }
```

#### Regulatory Status

```
GET /v1/regulatory
    Response: All 19 Category 2 peptides with current status across jurisdictions

GET /v1/regulatory/{peptide_slug}
    Response: Full regulatory history for one peptide

GET /v1/regulatory/{peptide_slug}/timeline
    Response: Chronological timeline of status changes
```

**Example response for `GET /v1/regulatory/bpc-157`:**

```json
{
  "peptide": "BPC-157",
  "current_status": {
    "fda": "category_2",
    "wada": "prohibited",
    "kennedy_announcement": "returning_to_category_1",
    "formal_rule_published": false,
    "expected_rulemaking": "Q2-Q3 2026"
  },
  "history": [
    { "date": "2024-06-03", "jurisdiction": "fda", "action": "Moved to Category 2", "source_url": "..." },
    { "date": "2026-01-01", "jurisdiction": "wada", "action": "Added to 2026 Prohibited List", "source_url": "..." },
    { "date": "2026-02-27", "jurisdiction": "fda", "action": "Kennedy announces return to Category 1 (no formal rule)", "source_url": "..." }
  ],
  "disclaimer": "Regulatory status reflects formal published rules. Announcements without published Federal Register notices are noted but do not change formal legal status."
}
```

#### COA Verification

```
POST /v1/coa/upload
    Body: multipart/form-data (file, optional vendor_name, optional peptide_name)
    Auth: Optional (anonymous uploads allowed with rate limit)
    Response: { upload_id: "...", status: "pending" }

GET /v1/coa/{upload_id}
    Response: Analysis results with red flags
```

**Example response for `GET /v1/coa/abc123`:**

```json
{
  "upload_id": "abc123",
  "status": "analyzed",
  "vendor_claimed": "Example Peptides",
  "peptide_claimed": "BPC-157",
  "purity_claimed": 99.2,
  "red_flags": [
    {
      "code": "ROUND_PURITY",
      "severity": "medium",
      "message": "Purity of 99.2% is suspiciously close to 99%. Legitimate tests typically show non-round numbers like 97.3% or 98.6%."
    },
    {
      "code": "NO_CHROMATOGRAM",
      "severity": "high",
      "message": "No HPLC chromatogram image detected in the document. Legitimate COAs include the raw chromatogram."
    }
  ],
  "red_flag_count": 2,
  "database_comparison": {
    "vendor_in_database": true,
    "vendor_grade": "C",
    "vendor_avg_purity": 82.5,
    "claimed_vs_tested_delta": 16.7,
    "delta_flag": "Claimed purity is 16.7% higher than average tested purity for this vendor."
  }
}
```

#### Storage Calculator

```
POST /v1/tools/storage-calculator
    Body: {
        "peptide": "bpc-157",
        "reconstitution_date": "2026-03-20",
        "diluent": "bacteriostatic_water",
        "storage_temp_c": 4,
        "freeze_thaw_cycles": 2
    }
    Response: {
        "estimated_current_potency_percent": 88.5,
        "recommended_discard_date": "2026-04-03",
        "days_remaining": 10,
        "degradation_factors": [
            { "factor": "time_at_temp", "loss_percent": 6.0 },
            { "factor": "freeze_thaw", "loss_percent": 5.5 }
        ],
        "recommendation": "Use within 10 days. Store at 2-8°C. Avoid additional freeze-thaw cycles."
    }
```

### 3.3 Rate Limiting

| Tier | Limit | Scope |
|------|-------|-------|
| **Anonymous** | 30 requests/minute, 500/day | By IP |
| **Free authenticated** | 60 requests/minute, 2,000/day | By user |
| **Premium** | 300 requests/minute, 20,000/day | By user |

Implementation: Use `slowapi` (FastAPI rate limiter built on `limits` library). Store counters in SQLite or in-memory for MVP. Migrate to Redis if needed at scale.

Rate limit headers on every response:
```
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 54
X-RateLimit-Reset: 1711324800
```

### 3.4 Authentication

MVP uses API key-style tokens for programmatic access and session cookies for browser access:

- **Browser sessions:** NextAuth.js handles login via email magic link. Session cookie sent to FastAPI backend via `Authorization: Bearer <session_token>` header.
- **API keys:** Generated in user settings for programmatic access. Stored hashed in the `users` table.
- **Anonymous access:** All read endpoints (peptides, vendors, search, regulatory) are public. COA upload and storage calculator are public with stricter rate limits.
- **Premium gating (Phase 2):** Detailed vendor reports, unlimited COA analysis, alert subscriptions.

---

## 4. Core Features (MVP)

### 4.1 Vendor Database with Search and Filtering

**Pages:**
- `/vendors` -- Searchable, filterable vendor listing with grade badges
- `/vendors/[slug]` -- Individual vendor profile with all test results, grade history, peptide-by-peptide breakdown
- `/vendors?peptide=bpc-157&grade=A,B` -- Pre-filtered views linked from peptide pages

**UI components:**
- Search bar with typeahead (searches vendor name)
- Grade filter (checkboxes: A, B, C, D, E)
- Peptide filter (dropdown)
- Sort by: grade, score, test count, last test date
- Vendor cards showing: name, overall grade badge, score, test count, active/shutdown status, confidence indicator

**Data source:** `vendor_ratings` table, aggregated from `test_results`.

### 4.2 Vendor Quality Ratings (A-E Tier)

**Grading methodology (from Finnrick model, extended):**

| Grade | Score Range | Label | Color |
|-------|-----------|-------|-------|
| A | 8.0-10.0 | Excellent | Green |
| B | 6.0-7.9 | Good | Light green |
| C | 4.0-5.9 | Acceptable | Yellow |
| D | 2.0-3.9 | Poor | Orange |
| E | 0.0-1.9 | Failing | Red |
| U | -- | Untested | Gray |

**Confidence badges:** Display alongside grades to indicate data reliability.
- High confidence: 10+ tests from 2+ sources
- Medium confidence: 3-9 tests
- Low confidence: 1-2 tests (marked "tentative")

**Multi-source triangulation:** When data exists from multiple labs (Finnrick + Janoshik + community), display each source's rating separately alongside the composite. This addresses Finnrick's documented conflict-of-interest concerns by showing independent corroboration.

### 4.3 COA Verification Tool

**MVP scope: Rule-based red-flag detection (no ML).**

Red flags to check (from RQ-PEP-001 Section 8):

| # | Red Flag | Severity | Detection Method |
|---|----------|----------|-----------------|
| 1 | Purity exactly 99.0% or 99.9% (suspiciously round) | Medium | Regex on extracted text |
| 2 | No chromatogram image in document | High | Image detection in PDF |
| 3 | Missing lab name, address, or accreditation | High | Text pattern matching |
| 4 | Date format inconsistencies | Medium | Date parsing |
| 5 | Vendor name does not match a known lab format | Medium | Lookup against known lab templates |
| 6 | Claimed purity significantly above database average for that vendor | High | Cross-reference `vendor_ratings` |
| 7 | Document appears to be a template/form fill (no unique identifiers) | Medium | Structural analysis |
| 8 | Missing lot/batch number | Low | Text pattern matching |

**Implementation:** Accept PDF and image uploads. Use `PyMuPDF` (fitz) for PDF text extraction. Store files on R2. Run red-flag rules server-side. Return results as structured JSON.

Phase 2 upgrade path: Add OCR via `pytesseract` for image-only COAs, then ML classification for "legitimate vs. suspicious" scoring.

### 4.4 Peptide Regulatory Status Tracker

**Coverage: All 19 Category 2 peptides + semaglutide + tirzepatide.**

Category 2 peptides (per RQ-PEP-005):
BPC-157, Thymosin Alpha-1, AOD-9604, GHK-Cu, Thymosin Beta-4, Epithalon, Selank, Semax, DSIP, CJC-1295, Ipamorelin, Tesamorelin, Sermorelin, GHRP-2, GHRP-6, IGF-1 LR3, Mechano Growth Factor, Follistatin 344, PT-141

**Pages:**
- `/regulatory` -- Dashboard showing all tracked peptides with status badges
- `/regulatory/[slug]` -- Individual peptide regulatory timeline

**Status badges:**
- FDA Approved (green)
- Category 1 - Compoundable (blue)
- Category 2 - Restricted (orange)
- Announced for Reclassification - No Formal Rule (yellow, with tooltip explaining Kennedy announcement vs. published rule)
- WADA Prohibited (red)
- State Enforcement Active (red, with state list)

**Data maintenance:** Manual updates via admin interface. Regulatory changes are infrequent (weeks/months between updates). Automated scraping is Phase 2.

### 4.5 Storage Calculator

**Page:** `/tools/storage-calculator`

**Inputs:**
- Peptide (dropdown from database)
- Reconstitution date (date picker)
- Diluent (bacteriostatic water, sterile water, acetic acid)
- Storage temperature (2-8C refrigerator, room temp, frozen)
- Number of freeze-thaw cycles

**Outputs:**
- Estimated current potency (%)
- Days of useful life remaining
- Recommended discard date
- Visual degradation curve chart
- Storage tips specific to the peptide

**Degradation models (from RQ-PEP-004 data):**

| Peptide | Reconstituted Shelf Life (2-8C) | Room Temp Degradation/Day | Freeze-Thaw Loss/Cycle |
|---------|-------------------------------|--------------------------|----------------------|
| BPC-157 | 14 days | ~2.5% | 3-5% |
| TB-500 | 21 days | ~1.5% | 2-5% |
| Semaglutide | 56 days (per label) | ~0.5% | 1-2% |
| Ipamorelin | 14 days | ~2.0% | 2-4% |
| CJC-1295 | 14 days | ~2.0% | 2-4% |
| GHK-Cu | 21 days | ~1.0% | 1-3% |

Implementation: Pure frontend calculation using the degradation constants stored in the `peptides` table. No backend call needed for basic calculation.

### 4.6 Consumer Education Pages

**Convert existing content to web pages:**

| Source | Target Page | SEO Value |
|--------|------------|-----------|
| consumer_guide.md Section 1 (Semaglutide) | `/peptides/semaglutide` | High (165K+ monthly searches for GLP-1 terms) |
| consumer_guide.md Section 2 (Tirzepatide) | `/peptides/tirzepatide` | High |
| consumer_guide.md Section 3 (BPC-157) | `/peptides/bpc-157` | High (165K monthly for BPC-157) |
| consumer_guide.md Section 4 (Ipamorelin) | `/peptides/ipamorelin` | Medium |
| consumer_guide.md Section 5 (CJC-1295) | `/peptides/cjc-1295` | Medium |
| consumer_guide.md Section 11 (How to Evaluate) | `/guides/evaluating-peptide-claims` | High |
| RQ-PEP-001 | `/reports/bpc157-quality` | High |
| RQ-PEP-002 | `/reports/glp1-enforcement` | High |
| RQ-PEP-003 | `/reports/testing-methods` | Medium |
| RQ-PEP-004 | `/reports/stability-storage` | Medium |
| RQ-PEP-005 | `/reports/regulatory-landscape` | High |
| Cross-Reference Synthesis | `/reports/state-of-the-market-2026` | High |

Each peptide page includes:
- Regulatory status badge
- Evidence tier indicator
- Mechanism of action (plain language)
- Clinical trial summary with links to ClinicalTrials.gov
- Vendor quality summary (link to filtered vendor list)
- Storage recommendations
- Safety information
- Medical disclaimer (per Section 7)

---

## 5. Data Pipeline

### 5.1 Initial Data Import (peptide_db.py migration)

The existing `peptide_db.py` loads JSON files from `data/` directory. Migration script:

```python
# migrate_json_to_sqlite.py
"""
One-time migration: Read all JSON files from peptide_db.py data directory,
create peptide and vendor records, import test results into SQLite.
"""

import json
import sqlite3
import os
from pathlib import Path

DATA_DIR = Path("C:/Users/Owner/peptide-checker/data")
DB_PATH = "peptide_checker.db"

def migrate():
    conn = sqlite3.connect(DB_PATH)
    # 1. Create tables (run schema SQL above)
    # 2. Walk DATA_DIR, parse each JSON file
    # 3. For each entry:
    #    a. INSERT OR IGNORE into peptides (derive from peptide_name)
    #    b. INSERT OR IGNORE into vendors (derive from vendor field)
    #    c. INSERT into test_results (map all fields)
    # 4. Recompute vendor_ratings from test_results
    conn.close()
```

**Current data inventory:**
- `data/bpc157/finnrick_ratings.json` -- ~30 BPC-157 vendor ratings from Finnrick
- `data/semaglutide/finnrick_ratings.json` -- Semaglutide vendor ratings
- `data/semaglutide/jmir_study.json` -- JMIR study purity data
- `data/schema.json` -- JSON Schema definition (maps directly to `test_results` columns)

Migration is straightforward because the existing JSON schema maps 1:1 to the `test_results` table columns.

### 5.2 Finnrick Data Integration Strategy

**Phase 1 (MVP):** Manual import.
- Download Finnrick's public vendor ratings for all 15 peptides they cover
- Parse into the schema defined above
- Import via a Python script similar to the existing `cmd_add` in `peptide_db.py`
- Flag all Finnrick-sourced data with `source = "finnrick"` and note the conflict-of-interest concerns in the UI

**Phase 2:** API integration if Finnrick offers one, or automated scraping with their permission. The data partnership strategy from PEPTIDE_PARTNERSHIP_STRATEGY.md recommends a one-way data ingestion agreement, not endorsement of their methodology.

### 5.3 COA Document Parsing (PDF to Structured Data)

**MVP approach:**

1. Accept PDF or image upload via `/v1/coa/upload`
2. Store original file on Cloudflare R2
3. Extract text from PDF using `PyMuPDF` (fitz)
4. Run regex patterns to extract:
   - Lab name and address
   - Test date
   - Peptide name / identity
   - Purity percentage
   - Method (HPLC, LC-MS, etc.)
   - Lot/batch number
5. Run red-flag rules against extracted data
6. Cross-reference extracted vendor/purity against `vendor_ratings` table
7. Store structured results in `coa_uploads` table

**Phase 2 upgrade:** Add OCR (pytesseract) for image-only uploads. Add ML classification model trained on collected COA data.

### 5.4 Automated Regulatory Status Updates

**MVP:** Manual updates via admin interface. Regulatory changes happen infrequently (the Kennedy announcement was the first major change in months). A solo founder can track FDA Federal Register notices, WADA updates, and state AG actions manually.

**Phase 2:** Set up RSS/Atom feed monitors for:
- FDA Federal Register notices (peptide-related keywords)
- WADA Prohibited List updates (annual, January 1)
- State AG press releases (keyword alerts via Google Alerts)
- PCAC meeting announcements

Alerts trigger an admin notification; human reviews and updates the database.

---

## 6. SEO and Content Strategy

### 6.1 URL Structure

```
/                                           Homepage
/peptides                                   Peptide directory
/peptides/[slug]                            Individual peptide page (e.g., /peptides/bpc-157)
/vendors                                    Vendor directory
/vendors/[slug]                             Individual vendor profile
/vendors?peptide=[slug]&grade=A,B           Filtered vendor views
/regulatory                                 Regulatory status dashboard
/regulatory/[slug]                          Individual peptide regulatory timeline
/reports                                    Research reports index
/reports/[slug]                             Individual research report
/guides                                     Consumer guides index
/guides/[slug]                              Individual guide page
/tools/storage-calculator                   Storage calculator
/tools/coa-verification                     COA upload tool
/about                                      About / methodology / independence statement
/privacy                                    Privacy policy
/health-data-privacy                        MHMDA-compliant health data privacy policy
/terms                                      Terms of service
/disclaimer                                 Medical disclaimer
```

All dynamic pages use clean, keyword-rich slugs. No query parameters in canonical URLs (use Next.js `generateStaticParams` for SSG where possible).

### 6.2 Priority Pages for Organic Search Traffic

**Tier 1 (build first, highest search volume):**

| Page | Target Keywords | Monthly Search Volume (est.) |
|------|----------------|----------------------------|
| `/peptides/bpc-157` | "bpc-157", "bpc 157 review", "is bpc-157 safe" | 165,000+ |
| `/peptides/semaglutide` | "semaglutide", "ozempic alternative", "compounded semaglutide" | 500,000+ |
| `/peptides/tirzepatide` | "tirzepatide", "mounjaro", "zepbound" | 200,000+ |
| `/vendors?peptide=bpc-157` | "best bpc-157 vendor", "bpc-157 vendor review" | 10,000+ |
| `/reports/state-of-the-market-2026` | "peptide market 2026", "peptide vendor quality" | New term, brand-building |
| `/guides/evaluating-peptide-claims` | "how to verify peptide quality", "peptide coa" | 5,000+ |

**Tier 2 (build second, medium volume):**

| Page | Target Keywords |
|------|----------------|
| `/tools/storage-calculator` | "peptide storage", "bpc-157 shelf life", "reconstituted peptide stability" |
| `/regulatory` | "peptide legal status 2026", "fda peptide reclassification" |
| `/reports/bpc157-quality` | "bpc-157 testing results", "bpc-157 purity" |
| `/reports/glp1-enforcement` | "compounded semaglutide safety", "fda glp-1 warning" |
| `/peptides/ipamorelin` | "ipamorelin review", "ipamorelin safety" |
| `/peptides/cjc-1295` | "cjc-1295", "cjc-1295 ipamorelin" |

### 6.3 Publishing Research Reports as Web Content

Convert the 5 research reports + synthesis from Markdown to Next.js pages using MDX:

1. Install `@next/mdx` and `remark-gfm` for GitHub Flavored Markdown support
2. Place each report as a `.mdx` file in `app/reports/[slug]/page.mdx`
3. Add frontmatter with title, date, description, keywords
4. Add structured data (see 6.4)
5. Add table of contents sidebar for long reports
6. Add "last updated" date and data source citations
7. Add medical disclaimer banner at top and bottom of every report
8. Internal link between reports and relevant peptide/vendor pages

### 6.4 Schema.org Markup

Add JSON-LD structured data to every page:

**Peptide pages (`/peptides/[slug]`):**
```json
{
  "@context": "https://schema.org",
  "@type": "MedicalWebPage",
  "about": {
    "@type": "Drug",
    "name": "BPC-157",
    "alternateName": ["Bepecin", "PL-10"],
    "activeIngredient": "Pentadecapeptide BPC 157",
    "legalStatus": "Investigational"
  },
  "audience": {
    "@type": "MedicalAudience",
    "audienceType": "Consumer"
  },
  "lastReviewed": "2026-03-24",
  "medicalDisclaimer": "This content is for informational purposes only and does not constitute medical advice."
}
```

**Report pages (`/reports/[slug]`):**
```json
{
  "@context": "https://schema.org",
  "@type": "ScholarlyArticle",
  "headline": "BPC-157 Quality Testing Data Analysis 2026",
  "author": { "@type": "Organization", "name": "Peptide Checker" },
  "datePublished": "2026-03-24",
  "publisher": { "@type": "Organization", "name": "Peptide Checker" }
}
```

**Vendor pages (`/vendors/[slug]`):**
```json
{
  "@context": "https://schema.org",
  "@type": "Review",
  "itemReviewed": {
    "@type": "Organization",
    "name": "Vendor Name"
  },
  "reviewRating": {
    "@type": "Rating",
    "ratingValue": "8.0",
    "bestRating": "10",
    "worstRating": "0"
  },
  "author": { "@type": "Organization", "name": "Peptide Checker" }
}
```

Also add `WebSite` and `SearchAction` schema to the homepage for Google Sitelinks search box eligibility.

---

## 7. Compliance Implementation

### 7.1 Medical Disclaimer

**Placement:** Every page. Two implementations:

1. **Persistent site-wide banner** (top of every page, not dismissable):
   > "Peptide Checker provides product verification data and educational information. It does not provide medical advice, diagnosis, or treatment recommendations. Consult a qualified healthcare professional before using any peptide product."

2. **Per-page contextual disclaimer** (bottom of peptide pages, vendor pages, reports):
   > "The information on this page is for educational and informational purposes only. [Peptide name] has not been evaluated by the FDA for safety or efficacy unless otherwise noted. Test results reported here reflect laboratory analysis of products and do not constitute an endorsement or recommendation to purchase or use any product. Always consult a licensed healthcare provider."

### 7.2 Privacy Policy Requirements

**Two separate privacy policies required (per MHMDA compliance guidance):**

1. **General Privacy Policy** (`/privacy`):
   - What data is collected (email, IP, usage analytics)
   - How it is used (account management, service improvement)
   - Third-party services (Vercel analytics, Stripe for payments)
   - Data retention periods
   - User rights (access, deletion, correction)
   - Contact information

2. **Consumer Health Data Privacy Policy** (`/health-data-privacy`):
   - Specific to any health-related data: search queries for peptide names, COA uploads, storage calculator inputs
   - What health data is collected
   - Why it is collected (to provide the requested service -- not sold, not shared for advertising)
   - Opt-in consent mechanism before collecting health-adjacent data
   - How to request deletion
   - Third parties who may access this data (and why)

**Key implementation decisions:**
- Do NOT use Google Analytics on peptide/health pages (MHMDA risk). Use Vercel Analytics (privacy-friendly, no cookies) or Plausible/Fathom (EU-based, GDPR-compliant).
- Do NOT link search queries to user accounts unless the user explicitly opts in.
- Anonymize COA upload data by default (do not require login for basic upload).
- Implement data deletion endpoint: `DELETE /v1/users/me/data` that removes all user-linked data.

### 7.3 Terms of Service Essentials

`/terms` must include:

- Medical advice disclaimer (repeated from banner)
- "For educational and informational purposes only"
- Platform does not endorse, recommend, or encourage purchase or use of any product
- Limitation of liability (capped at fees paid, or $100 for free users)
- Indemnification clause
- Binding arbitration with class action waiver
- Choice of law: Delaware (or Wyoming, matching LLC formation)
- User acknowledgment that peptide regulatory status is evolving and may change
- User acknowledgment that test data reflects specific samples at specific times and may not represent current product quality
- Prohibited uses: no scraping, no republishing ratings as vendor endorsements
- **Affirmative acceptance required:** Checkbox consent at account creation, not browse-wrap

### 7.4 Cookie Consent

**MVP approach: Minimize cookies to avoid consent requirements.**

- NextAuth.js session cookie: Strictly necessary (exempt from consent under most frameworks)
- Vercel Analytics: Cookieless (no consent needed)
- No third-party advertising cookies
- No Google Analytics, Meta Pixel, or similar tracking pixels

If no non-essential cookies are set, no cookie banner is needed. This is the simplest compliant path.

If Stripe is added (Phase 2), Stripe sets its own cookies. At that point, add a simple cookie consent banner for payment-related pages only.

### 7.5 Editorial Guidelines for Content

**Hard rules (violations are publishing blockers):**

NEVER write:
- "[Peptide] treats/cures/prevents [condition]"
- "[Peptide] is effective for [use case]"
- "[Peptide] works for [symptom]"
- "Research proves [peptide] [health benefit]"
- Dosage recommendations
- Treatment protocols
- Before/after comparisons implying health outcomes

ALWAYS write:
- "Published research has examined [peptide] for [endpoint]"
- "This product was tested and found to contain [substance] at [concentration]"
- "The FDA has not approved [peptide] for human use"
- "The manufacturer claims [X]. Testing found [Y]."
- "Consult a healthcare professional before using any peptide product"

**Process:** Every piece of content reviewed against this checklist before publication. Document the review in a content log (demonstrates good faith if challenged by FTC).

---

## 8. Deployment Plan

### 8.1 CI/CD Pipeline

```
GitHub repo (monorepo)
├── /frontend          (Next.js app)
├── /backend           (FastAPI app)
├── /shared            (types, constants shared between front/back)
├── /scripts           (migration, data import, admin tools)
└── /data              (seed data JSON files, copied from peptide-checker)
```

**GitHub Actions workflows:**

1. **`ci.yml`** -- Runs on every push:
   - Lint (ESLint for frontend, ruff for backend)
   - Type check (TypeScript, mypy)
   - Unit tests (pytest for backend, vitest for frontend)
   - Build check (Next.js build, Docker build for backend)

2. **`deploy-frontend.yml`** -- Runs on push to `main`:
   - Vercel auto-deploys from GitHub (zero config)
   - Preview deployments on PRs

3. **`deploy-backend.yml`** -- Runs on push to `main`:
   - Build Docker image
   - Push to Railway (or Render) via their GitHub integration
   - Run database migrations

### 8.2 Domain and DNS Setup

1. Register `peptidechecker.com` (or `peptidechecker.org` if .com is taken)
2. DNS managed via Cloudflare (free tier):
   - `peptidechecker.com` -- A record to Vercel
   - `api.peptidechecker.com` -- CNAME to Railway
   - `www.peptidechecker.com` -- redirect to apex
3. Cloudflare proxy enabled for DDoS protection and CDN caching

### 8.3 SSL / Security

- Vercel provides automatic SSL for frontend
- Railway provides automatic SSL for backend
- Cloudflare provides edge SSL and origin certificates
- Enable HSTS header: `Strict-Transport-Security: max-age=31536000; includeSubDomains`
- CSP header to prevent XSS
- CORS: Allow `peptidechecker.com` origin only on API
- Rate limiting (Section 3.3)
- File upload size limit: 10 MB for COA uploads
- File type validation: Accept only PDF, PNG, JPG, WEBP for COA uploads

### 8.4 Monitoring and Error Tracking

| Tool | Purpose | Cost |
|------|---------|------|
| **Vercel Analytics** | Frontend performance, page views, Web Vitals | Free (included) |
| **Sentry** (free tier) | Error tracking, crash reporting (frontend + backend) | Free up to 5K events/month |
| **UptimeRobot** (free tier) | Uptime monitoring, downtime alerts | Free for 50 monitors |
| **Railway metrics** | Backend CPU, memory, request count | Free (included) |

### 8.5 Cost Estimate

| Service | Monthly Cost (MVP) | Monthly Cost (10K users) |
|---------|-------------------|-------------------------|
| Vercel (Hobby) | $0 | $0 (upgrade to Pro at $20 if needed) |
| Railway (Starter) | $5 | $10-$20 |
| Turso (Free) | $0 | $0 (free tier: 9 GB, 500M reads/month) |
| Cloudflare (Free) | $0 | $0 |
| Cloudflare R2 | $0 | $0 (free tier: 10 GB storage) |
| Domain | ~$1/month ($12/year) | ~$1/month |
| Sentry (Free) | $0 | $0 |
| UptimeRobot (Free) | $0 | $0 |
| **Total** | **~$6/month** | **~$12-22/month** |

This is well within the business plan's $200-$600/year hosting budget. Costs stay near zero until significant traffic arrives.

---

## 9. Week 1 Sprint Plan

### Constraints
- Solo founder
- 3-4 focused hours per day on Peptide Checker (per decision matrix allocation)
- Target: deployable MVP by end of Week 2 (10 working days)
- Claude Code available for pair programming

### Day 1 (Monday): Project Setup + Database

**Morning (2 hrs):**
- [ ] Create GitHub monorepo `peptide-checker-web`
- [ ] Initialize Next.js 14 app with App Router + Tailwind CSS
- [ ] Initialize FastAPI backend with `uv` or `poetry`
- [ ] Define SQLite schema (copy SQL from Section 2 of this spec)
- [ ] Write and run migration script

**Afternoon (2 hrs):**
- [ ] Write `migrate_json_to_sqlite.py` -- import all existing JSON data from `peptide-checker/data/`
- [ ] Verify: 30 BPC-157 vendors + semaglutide data loads correctly
- [ ] Seed additional peptide records for all 19 Category 2 peptides (from consumer_guide.md + RQ-PEP-005)
- [ ] Seed regulatory_status records for all tracked peptides

**Done when:** `python -c "import sqlite3; conn = sqlite3.connect('peptide_checker.db'); print(conn.execute('SELECT COUNT(*) FROM test_results').fetchone())"` returns 30+ rows.

### Day 2 (Tuesday): FastAPI Backend Core

**Morning (2 hrs):**
- [ ] Implement `GET /v1/peptides` and `GET /v1/peptides/{slug}`
- [ ] Implement `GET /v1/vendors` with query params (peptide, grade, sort)
- [ ] Implement `GET /v1/vendors/{slug}`

**Afternoon (2 hrs):**
- [ ] Implement `GET /v1/search?q=`
- [ ] Implement `GET /v1/regulatory` and `GET /v1/regulatory/{slug}`
- [ ] Add OpenAPI docs (FastAPI auto-generates at `/docs`)
- [ ] Write basic pytest tests for each endpoint

**Done when:** `curl http://localhost:8000/v1/vendors?peptide=bpc-157&grade=A` returns JSON with vendor data.

### Day 3 (Wednesday): Frontend -- Vendor Pages

**Morning (2 hrs):**
- [ ] Build layout: header, footer, navigation, disclaimer banner
- [ ] Build `/vendors` page with search bar, grade filter, vendor cards
- [ ] Connect to FastAPI backend via `fetch` / SWR

**Afternoon (2 hrs):**
- [ ] Build `/vendors/[slug]` page showing vendor profile and test results
- [ ] Build grade badge component (colored A-E badges)
- [ ] Build confidence indicator component
- [ ] Responsive design (mobile-first)

**Done when:** Navigating to `localhost:3000/vendors` shows filterable vendor cards with real data from the API.

### Day 4 (Thursday): Frontend -- Peptide Pages + Regulatory

**Morning (2 hrs):**
- [ ] Build `/peptides` directory page
- [ ] Build `/peptides/[slug]` page with regulatory status, evidence tier, vendor summary
- [ ] Convert consumer_guide.md content for top 3 peptides (semaglutide, tirzepatide, BPC-157)

**Afternoon (2 hrs):**
- [ ] Build `/regulatory` dashboard with status badges for all 19 Category 2 peptides
- [ ] Build `/regulatory/[slug]` timeline page
- [ ] Add Kennedy announcement vs. formal rule distinction in UI

**Done when:** `/peptides/bpc-157` shows a complete page with regulatory status, evidence tier, vendor stats, and educational content.

### Day 5 (Friday): Storage Calculator + COA Upload

**Morning (2 hrs):**
- [ ] Build `/tools/storage-calculator` -- form inputs, degradation calculation, results display
- [ ] Implement client-side degradation math using constants from peptides table
- [ ] Add degradation curve visualization (simple chart with Chart.js or recharts)

**Afternoon (2 hrs):**
- [ ] Build `/tools/coa-verification` -- file upload form
- [ ] Implement `POST /v1/coa/upload` backend endpoint
- [ ] Implement 3-4 basic red-flag rules (round purity, missing chromatogram, vendor cross-reference)
- [ ] Display results with red-flag cards

**Done when:** Uploading a PDF COA returns a list of detected red flags and a cross-reference against the vendor database.

### Weekend: Polish + Reports + Deploy

**Saturday (2-3 hrs):**
- [ ] Convert 2-3 research reports from Markdown to MDX pages under `/reports/`
- [ ] Build `/reports` index page
- [ ] Add Schema.org JSON-LD to all page types
- [ ] Add `robots.txt` and `sitemap.xml` (Next.js generates these)
- [ ] Write medical disclaimer, privacy policy, and terms of service (use templates, schedule attorney review)

**Sunday (2-3 hrs):**
- [ ] Deploy frontend to Vercel
- [ ] Deploy backend to Railway
- [ ] Configure custom domain + DNS via Cloudflare
- [ ] Set up Sentry error tracking
- [ ] Set up UptimeRobot monitoring
- [ ] Smoke test all pages on production
- [ ] Register domain if not already done

### Definition of "Done" for MVP Launch

The MVP is complete and ready for soft launch when ALL of the following are true:

1. **Vendor database is live** with 30+ vendors, searchable and filterable by peptide and grade
2. **Peptide pages exist** for at least 5 peptides (BPC-157, semaglutide, tirzepatide, ipamorelin, CJC-1295) with educational content, regulatory status, and evidence tiers
3. **Regulatory tracker** shows current status for all 19 Category 2 peptides with the Kennedy announcement context
4. **Storage calculator** works for at least 4 peptides with degradation models
5. **COA verification** accepts PDF uploads and returns basic red-flag analysis
6. **At least 2 research reports** are published as web pages
7. **Medical disclaimer** appears on every page
8. **Privacy policy and terms of service** are published (attorney review can be in progress)
9. **Site is deployed** on a custom domain with SSL
10. **Mobile-responsive** -- all pages readable on phone screens

This is NOT required for MVP:
- User accounts / authentication
- Subscription billing
- Full Finnrick data import (expand after launch)
- ML-powered COA analysis
- Automated regulatory updates
- Email newsletter
- Social sharing features

---

## Appendix A: File Structure

```
peptide-checker-web/
├── frontend/
│   ├── app/
│   │   ├── layout.tsx                    # Root layout with disclaimer banner
│   │   ├── page.tsx                      # Homepage
│   │   ├── peptides/
│   │   │   ├── page.tsx                  # Peptide directory
│   │   │   └── [slug]/
│   │   │       └── page.tsx              # Individual peptide page
│   │   ├── vendors/
│   │   │   ├── page.tsx                  # Vendor directory with search/filter
│   │   │   └── [slug]/
│   │   │       └── page.tsx              # Individual vendor profile
│   │   ├── regulatory/
│   │   │   ├── page.tsx                  # Regulatory dashboard
│   │   │   └── [slug]/
│   │   │       └── page.tsx              # Peptide regulatory timeline
│   │   ├── reports/
│   │   │   ├── page.tsx                  # Reports index
│   │   │   └── [slug]/
│   │   │       └── page.mdx              # Individual report (MDX)
│   │   ├── guides/
│   │   │   └── [slug]/
│   │   │       └── page.mdx              # Consumer guides (MDX)
│   │   ├── tools/
│   │   │   ├── storage-calculator/
│   │   │   │   └── page.tsx
│   │   │   └── coa-verification/
│   │   │       └── page.tsx
│   │   ├── about/page.tsx
│   │   ├── privacy/page.tsx
│   │   ├── health-data-privacy/page.tsx
│   │   ├── terms/page.tsx
│   │   └── disclaimer/page.tsx
│   ├── components/
│   │   ├── GradeBadge.tsx
│   │   ├── ConfidenceIndicator.tsx
│   │   ├── RegulatoryStatusBadge.tsx
│   │   ├── EvidenceTierBadge.tsx
│   │   ├── DisclaimerBanner.tsx
│   │   ├── SearchBar.tsx
│   │   ├── VendorCard.tsx
│   │   ├── PeptideCard.tsx
│   │   ├── RedFlagCard.tsx
│   │   └── DegradationChart.tsx
│   ├── lib/
│   │   ├── api.ts                        # Backend API client
│   │   ├── degradation.ts                # Storage calculator math
│   │   └── types.ts                      # Shared TypeScript types
│   ├── tailwind.config.ts
│   ├── next.config.mjs
│   └── package.json
├── backend/
│   ├── app/
│   │   ├── main.py                       # FastAPI app entrypoint
│   │   ├── routers/
│   │   │   ├── peptides.py
│   │   │   ├── vendors.py
│   │   │   ├── search.py
│   │   │   ├── regulatory.py
│   │   │   ├── coa.py
│   │   │   └── tools.py
│   │   ├── models/
│   │   │   ├── database.py               # SQLite connection + Turso config
│   │   │   └── schemas.py                # Pydantic response models
│   │   ├── services/
│   │   │   ├── coa_analyzer.py           # Red-flag detection logic
│   │   │   ├── ratings.py                # Vendor rating aggregation
│   │   │   └── storage.py                # R2 file storage client
│   │   └── middleware/
│   │       └── rate_limit.py             # slowapi rate limiting
│   ├── tests/
│   │   ├── test_peptides.py
│   │   ├── test_vendors.py
│   │   └── test_coa.py
│   ├── pyproject.toml
│   ├── Dockerfile
│   └── requirements.txt
├── scripts/
│   ├── migrate_json_to_sqlite.py         # One-time data migration
│   ├── seed_peptides.py                  # Seed peptide + regulatory data
│   ├── import_finnrick.py                # Bulk Finnrick data import
│   └── recompute_ratings.py              # Recompute vendor_ratings from test_results
├── data/
│   ├── bpc157/                           # Copied from peptide-checker/data/
│   ├── semaglutide/
│   └── schema.json
├── .github/
│   └── workflows/
│       └── ci.yml
└── README.md
```

## Appendix B: Degradation Model Constants

From RQ-PEP-004 research data, to be stored in the `peptides` table:

| Peptide | Lyophilized Shelf Life (2-8C) | Reconstituted Shelf Life (2-8C) | Room Temp Degradation (%/day) | Freeze-Thaw Loss (%/cycle) | Primary Degradation Pathway |
|---------|------------------------------|-------------------------------|------------------------------|---------------------------|---------------------------|
| BPC-157 | 2+ years | 10-14 days | 2-3% | 3-5% | Oxidation, aspartimide formation |
| TB-500 (Thymosin Beta-4) | 2+ years | 14-21 days | 1-2% | 2-5% | Aggregation |
| Semaglutide | Per label (18 months) | 56 days (pen, per label) | <1% | 1-2% | Deamidation |
| Tirzepatide | Per label | 21 days (per label) | <1% | 1-2% | Deamidation |
| Ipamorelin | 1-2 years | 10-14 days | 2-3% | 2-4% | Oxidation |
| CJC-1295 | 1-2 years | 10-14 days | 2-3% | 2-4% | Aggregation |
| GHK-Cu | 2+ years | 14-21 days | 1-2% | 1-3% | Copper dissociation |
| PT-141 | 1-2 years | 10-14 days | 2-3% | 2-4% | Oxidation |

## Appendix C: Category 2 Peptide Reference List

All 19 peptides on the FDA Category 2 restricted list as of March 2026, to be seeded into the `peptides` table:

| # | Peptide | Announced for Category 1 Return | WADA 2026 Status |
|---|---------|-------------------------------|-----------------|
| 1 | BPC-157 | Yes | Prohibited (S0) |
| 2 | Thymosin Alpha-1 | Yes | Not listed |
| 3 | AOD-9604 | Yes | Prohibited (S0) |
| 4 | GHK-Cu | Yes | Not listed |
| 5 | Thymosin Beta-4 (TB-500) | Yes | Prohibited (S0) |
| 6 | Epithalon | TBD | Not listed |
| 7 | Selank | Yes | Not listed |
| 8 | Semax | Yes | Not listed |
| 9 | DSIP (Delta Sleep-Inducing Peptide) | TBD | Not listed |
| 10 | CJC-1295 | Yes | Prohibited (S2) |
| 11 | Ipamorelin | Yes | Prohibited (S2) |
| 12 | Tesamorelin | Yes | Prohibited (S2) |
| 13 | Sermorelin | Yes | Prohibited (S2) |
| 14 | GHRP-2 | Yes | Prohibited (S2) |
| 15 | GHRP-6 | Yes | Prohibited (S2) |
| 16 | IGF-1 LR3 | TBD | Prohibited (S2) |
| 17 | Mechano Growth Factor (MGF) | TBD | Prohibited (S2) |
| 18 | Follistatin 344 | TBD | Prohibited (S2) |
| 19 | PT-141 (Bremelanotide) | Yes | Not listed |

Note: "Announced for Category 1 Return" reflects the Kennedy Feb 27 announcement. No formal FDA rulemaking has been published as of March 24, 2026. The regulatory tracker must clearly distinguish between announcements and formal rules.

---

*Technical specification generated 2026-03-24*
*This is a build document. Start with Day 1 of the sprint plan.*
*Review and update at end of Week 1 based on actual progress.*
