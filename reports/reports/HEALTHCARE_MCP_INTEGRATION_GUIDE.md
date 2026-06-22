# Healthcare MCP Integration Guide for Peptide-Checker & HUMMBL

**Date:** 2026-03-24
**Status:** Active reference document
**Feeds:** Goal 10 (Consumer Education Engine), Goal 7 (Peptide Quality Database), Goal 9 (GLP-1 Verification Service)

---

## Table of Contents

1. [Available MCP Tools](#1-available-mcp-tools)
2. [ChEMBL for Peptide Research](#2-chembl-for-peptide-research)
3. [Clinical Trials for Peptide Evidence](#3-clinical-trials-for-peptide-evidence)
4. [CMS Coverage for GLP-1 Analysis](#4-cms-coverage-for-glp-1-analysis)
5. [NPI for Provider Verification](#5-npi-for-provider-verification)
6. [ICD-10 for Condition Mapping](#6-icd-10-for-condition-mapping)
7. [Integration Architecture](#7-integration-architecture)
8. [Automated Research Report Pipeline](#8-automated-research-report-pipeline)
9. [Example Workflows](#9-example-workflows)

---

## 1. Available MCP Tools

### Tool Inventory

| MCP Server | Tools | Data Source | Rate Limits |
|---|---|---|---|
| **ChEMBL** | `compound_search`, `drug_search`, `get_bioactivity`, `get_mechanism`, `get_admet`, `target_search` | EMBL-EBI ChEMBL v34 | API-based, generous |
| **Clinical Trials** | `search_trials`, `get_trial_details`, `analyze_endpoints`, `search_investigators`, `search_by_sponsor`, `search_by_eligibility` | ClinicalTrials.gov v2 | Public API |
| **CMS Coverage** | `search_national_coverage`, `search_local_coverage`, `get_coverage_document`, `sad_exclusion_list`, `get_contractors`, `get_whats_new_report` | Medicare Coverage Database | Public API |
| **NPI Registry** | `npi_search`, `npi_lookup`, `npi_validate` | CMS NPPES v2.1 | Max 200 results/req |
| **ICD-10 Codes** | `search_codes`, `lookup_code`, `validate_code`, `get_hierarchy`, `get_by_category`, `get_by_body_system` | 2026 ICD-10-CM/PCS | Local data |

---

## 2. ChEMBL for Peptide Research

### 2.1 Peptide Compound Lookup Results

**Verified ChEMBL entries for key peptides (queried 2026-03-24):**

| Peptide | ChEMBL ID | Type | Max Phase | MW (Da) | Natural Product | Notes |
|---|---|---|---|---|---|---|
| **BPC-157** | CHEMBL4297358 | Protein | 1 (Phase I) | 1419.56 | Yes | Synonyms: Bepecin, PL-10, PL-14736, PLD-116 |
| **Semaglutide** | CHEMBL2108724 | Protein | 4 (Approved) | N/A (seq) | No | Brands: Ozempic, Wegovy, Rybelsus. First approved 2017 |
| **Tirzepatide** | CHEMBL4297839 | Protein | 4 (Approved) | N/A (seq) | No | Brands: Mounjaro, Zepbound. First-in-class. Approved 2022 |
| **TB-500** | Not found | -- | -- | -- | -- | Fragment of thymosin beta-4; not catalogued as distinct compound |
| **Thymosin Beta-4** | Not found (by name) | -- | -- | -- | -- | Search by "thymosin beta" returns no ChEMBL compounds |

**Key finding:** BPC-157 IS in ChEMBL (CHEMBL4297358) with Phase 1 designation and molecular formula C62H98N16O22. TB-500 and full-length thymosin beta-4 are NOT in ChEMBL, limiting automated research for those peptides via this source.

### 2.2 How to Look Up Peptides

```
Tool: compound_search
Parameters:
  name: "BPC-157"        # Try common names, trade names, and synonyms

Tool: compound_search
Parameters:
  name: "semaglutide"
  max_phase: 4           # Filter to approved drugs only
```

**Search strategy for peptides not found by name:**
1. Try alternative names (e.g., "pentadecapeptide BPC 157", "Bepecin")
2. Try the parent protein name (e.g., "thymosin" for TB-500)
3. Search by SMILES if you have the structure
4. Fall back to `drug_search` with indication (e.g., indication="wound healing")

### 2.3 Bioactivity Data

**Semaglutide bioactivity (CHEMBL2108724) -- verified data:**

| Assay | Target | Value | Units | pChEMBL | Source |
|---|---|---|---|---|---|
| IC50 (no HSA) | GLP-1 Receptor | 0.13 | nM | 9.89 | J Med Chem 2015 |
| IC50 (no HSA) | GLP-1 Receptor | 0.38 | nM | 9.42 | J Med Chem 2015 |
| IC50 (with 2% HSA) | GLP-1 Receptor | 30 | nM | 7.52 | J Med Chem 2015 |
| IC50 (with 2% HSA) | GLP-1 Receptor | 357 | nM | 6.45 | J Med Chem 2015 |
| T1/2 | Human | 160-165 | hours | -- | J Med Chem 2015 |
| HbA1c reduction | T2D patients | 1.7 | % | -- | Bioorg Med Chem Lett 2013 |
| Weight reduction | T2D patients | 4.8 | kg | -- | Bioorg Med Chem Lett 2013 |

**BPC-157 bioactivity (CHEMBL4297358):** Zero bioactivity records in ChEMBL. This is significant -- BPC-157 has no standardized IC50/EC50/Ki data in the primary medicinal chemistry database. All evidence is from animal studies published in journals, not deposited as structured bioactivity data.

**What this means for peptide-checker:** For peptides like BPC-157 and TB-500, ChEMBL bioactivity data is sparse or absent. The pipeline must fall back to Clinical Trials and literature search (bioRxiv MCP) for evidence.

### 2.4 Mechanism of Action Data

**Semaglutide (CHEMBL2108724):**
- MoA: Glucagon-like peptide 1 receptor **AGONIST**
- Target: CHEMBL1784 (GLP-1R)
- Direct interaction: Yes
- Disease efficacy: Yes
- Comment: "Peptide, GLP-1 analogue"
- References: PubMed 22918257, 24608440

**Tirzepatide (CHEMBL4297839) -- dual mechanism:**
1. Gastric inhibitory polypeptide (GIP) receptor **AGONIST** (Target: CHEMBL4383)
2. Glucagon-like peptide 1 (GLP-1) receptor **AGONIST** (Target: CHEMBL1784)
- Both direct interactions, both disease efficacy confirmed
- First-in-class dual GIP/GLP-1 agonist
- Reference: PubMed 33325008

**BPC-157:** No mechanism data in ChEMBL. The proposed mechanisms (NO system modulation, VEGF upregulation, FAK-paxillin pathway) exist only in primary literature, not in structured databases.

### 2.5 ADMET Properties

ChEMBL provides **calculated** molecular properties, not experimental ADMET. For peptides with structure_type="SEQ" (semaglutide, tirzepatide), calculated properties may be unavailable since SMILES/InChI are not provided for large sequences.

BPC-157 (CHEMBL4297358) has a SMILES structure and MW=1419.56, but key ADMET descriptors (ALogP, PSA, HBA, HBD, QED) are all null in ChEMBL -- peptides violate traditional drug-likeness rules (Lipinski Ro5) by design due to high molecular weight.

**Practical implication:** ADMET via ChEMBL is not useful for peptides. Peptide pharmacokinetics (half-life, bioavailability, degradation) must come from clinical trial data and published literature.

### 2.6 Automating Peptide Research via ChEMBL

```python
# Pseudocode for automated ChEMBL peptide research
def chembl_peptide_report(peptide_name):
    # Step 1: Find compound
    compound = compound_search(name=peptide_name)
    if not compound:
        return {"status": "NOT_IN_CHEMBL", "fallback": "clinical_trials"}

    chembl_id = compound.molecule_chembl_id

    # Step 2: Get mechanism
    mechanism = get_mechanism(molecule_chembl_id=chembl_id)

    # Step 3: Get bioactivity
    bioactivity = get_bioactivity(molecule_chembl_id=chembl_id, limit=50)

    # Step 4: Get ADMET (may be empty for peptides)
    admet = get_admet(molecule_chembl_id=chembl_id)

    return {
        "compound": compound,
        "mechanism": mechanism,
        "bioactivity": bioactivity,
        "admet": admet,
        "max_phase": compound.max_phase,
        "evidence_level": classify_evidence(compound.max_phase, len(bioactivity))
    }
```

---

## 3. Clinical Trials for Peptide Evidence

### 3.1 Trial Counts (Queried 2026-03-24)

| Peptide | Total Trials | Recruiting | Completed | Phase 1 | Phase 2 | Phase 3 | Phase 4 |
|---|---|---|---|---|---|---|---|
| **BPC-157** | 2 | 1 | 0 | 1 | 1 | 0 | 0 |
| **Semaglutide** | 661 | Many | Many | Yes | Yes | Yes | Yes |
| **TB-500 / Thymosin Beta-4** | 17 | 1 | ~10 | Yes | Yes | Yes (dry eye) | 0 |
| **Tirzepatide** | 221 | Many | Many | Yes | Yes | Yes | Yes |

### 3.2 Key Trials Discovered

#### BPC-157

**NCT07437547** (ACTIVE - RECRUITING)
- Title: "Randomized, Double-Blind, Placebo-Controlled Phase 2 Trial of BPC 157 for Accelerated Repair of Acute Grade II Hamstring Strain"
- Sponsor: Hudson Biotech
- Phase: 2
- Enrollment: 120
- Start: 2026-02-02
- Status: **RECRUITING** -- first rigorous human efficacy trial for BPC-157 in musculoskeletal injury

**NCT02637284** (Phase 1, status UNKNOWN)
- Title: Phase I Pilot Study assessing safety/PK of PCO-02 (active ingredient BPC-157)
- Sponsor: PharmaCotherapia d.o.o. (Croatia)
- Enrollment: 42 healthy volunteers
- Dates: 2015-2016
- Status unknown -- likely completed but results not posted

#### TB-500 / Thymosin Beta-4

**NCT07487363** (ACTIVE - RECRUITING)
- Title: "Phase 1/2 Study of TB-500 (Thymosin Beta 4 17-23 Fragment) in Adults with Stable Atherosclerotic Cardiovascular Disease"
- Sponsor: Hudson Biotech
- Phase: 1/2
- Enrollment: 80
- Start: 2026-02-05
- Key: First formal clinical trial of the TB-500 fragment specifically (not full-length TB4)

**NCT03937882** (Completed, Phase 3)
- Title: "ARISE-3: RGN-259 for Treatment of Dry Eye"
- RGN-259 = thymosin beta-4 ophthalmic solution
- Enrollment: 700
- Sponsor: ReGenTree, LLC
- This is the most advanced thymosin beta-4 trial (Phase 3, large enrollment)

**NCT05984134** (Completed, Phase 2b)
- Recombinant Human Thymosin Beta-4 (NL005) for Acute Myocardial Infarction
- Sponsor: Beijing Northland Biotech
- Enrollment: 90

### 3.3 Building Evidence Level Ratings

Based on the data above, here is the proposed evidence rating system:

```
EVIDENCE LEVELS:
  Level 1: FDA Approved (max_phase = 4)
           -> Semaglutide, Tirzepatide

  Level 2: Phase 3 Completed with positive results
           -> Thymosin Beta-4 for dry eye (RGN-259/ARISE trials)

  Level 3: Phase 2 Active or Completed
           -> BPC-157 (NCT07437547 recruiting)
           -> Thymosin Beta-4 for AMI (NL005)

  Level 4: Phase 1 Only / Animal Data with Trial Registered
           -> BPC-157 historically (Phase 1 from 2015)
           -> TB-500 fragment (Phase 1/2 just started)

  Level 5: Preclinical / Animal Data Only, No Human Trials
           -> Many research peptides (CJC-1295, Ipamorelin, etc.)

  Level 6: No Published Data / Unresearched
```

**Automation logic:**
```python
def get_evidence_level(peptide_name):
    # Check ChEMBL max_phase
    compound = compound_search(name=peptide_name)
    if compound and compound.max_phase == 4:
        return 1  # FDA approved

    # Check clinical trials
    trials = search_trials(intervention=peptide_name, count_total=True)

    if trials.total == 0:
        return 5 if has_pubmed_data(peptide_name) else 6

    max_phase_trial = max(trial.phase for trial in trials if trial.phase)

    if "PHASE3" in max_phase_trial:
        completed_p3 = [t for t in trials if "PHASE3" in t.phase and t.status == "COMPLETED"]
        return 2 if completed_p3 else 3
    elif "PHASE2" in max_phase_trial:
        return 3
    elif "PHASE1" in max_phase_trial:
        return 4

    return 5
```

### 3.4 Investigator Verification via NPI Cross-Reference

For any clinical trial, extract the principal investigator name and verify via NPI:

```
# Step 1: Find investigators for a trial area
Tool: search_investigators
Parameters:
  condition: "obesity"
  location: "United States"
  status: ["RECRUITING"]

# Step 2: For each investigator name, verify NPI
Tool: npi_search
Parameters:
  first_name: "John"
  last_name: "Smith"
  enumeration_type: "NPI-1"
  taxonomy_description: "Internal Medicine"

# Step 3: Get full credentials
Tool: npi_lookup
Parameters:
  npi: "1234567890"
```

### 3.5 Endpoint Analysis

Use `analyze_endpoints` to understand what outcomes are being measured for peptide classes:

```
# Aggregate endpoint analysis for obesity trials (GLP-1 context)
Tool: analyze_endpoints
Parameters:
  condition: "obesity"
  phase: ["PHASE3"]
  page_size: 100

# Single trial deep-dive
Tool: analyze_endpoints
Parameters:
  nct_id: "NCT07437547"   # BPC-157 hamstring trial
```

---

## 4. CMS Coverage for GLP-1 Analysis

### 4.1 Coverage Status (Verified 2026-03-24)

**Critical finding: Both semaglutide and tirzepatide are on the Self-Administered Drug (SAD) Exclusion List.**

This means:
- Ozempic (semaglutide) -- **EXCLUDED from Part B** (self-administered injectable)
- Wegovy (semaglutide) -- **EXCLUDED from Part B**
- Mounjaro (tirzepatide) -- **EXCLUDED from Part B**
- Zepbound (tirzepatide) -- **EXCLUDED from Part B**

These drugs are billed under HCPCS codes C9399, J3490, J3590 and are classified as self-administered across **all** Medicare Administrative Contractors (First Coast, WPS, NGS, Noridian, Novitas, Palmetto, CGS).

**Coverage pathway:** These are Part D (prescription drug plan) coverage, NOT Part B. Coverage varies by plan formulary.

### 4.2 Relevant National Coverage Determinations

| NCD ID | Title | Last Updated |
|---|---|---|
| 100.1 | Bariatric Surgery for Treatment of Co-Morbid Conditions Related to Morbid Obesity | 04/09/2025 |
| 210.12 | Intensive Behavioral Therapy for Obesity | 12/02/2024 |
| 40.5 | Treatment of Obesity (RETIRED -- incorporated into 100.1) | 08/16/2023 |
| 100.11 | Gastric Balloon for Treatment of Obesity (RETIRED) | 06/06/2024 |

**Key NCD 100.1** (Bariatric Surgery) was updated April 2025 -- worth monitoring for whether anti-obesity medications get incorporated.

### 4.3 Impact on Compounding Market

The SAD exclusion list status creates the following market dynamics:

1. **Self-injection = Part D coverage** -- higher out-of-pocket for Medicare patients
2. **Compounded semaglutide** fills the cost gap for patients who cannot afford branded versions
3. **FDA crackdown on compounding** (post-shortage declaration) directly threatens this market
4. **No NCD/LCD for injectable GLP-1 agonists** -- Medicare has no national policy covering these drugs under Part B

### 4.4 Automated Coverage Monitoring

```python
def monitor_glp1_coverage():
    """Run weekly to detect coverage policy changes"""

    # Check for new NCDs mentioning obesity/GLP-1
    ncds = search_national_coverage(keyword="obesity", document_type="ncd")

    # Check SAD list for any changes to semaglutide/tirzepatide
    sema_sad = sad_exclusion_list(keyword="semaglutide")
    tirz_sad = sad_exclusion_list(keyword="tirzepatide")

    # Check for new LCDs
    lcds = search_local_coverage(keyword="GLP-1", document_type="lcd")

    # Check what's new
    national_changes = get_whats_new_report()  # national

    # Alert if any new documents appear
    return {
        "ncd_count": ncds.count,
        "semaglutide_sad_entries": sema_sad.count,
        "tirzepatide_sad_entries": tirz_sad.count,
        "lcd_results": lcds.count,
        "timestamp": datetime.now()
    }
```

---

## 5. NPI for Provider Verification

### 5.1 Compounding Pharmacy Verification

**Verified query pattern** -- searching NPI registry for compounding pharmacies:

```
Tool: npi_search
Parameters:
  organization_name: "compound*"
  enumeration_type: "NPI-2"
  limit: 200
```

**Sample results (verified 2026-03-24):**

| NPI | Name | Taxonomy | Location |
|---|---|---|---|
| 1215143490 | Compound Pharmaceutical Technologies, Inc. | Compounding Pharmacy (3336C0004X) | Daphne, AL |
| 1316558521 | Compound Preferred LLC | Compounding Pharmacy (3336C0004X) | Idaho Falls, ID |
| 1447648084 | CompoundCorrectRx | Compounding Pharmacy (3336C0004X) | Franklin, TN |
| 1770849424 | Compounder, LLC | Compounding Pharmacy (3336C0004X) | Columbia, MD |
| 1972649598 | Compound Central Pharmacy | Community/Retail Pharmacy (3336C0003X) | Los Alamitos, CA |

**Key taxonomy codes for peptide-checker:**
- `3336C0004X` = Compounding Pharmacy (the specific type we want)
- `3336C0003X` = Community/Retail Pharmacy (may also compound)

### 5.2 Prescriber Verification Workflow

```
# Step 1: Validate NPI format (instant, no API call)
Tool: npi_validate
Parameters:
  npi: "1234567893"
# Returns: valid/invalid + Luhn check

# Step 2: Look up full provider details
Tool: npi_lookup
Parameters:
  npi: "1234567893"
# Returns: name, credentials, specialty, practice address, license

# Step 3: Search by name if NPI unknown
Tool: npi_search
Parameters:
  first_name: "John"
  last_name: "Smith"
  taxonomy_description: "Internal Medicine"
  state: "CA"
```

### 5.3 "Prescriber Verified" Badge System

For peptide-checker, implement a verification tier:

```
VERIFICATION LEVELS:

  GREEN (Verified):
    - NPI exists and is Active
    - Taxonomy matches relevant specialty (Internal Medicine, Endocrinology, etc.)
    - Practice address is a real medical facility

  YELLOW (Partial):
    - NPI exists but specialty does not align (e.g., dentist prescribing peptides)
    - OR NPI is active but provider has non-standard taxonomy

  RED (Unverified):
    - NPI not found in NPPES
    - NPI is Deactivated
    - NPI fails Luhn validation (likely fake)

  GRAY (Cannot Verify):
    - International provider (not in US NPPES)
    - No NPI provided by prescriber
```

### 5.4 Telehealth Platform Prescriber Audit

To verify prescribers on telehealth peptide platforms:

```python
def audit_telehealth_prescribers(platform_prescriber_list):
    results = []
    for prescriber in platform_prescriber_list:
        # Validate format
        if prescriber.npi:
            validation = npi_validate(npi=prescriber.npi)
            if not validation.valid:
                results.append({"name": prescriber.name, "status": "INVALID_NPI"})
                continue

            # Full lookup
            details = npi_lookup(npi=prescriber.npi)
            results.append({
                "name": prescriber.name,
                "npi": prescriber.npi,
                "status": details.status,  # A=Active, D=Deactivated
                "specialty": details.primary_taxonomy_desc,
                "credentials": details.credentials,
                "state": details.practice_state,
                "verified": details.found and details.status == "A"
            })
        else:
            # Search by name
            matches = npi_search(
                first_name=prescriber.first_name,
                last_name=prescriber.last_name,
                enumeration_type="NPI-1"
            )
            results.append({
                "name": prescriber.name,
                "matches_found": matches.count,
                "status": "NEEDS_MANUAL_REVIEW"
            })
    return results
```

---

## 6. ICD-10 for Condition Mapping

### 6.1 Peptide-to-Condition Mapping

**BPC-157 -- Studied Conditions:**

| Use Case | ICD-10 Code | Description | Evidence Level |
|---|---|---|---|
| Musculoskeletal injury | S86.091A | Other specified injury of Achilles tendon, initial encounter | 3 (Phase 2 active) |
| Muscle strain | S46.x | Injury of muscle/tendon at shoulder level | 3 |
| Gastric ulcer | K25.3 | Acute gastric ulcer without hemorrhage or perforation | 4 (animal data) |
| Gastric ulcer (chronic) | K25.7 | Chronic gastric ulcer without hemorrhage or perforation | 4 |
| Inflammatory bowel | K58.9 | Irritable bowel syndrome, unspecified | 5 (preclinical) |
| Wound healing | T81.30XS | Disruption of wound, unspecified | 5 (preclinical) |

**Semaglutide -- Approved Indications:**

| Use Case | ICD-10 Code | Description | Evidence Level |
|---|---|---|---|
| Type 2 diabetes | E11.65 | T2DM with hyperglycemia | 1 (Approved) |
| Obesity, class 1 | E66.811 | Obesity, class 1 | 1 (Approved) |
| Obesity, class 2 | E66.812 | Obesity, class 2 | 1 (Approved) |
| Obesity, class 3 | E66.813 | Obesity, class 3 | 1 (Approved) |
| Morbid obesity | E66.01 | Morbid (severe) obesity due to excess calories | 1 (Approved) |
| CKD with T2D | N18.x + E11.x | Chronic kidney disease with T2DM | 2 (Phase 3) |
| Cardiovascular risk | I25.x | Chronic ischemic heart disease | 2 (SUSTAIN/SELECT trials) |

**Tirzepatide -- Approved Indications:**

| Use Case | ICD-10 Code | Description | Evidence Level |
|---|---|---|---|
| Type 2 diabetes | E11.65 | T2DM with hyperglycemia | 1 (Approved) |
| Obesity | E66.811-813 | Obesity classes 1-3 | 1 (Approved) |
| Heart failure with obesity | I50.x + E66.x | Heart failure + obesity | 2 (Phase 3) |

**TB-500 / Thymosin Beta-4 -- Studied Conditions:**

| Use Case | ICD-10 Code | Description | Evidence Level |
|---|---|---|---|
| Dry eye syndrome | H04.129 | Dry eye syndrome, unspecified | 2 (Phase 3 ARISE) |
| Acute MI | I21.x | Acute myocardial infarction | 3 (Phase 2b) |
| Pressure ulcers | L89.x | Pressure ulcer | 3 (Phase 2) |
| Venous stasis ulcers | I87.2 | Venous insufficiency | 3 (Phase 2) |
| Atherosclerotic CVD | I25.10 | Atherosclerotic heart disease | 4 (Phase 1/2 starting) |
| Epidermolysis bullosa | Q81.x | Epidermolysis bullosa | 4 (Phase 2, terminated) |

### 6.2 ICD-10 Search Patterns

```
# Find all obesity codes
Tool: search_codes
Parameters:
  query: "obesity"
  code_type: "diagnosis"
  limit: 50

# Find specific code details
Tool: lookup_code
Parameters:
  code: "E66.01"
  code_type: "diagnosis"

# Validate a code for billing
Tool: validate_code
Parameters:
  code: "E11.65"
  code_type: "diagnosis"
```

### 6.3 Consumer Education Mapping

For the peptide-checker consumer interface, present as:

```
BPC-157 Research Summary:
  Conditions Being Studied:
    - Muscle & Tendon Injuries (Phase 2 clinical trial, recruiting)
    - Gastric Ulcers (animal studies only)
    - Inflammatory Bowel Conditions (animal studies only)
    - Wound Healing (animal studies only)

  FDA Status: NOT approved for any condition
  Evidence Level: 3 (Early Human Trials)

  [Learn More About the Clinical Trial: NCT07437547]
```

---

## 7. Integration Architecture

### 7.1 Data Flow

```
                    +------------------+
                    |  MCP Tool Layer  |
                    +------------------+
                           |
            +--------------+--------------+
            |              |              |
        ChEMBL      ClinicalTrials    CMS/NPI/ICD-10
            |              |              |
            v              v              v
    +-------+------+  +---+----+  +------+-------+
    | Compound     |  | Trial  |  | Coverage     |
    | Bioactivity  |  | Evidence|  | Provider     |
    | Mechanism    |  | Endpoints| | Conditions   |
    +-------+------+  +---+----+  +------+-------+
            |              |              |
            +--------------+--------------+
                           |
                    +------v-------+
                    | Normalizer & |
                    | Cache Layer  |
                    +--------------+
                           |
                    +------v-------+
                    | peptide-     |
                    | checker DB   |
                    +--------------+
                           |
              +------------+------------+
              |            |            |
        Research      Consumer      Provider
        Reports       Education     Verification
```

### 7.2 Caching Strategy

| Data Source | Cache Duration | Rationale |
|---|---|---|
| ChEMBL compound data | 30 days | ChEMBL updates ~2x/year (major releases) |
| ChEMBL bioactivity | 30 days | Same release cycle |
| Clinical Trials search | 7 days | Trials update status frequently |
| Clinical Trial details | 14 days | Protocol details change less often |
| CMS NCD/LCD | 14 days | Policy changes are infrequent but important |
| CMS SAD List | 7 days | Updated quarterly but check weekly |
| NPI lookup | 30 days | Provider data changes slowly |
| NPI search | 1 day | New providers added daily |
| ICD-10 codes | 365 days | Annual release cycle (October) |

### 7.3 Cache Implementation

```python
import hashlib
import json
from datetime import datetime, timedelta

CACHE_TTL = {
    "chembl_compound": timedelta(days=30),
    "chembl_bioactivity": timedelta(days=30),
    "chembl_mechanism": timedelta(days=30),
    "clinical_trials_search": timedelta(days=7),
    "clinical_trials_detail": timedelta(days=14),
    "cms_ncd": timedelta(days=14),
    "cms_sad": timedelta(days=7),
    "npi_lookup": timedelta(days=30),
    "npi_search": timedelta(days=1),
    "icd10": timedelta(days=365),
}

def cache_key(tool_name, params):
    """Generate deterministic cache key from tool + params"""
    param_str = json.dumps(params, sort_keys=True)
    return f"{tool_name}:{hashlib.sha256(param_str.encode()).hexdigest()[:16]}"

def should_refresh(cache_entry, tool_category):
    """Check if cached data is stale"""
    age = datetime.now() - cache_entry.timestamp
    return age > CACHE_TTL[tool_category]
```

### 7.4 Update Frequency Schedule

| Task | Frequency | Tools Used |
|---|---|---|
| Full peptide compound refresh | Monthly | ChEMBL compound_search for each tracked peptide |
| Clinical trial status update | Weekly | Clinical Trials search_trials for each peptide |
| CMS coverage monitoring | Weekly | CMS search_national/local, sad_exclusion_list |
| NPI provider re-verification | Monthly | NPI npi_lookup for verified providers |
| ICD-10 code refresh | Annually (October) | ICD-10 search_codes for all mapped conditions |
| New peptide onboarding | On-demand | Full pipeline for new peptide entry |

---

## 8. Automated Research Report Pipeline

### 8.1 Pipeline Design

```
PEPTIDE RESEARCH REPORT PIPELINE
=================================

Input: peptide_name (e.g., "BPC-157")

Stage 1: COMPOUND IDENTIFICATION (ChEMBL)
  |-- compound_search(name=peptide_name)
  |-- IF found: get_mechanism(), get_bioactivity(), get_admet()
  |-- IF not found: flag as "not in primary databases"
  |-- Output: compound_profile{}

Stage 2: CLINICAL EVIDENCE (Clinical Trials)
  |-- search_trials(intervention=peptide_name, count_total=True)
  |-- FOR each trial: get_trial_details(nct_id)
  |-- analyze_endpoints(condition=primary_condition)
  |-- search_investigators(condition=primary_condition)
  |-- Output: evidence_profile{}

Stage 3: COVERAGE STATUS (CMS)
  |-- search_national_coverage(keyword=peptide_name)
  |-- search_local_coverage(keyword=peptide_name)
  |-- sad_exclusion_list(keyword=brand_names)
  |-- Output: coverage_profile{}

Stage 4: PROVIDER LANDSCAPE (NPI)
  |-- npi_search(taxonomy_description="Compounding Pharmacy")
  |-- FOR known prescribers: npi_validate() + npi_lookup()
  |-- Output: provider_profile{}

Stage 5: CONDITION MAPPING (ICD-10)
  |-- FOR each studied_condition:
  |     search_codes(query=condition_name)
  |     lookup_code(code=best_match)
  |-- Output: condition_map{}

Stage 6: SYNTHESIS
  |-- Combine all profiles
  |-- Calculate evidence_level (1-6 scale)
  |-- Generate consumer-facing summary
  |-- Generate provider-facing technical summary
  |-- Output: research_report.md
```

### 8.2 Report Template

```markdown
# Peptide Research Report: {PEPTIDE_NAME}
Generated: {DATE} | Evidence Level: {LEVEL} ({LEVEL_DESCRIPTION})

## Quick Summary
- **FDA Status:** {approved/unapproved}
- **Clinical Trials:** {total_count} ({recruiting_count} recruiting)
- **Highest Phase:** {max_phase}
- **Medicare Coverage:** {coverage_status}
- **ChEMBL ID:** {chembl_id or "Not catalogued"}

## What Is {PEPTIDE_NAME}?
{mechanism_of_action_plain_english}

## Scientific Evidence
### Bioactivity Data
{bioactivity_table}

### Clinical Trials
{trials_table_with_status}

### Mechanism of Action
{mechanism_details}

## Conditions Being Studied
{condition_icd10_mapping_table}

## Insurance & Coverage
{cms_coverage_analysis}

## Provider Verification
{prescriber_verification_notes}

## Risk Factors
{black_box_warnings}
{withdrawn_flags}
{sad_exclusion_status}

## Data Sources
- ChEMBL v34: {compound_url}
- ClinicalTrials.gov: {trial_urls}
- CMS Medicare Coverage Database: {ncd_lcd_urls}
- NPI Registry: {verification_date}
- ICD-10-CM 2026: {code_set_version}
```

### 8.3 Evidence Level Classification Logic

```python
def classify_evidence(chembl_data, trials_data, cms_data):
    """
    Classify peptide evidence on 1-6 scale.
    Combines ChEMBL max_phase, trial count/phase, and coverage data.
    """

    # Level 1: FDA Approved
    if chembl_data and chembl_data.get("max_phase") == 4:
        return 1, "FDA Approved"

    # Level 2: Phase 3 completed with positive results
    if trials_data:
        phase3_completed = [
            t for t in trials_data["items"]
            if t.get("phase") and "PHASE3" in t["phase"]
            and t["status"] == "COMPLETED"
        ]
        if phase3_completed:
            return 2, "Phase 3 Completed"

    # Level 3: Phase 2 data exists
    if trials_data:
        phase2_plus = [
            t for t in trials_data["items"]
            if t.get("phase") and any(p in t["phase"] for p in ["PHASE2", "PHASE3"])
        ]
        if phase2_plus:
            return 3, "Phase 2+ Clinical Data"

    # Level 4: Phase 1 or trials registered
    if trials_data and trials_data["total"] > 0:
        return 4, "Early Clinical Trials"

    # Level 5: In ChEMBL but no trials
    if chembl_data and chembl_data.get("molecule_chembl_id"):
        return 5, "Preclinical Data Only"

    # Level 6: Not in any database
    return 6, "No Published Data"
```

---

## 9. Example Workflows

### 9.1 Complete Workflow: BPC-157

```
STEP 1: ChEMBL Compound Search
===============================
Tool: compound_search
Params: { name: "BPC-157" }

Result:
  chembl_id: CHEMBL4297358
  type: Protein
  max_phase: 1
  MW: 1419.56 Da
  formula: C62H98N16O22
  synonyms: [Bepecin, PL-10, PL-14736, PLD-116]
  natural_product: true

STEP 2: ChEMBL Mechanism
=========================
Tool: get_mechanism
Params: { molecule_chembl_id: "CHEMBL4297358" }

Result: No mechanism data in ChEMBL.
Note: BPC-157 mechanism not yet curated. Literature suggests:
  - Nitric oxide (NO) system modulation
  - VEGF upregulation
  - FAK-paxillin pathway activation
  - Cytoprotective gastroprotection

STEP 3: ChEMBL Bioactivity
============================
Tool: get_bioactivity
Params: { molecule_chembl_id: "CHEMBL4297358" }

Result: 0 bioactivity records.
Note: No structured IC50/EC50/Ki data exists for BPC-157.

STEP 4: Clinical Trials Search
================================
Tool: search_trials
Params: { intervention: "BPC-157", count_total: true }

Result: 2 trials total

  Trial 1: NCT07437547 (RECRUITING)
    Phase 2, 120 patients
    Hamstring strain repair
    Sponsor: Hudson Biotech
    MRI-confirmed Grade II injury

  Trial 2: NCT02637284 (UNKNOWN)
    Phase 1, 42 healthy volunteers
    Safety/PK study
    Sponsor: PharmaCotherapia d.o.o.

STEP 5: CMS Coverage Check
============================
Tool: search_national_coverage
Params: { keyword: "BPC-157" }

Result: 0 NCDs. (BPC-157 is not FDA-approved; no Medicare coverage exists)

Tool: sad_exclusion_list
Params: { keyword: "BPC-157" }

Result: 0 entries. (Not on SAD list because not FDA-approved at all)

STEP 6: ICD-10 Condition Mapping
==================================
Tool: search_codes
Params: { query: "muscle strain", code_type: "diagnosis" }

Key codes:
  S86.091A - Achilles tendon injury, initial encounter
  S46.x    - Shoulder muscle/tendon injury
  K25.3    - Acute gastric ulcer
  K25.7    - Chronic gastric ulcer

STEP 7: Synthesize Report
===========================
Evidence Level: 3 (Phase 2 Active)
FDA Status: Not Approved
Clinical Trials: 2 (1 recruiting)
ChEMBL Data: Compound identified, no bioactivity/mechanism data
Medicare Coverage: None
Consumer Takeaway: "BPC-157 is currently in a Phase 2 clinical trial for
  muscle injury repair. It is NOT FDA-approved. No insurance covers it.
  The only rigorous human trial is recruiting now (NCT07437547)."
```

### 9.2 Complete Workflow: Semaglutide

```
STEP 1: ChEMBL Compound Search
===============================
Tool: compound_search
Params: { name: "semaglutide" }

Result:
  chembl_id: CHEMBL2108724
  type: Protein (sequence)
  max_phase: 4 (APPROVED)
  first_approval: 2017
  brands: [Ozempic, Wegovy, Rybelsus]
  oral: true, parenteral: true
  black_box_warning: true (thyroid C-cell tumors in rodents)
  USAN stem: -tide (-glutide) = GLP-1 analogs

STEP 2: ChEMBL Mechanism
=========================
Tool: get_mechanism
Params: { molecule_chembl_id: "CHEMBL2108724" }

Result:
  mechanism: "Glucagon-like peptide 1 receptor agonist"
  target: CHEMBL1784 (GLP-1R)
  action_type: AGONIST
  direct_interaction: true
  disease_efficacy: true
  references: PubMed 22918257, 24608440

STEP 3: ChEMBL Bioactivity
============================
Tool: get_bioactivity
Params: { molecule_chembl_id: "CHEMBL2108724", limit: 50 }

Result: 119 total bioactivity records. Key findings:
  - GLP-1R IC50 = 0.13 nM (pChEMBL 9.89) -- extremely potent
  - GLP-1R IC50 = 0.38 nM without HSA
  - GLP-1R IC50 = 30-357 nM with 2% HSA (albumin binding shifts potency)
  - Human T1/2 = 160-165 hours (~7 days, enabling weekly dosing)
  - HbA1c reduction: 1.7% in T2D patients
  - Weight reduction: 4.8 kg in T2D patients

STEP 4: Clinical Trials Search
================================
Tool: search_trials
Params: { intervention: "semaglutide", count_total: true }

Result: 661 total trials
  Conditions studied:
    - Type 2 diabetes (primary)
    - Obesity/overweight (primary)
    - Chronic kidney disease
    - Cardiovascular disease
    - NASH/MAFLD
    - Alzheimer's disease
    - Substance use disorders
    - And many more

STEP 5: CMS Coverage Check
============================
Tool: sad_exclusion_list
Params: { keyword: "semaglutide" }

Result: 20+ SAD entries across all MACs
  Ozempic: EXCLUDED from Part B (self-administered)
  Wegovy: EXCLUDED from Part B (self-administered)
  HCPCS codes: C9399, J3490, J3590
  Coverage: Part D (plan-specific formulary)

Tool: search_national_coverage
Params: { keyword: "obesity" }

Result: 4 NCDs found
  - NCD 100.1: Bariatric Surgery (updated April 2025)
  - NCD 210.12: Intensive Behavioral Therapy for Obesity
  Note: NO NCD exists specifically for GLP-1 medications

STEP 6: ICD-10 Condition Mapping
==================================
Primary codes:
  E11.65  - Type 2 diabetes with hyperglycemia
  E66.01  - Morbid obesity due to excess calories
  E66.811 - Obesity, class 1 (BMI 30-34.9)
  E66.812 - Obesity, class 2 (BMI 35-39.9)
  E66.813 - Obesity, class 3 (BMI 40+)
  E66.9   - Obesity, unspecified

STEP 7: Synthesize Report
===========================
Evidence Level: 1 (FDA Approved)
FDA Status: Approved 2017 (Ozempic), expanded indications ongoing
Clinical Trials: 661 (massive evidence base)
ChEMBL Data: Full compound profile, 119 bioactivity records
Medicare Coverage: Part D only (excluded from Part B as self-administered)
Black Box Warning: YES (thyroid C-cell tumors in rodents)
Consumer Takeaway: "Semaglutide is FDA-approved for type 2 diabetes
  (Ozempic) and weight management (Wegovy). It has the strongest
  evidence base of any peptide, with 661 clinical trials. Medicare
  covers it under Part D prescription drug plans, NOT Part B. It
  carries a black box warning about thyroid tumors found in animal
  studies."
```

---

## Appendix A: MCP Tool Quick Reference

### ChEMBL Tools

| Tool | When to Use | Key Params |
|---|---|---|
| `compound_search` | Look up any molecule by name | `name`, `chembl_id`, `max_phase` |
| `drug_search` | Find drugs by disease indication | `indication`, `only_approved` |
| `get_bioactivity` | Get IC50/EC50/Ki data | `molecule_chembl_id`, `activity_type` |
| `get_mechanism` | How a drug works | `molecule_chembl_id` |
| `get_admet` | Drug-likeness properties | `molecule_chembl_id` |
| `target_search` | Find protein targets | `target_name`, `gene_symbol` |

### Clinical Trials Tools

| Tool | When to Use | Key Params |
|---|---|---|
| `search_trials` | Find trials by condition/drug | `condition`, `intervention`, `status`, `phase` |
| `get_trial_details` | Deep-dive on specific trial | `nct_id` |
| `analyze_endpoints` | Compare outcome measures | `condition` or `nct_id`, `phase` |
| `search_investigators` | Find PIs and sites | `condition`, `location` |
| `search_by_sponsor` | Company pipeline analysis | `sponsor` |

### CMS Coverage Tools

| Tool | When to Use | Key Params |
|---|---|---|
| `search_national_coverage` | Find NCDs | `keyword`, `document_type="ncd"` |
| `search_local_coverage` | Find LCDs | `keyword`, `contractor_id` |
| `get_coverage_document` | Full NCD/LCD details | `document_id`, `document_type` |
| `sad_exclusion_list` | Check Part B exclusion | `keyword`, `hcpcs_code` |
| `get_contractors` | Find MACs by state | state param |

### NPI Registry Tools

| Tool | When to Use | Key Params |
|---|---|---|
| `npi_validate` | Format check (no API call) | `npi` |
| `npi_lookup` | Full provider details | `npi` |
| `npi_search` | Find providers | `first_name`, `last_name`, `taxonomy_description`, `state` |

### ICD-10 Tools

| Tool | When to Use | Key Params |
|---|---|---|
| `search_codes` | Find codes by description | `query`, `code_type` |
| `lookup_code` | Get specific code details | `code`, `code_type` |
| `validate_code` | Check HIPAA validity | `code`, `code_type` |

---

## Appendix B: Peptide Coverage Summary

| Peptide | ChEMBL | Trials | Evidence Level | FDA | Medicare Part B | Compounded |
|---|---|---|---|---|---|---|
| **Semaglutide** | CHEMBL2108724 | 661 | 1 (Approved) | Yes (2017) | SAD Excluded | Yes (market pressure) |
| **Tirzepatide** | CHEMBL4297839 | 221 | 1 (Approved) | Yes (2022) | SAD Excluded | Emerging |
| **BPC-157** | CHEMBL4297358 | 2 | 3 (Phase 2) | No | N/A | Primary market |
| **TB-500** | Not in ChEMBL | 1 (as fragment) | 4 (Phase 1/2) | No | N/A | Primary market |
| **Thymosin Beta-4** | Not in ChEMBL | 17 | 2 (Phase 3 dry eye) | No | N/A | Limited |

---

## Appendix C: Key Findings for Product Strategy

1. **BPC-157 is finally in real clinical trials.** NCT07437547 (Phase 2, hamstring repair, recruiting) is the first rigorous efficacy trial. This changes the peptide-checker narrative from "no human evidence" to "Phase 2 trial underway." Monitor this trial closely.

2. **Hudson Biotech is running both BPC-157 AND TB-500 trials.** Same sponsor for NCT07437547 (BPC-157) and NCT07487363 (TB-500). This company is the one to watch for peptide legitimization.

3. **GLP-1 drugs are universally SAD-excluded from Part B.** Semaglutide and tirzepatide are self-administered injectables, covered only under Part D. This creates the cost gap that drives the compounding market.

4. **No NCD exists for GLP-1 medications for obesity.** Medicare covers bariatric surgery (NCD 100.1) and behavioral therapy (NCD 210.12) but has no national coverage determination for anti-obesity medications. A future NCD here would reshape the market.

5. **ChEMBL has limited utility for research peptides.** BPC-157 has zero bioactivity records and no mechanism data. TB-500 is not even catalogued. The pipeline must rely heavily on Clinical Trials and literature search for these compounds.

6. **Compounding pharmacies are identifiable via NPI.** Taxonomy code 3336C0004X specifically identifies compounding pharmacies, enabling automated vendor verification for peptide-checker.

---

*This guide was generated using live MCP tool queries on 2026-03-24. All data points are verifiable by re-running the documented tool calls.*
