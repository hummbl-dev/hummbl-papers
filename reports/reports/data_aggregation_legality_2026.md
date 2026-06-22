# Data Aggregation Legality for Peptide-Checker (2026)

**Research Date:** 2026-03-24
**Purpose:** Can peptide-checker legally aggregate vendor data, testing results, and COA information from third-party sources?

**TL;DR:** Yes, with careful structuring. Factual data (purity percentages, test results) is not copyrightable in the US. Publicly available information can be aggregated. The main risks are (1) scraping behind logins or bypassing technical barriers, (2) defamation claims from vendors rated poorly, and (3) EU database rights if serving European users. The safest path: use APIs where available, link rather than copy, frame ratings as methodology-based opinions, and carry media liability insurance.

---

## Table of Contents

1. [Web Scraping Legality 2025-2026](#1-web-scraping-legality-2025-2026)
2. [Aggregating Public Test Data](#2-aggregating-public-test-data)
3. [Consumer Review Aggregation Precedents](#3-consumer-review-aggregation-precedents)
4. [Defamation and Vendor Litigation Risk](#4-defamation-and-vendor-litigation-risk)
5. [API and Data Licensing](#5-api-and-data-licensing)
6. [Best Practices for Peptide-Checker](#6-best-practices-for-peptide-checker)
7. [Data Pipeline Compliance Checklist](#7-data-pipeline-compliance-checklist)

---

## 1. Web Scraping Legality 2025-2026

### 1.1 hiQ Labs v. LinkedIn — Current Status and Implications

The landmark hiQ v. LinkedIn case went through five years of litigation (district courts, Ninth Circuit, Supreme Court, back to Ninth Circuit) before settling in late 2022.

**Key precedent established:** The Ninth Circuit conclusively held that scraping *publicly available* data cannot violate the Computer Fraud and Abuse Act (CFAA). The reasoning: one cannot access a website "without authorization" when no authorization is required in the first place.

**Settlement details (important nuance):** Despite the favorable CFAA ruling, hiQ ultimately paid $500,000 in damages and agreed to destroy all scraped data, source code, and algorithms. LinkedIn obtained a permanent injunction. The critical factor: hiQ had *also* scraped data behind logins using fake accounts — this crossed the line from public data scraping into unauthorized access.

**Takeaway for peptide-checker:** Scraping publicly viewable pages is legally defensible under CFAA. Scraping behind logins, using fake accounts, or circumventing access controls is not.

### 1.2 CFAA — What Is Illegal vs. Legal

**Legal under CFAA:**
- Accessing publicly available web pages that require no login
- Collecting factual data displayed openly on websites
- Automated collection of data that any visitor could see in a browser

**Illegal or high-risk under CFAA:**
- Accessing password-protected content without authorization
- Continuing to scrape after receiving a cease-and-desist *combined with* circumventing IP blocks or technical barriers
- Using fake accounts to access restricted data
- Exceeding authorized access (e.g., using a legitimate account to scrape data beyond its intended scope)

**Key cases:**
- *Van Buren v. United States* (2021, Supreme Court): Narrowed CFAA's "exceeds authorized access" to mean accessing areas of a computer one is not entitled to access — not accessing permitted areas with improper motives
- *Craigslist v. 3Taps*: Continued scraping after explicit revocation of access + circumvention of IP blocks = CFAA violation
- *Facebook v. Power Ventures*: Accessing data behind authentication after cease-and-desist = CFAA violation

### 1.3 Terms of Service Violations vs. Actual Law

**Critical distinction:** Violating a website's Terms of Service is *not automatically illegal*. Courts do not treat every TOS violation as a crime. However:

- TOS violations can support breach of contract claims (civil, not criminal)
- TOS violations can establish "intent" and "non-consensual access" in CFAA arguments
- Some jurisdictions (e.g., Texas Northern District, favored by X Corp) view TOS violations more seriously
- The trend in 2025-2026 is toward platforms using DMCA anti-circumvention (Section 1201) rather than CFAA alone

**Recent shift — DMCA Section 1201 as new weapon:**
- Reddit v. Perplexity AI, SerpApi, Oxylabs, AWMProxy (Oct 2025): Reddit invoked DMCA anti-circumvention provisions, alleging defendants bypassed "technological measures" (rate limits, CAPTCHAs, SearchGuard) — a significant escalation beyond traditional CFAA claims
- Google v. SerpApi (Dec 2025): Google similarly used DMCA anti-circumvention against scraping of search results
- These cases are currently at the motion-to-dismiss stage (as of March 2026)

### 1.4 Recent Web Scraping Lawsuits and Outcomes (2024-2026)

| Case | Year | Outcome/Status | Key Holding |
|------|------|----------------|-------------|
| Meta v. Bright Data | 2024 | Bright Data prevailed | TOS cannot bind users who never logged in; public data is fair game |
| X Corp v. Bright Data | 2024 | Dismissed | TOS cannot prevent public data collection; X didn't own user content |
| Thomson Reuters v. Ross Intelligence | 2024 | Against scraper | First major ruling against scraping for AI training |
| Reddit v. Anthropic | 2025 | Active (discovery) | Breach of contract, unjust enrichment, trespass to chattels |
| Reddit v. Perplexity/SerpApi | 2025 | Active (MTD stage) | DMCA Section 1201 anti-circumvention claims |
| Google v. SerpApi | 2025 | Active (MTD stage) | DMCA anti-circumvention for search result scraping |

### 1.5 EU Data Scraping Regulations

**GDPR applies when scraping personal data of EU residents:**
- Web scraping operators are classified as "data controllers"
- Must have a lawful basis for processing (legitimate interest is most common)
- Must comply with transparency, data minimization, and storage limitation principles
- GDPR Article 14 requires informing individuals when their data is obtained indirectly
- Fines: up to 20 million EUR or 4% of annual global revenue

**Key EU developments:**
- The Dutch DPA takes an extremely restrictive stance: purely commercial interests *cannot* justify web scraping
- France's CNIL considers respecting robots.txt a factor in the legitimate interest balancing test
- November 2025: EC proposed recognizing AI system development as a "legitimate interest" under GDPR and creating a new legal basis for processing special category data for AI training
- The EU Data Act (applied September 2025) clarified that sui generis database rights do not apply to IoT-generated data

**Peptide-checker implication:** If serving EU users or scraping EU-based sources, avoid collecting personal data. Stick to factual product data (purity, potency, test results) which is less problematic than personal data.

---

## 2. Aggregating Public Test Data

### 2.1 Finnrick's Publicly Posted Results

**Can peptide-checker aggregate this data?** Likely yes, with important caveats.

Finnrick publishes all test results openly at finnrick.com/products. Their stated mission is to "provide the public with comprehensive information for making informed purchasing decisions." They have tested 5,982+ samples from 182+ vendors across 15 products.

**Legal analysis:**
- The underlying *facts* (purity percentages, potency measurements, HPLC results) are not copyrightable under US law (*Feist v. Rural Telephone*)
- Finnrick's *specific arrangement and presentation* may have thin copyright protection as a compilation
- Their *scoring methodology* (0-10 scale, A-E ratings) is their creative expression — do not replicate the exact scoring system
- **Safest approach:** Link to Finnrick results rather than scraping them. Reference specific data points with attribution. Do not reproduce their entire database structure.

**Finnrick data access:** Finnrick offers a "Full Data Access" researcher program — contact them for formal data-sharing terms. No public API was identified.

### 2.2 Janoshik Public COA Data

**Can it be referenced/linked?** Yes.

Janoshik maintains a public verification database at public.janoshik.com where anyone can look up test results by sample reference ID. Their business model inherently depends on public accessibility of results.

**Legal analysis:**
- Individual COA data points (purity %, molecular weight confirmation) are facts — not copyrightable
- Linking to public.janoshik.com results is clearly permissible
- Reproducing their COA documents wholesale could raise copyright concerns (the *presentation* is copyrightable)
- **Safest approach:** Link to Janoshik's public verification page. Extract and cite specific factual data points (e.g., "Janoshik HPLC analysis showed 99.2% purity, sample ref #12345") with clear attribution.

### 2.3 Reddit Community Test Reports

**Can these be aggregated?** Yes, with significant legal caveats in 2025-2026.

**Current legal landscape for Reddit data:**
- Reddit's API is free for non-commercial, non-competitive use
- Commercial use: $0.24 per 1,000 API calls
- Reddit is actively litigating against unauthorized scraping (v. Anthropic, v. Perplexity, v. SerpApi)
- Reddit's Responsible Builder Policy governs third-party data use

**Safest approaches for community reports:**
1. **User-submitted content:** Allow peptide-checker users to voluntarily submit their own test reports (protected by Section 230 as user-generated content)
2. **Links, not copies:** Link to Reddit threads rather than reproducing post content
3. **Summaries:** Summarize community sentiment without quoting specific posts at length
4. **Reddit API (paid):** For commercial aggregation, use the official Reddit API under their commercial terms

**Risk:** Direct scraping of Reddit at scale without API access is currently the subject of active litigation and should be avoided.

### 2.4 Fair Use for Factual Data vs. Copyrighted Expression

**Fundamental principle (Feist v. Rural Telephone, 1991):**
> Facts are not copyrightable. The intent of copyright law is to encourage creative expression, not to reward the effort of collecting information.

**What this means for peptide-checker:**

| Data Type | Copyrightable? | Can Aggregate? |
|-----------|---------------|----------------|
| Purity percentage (e.g., 99.2%) | No — factual data | Yes |
| Potency measurement (e.g., 9.8mg vs 10mg claimed) | No — factual data | Yes |
| HPLC chromatogram image | Yes — creative work | Link only; do not reproduce |
| Lab report PDF layout/design | Yes — creative expression | Link only; extract facts |
| Vendor rating score (e.g., Finnrick's "A" rating) | Possibly — creative methodology | Reference with attribution |
| Test methodology description | Yes — creative expression | Summarize; do not copy verbatim |
| Chemical structure data | No — factual data | Yes |
| Price data | No — factual data | Yes |

**Database compilation protection:** While individual facts cannot be copyrighted, a database's *selection, coordination, and arrangement* can receive thin copyright protection if sufficiently original. However, anyone can extract facts from a protected compilation and rearrange them independently.

### 2.5 EU Sui Generis Database Right

**Significant risk for EU-facing operations.**

Unlike the US, the EU provides legal protection for databases based purely on the *investment* in obtaining, verifying, and presenting data — regardless of creativity. This protection lasts 15 years and prevents extraction of a "substantial part" of a protected database.

**Implications for peptide-checker:**
- Extracting *individual data points* from EU-based databases is generally permissible
- Extracting a *substantial portion* of a database (or systematically extracting small portions that cumulatively constitute a substantial part) may violate the database right
- The EU Data Act (September 2025) exempted IoT-generated data from sui generis protection, but lab test data is not IoT data
- **Mitigation:** Do not wholesale copy EU-based testing databases. Extract individual facts. Build your own database structure.

---

## 3. Consumer Review Aggregation Precedents

### 3.1 How ConsumerLab Handles Vendor Data Legally

ConsumerLab.com provides the closest operational model to what peptide-checker aims to do. Key aspects of their legal structure:

**Independent purchasing:** ConsumerLab buys products from retail stores, catalogs, and online retailers — not from manufacturers directly. This maintains independence and avoids conflicts.

**Third-party testing:** Tests are contracted to independent laboratories, not performed in-house. This provides an additional layer of objectivity.

**Revenue model:** Combination of subscription fees (consumers), click-through affiliate fees, and paid testing programs for manufacturers ($3,000-$7,000 per product).

**Vendor pushback history:**
- CRN (Council for Responsible Nutrition) filed an FTC complaint against ConsumerLab's business practices
- ConsumerLab counter-sued CRN but ultimately dropped the lawsuit
- All but one of ConsumerLab's claims were dismissed; the final count was dismissed with prejudice
- FTC has reviewed ConsumerLab's practices and did not take enforcement action

**Key lesson:** ConsumerLab has survived 25+ years of vendor pushback without being successfully sued for defamation. Their defense rests on: (1) objective testing methodology, (2) independent lab verification, (3) factual reporting of test results, and (4) clear disclosure of methodology.

### 3.2 Review Aggregation Precedents

**Yelp/TripAdvisor/Glassdoor model:**
- These platforms are protected by CDA Section 230 for user-generated reviews
- They add their own editorial features (star ratings, "top picks") which are treated as protected opinion
- TripAdvisor's "Dirtiest Hotels" list based on user survey data received Section 230 protection

**Section 230 applicability to peptide-checker:**
- Section 230 protects platforms from liability for *user-generated content*
- If peptide-checker hosts user-submitted test reports and reviews, Section 230 applies
- If peptide-checker creates its own ratings and analysis, Section 230 does *not* apply — the site is the "information content provider"
- **Hybrid approach works:** Platform features (user reviews) get Section 230 protection; editorial content (staff-created ratings) relies on truth/opinion defenses

### 3.3 Section 230 Protections and Limitations

**What Section 230 protects:**
- Hosting user-generated reviews, test reports, and community discussions
- Moderating (removing) content without becoming liable for remaining content
- Displaying aggregated user ratings based on user submissions

**What Section 230 does NOT protect:**
- Content created or materially contributed to by the platform itself
- AI-generated content (evolving area — no clear precedent yet)
- Product recommendations that go beyond mere hosting

**Emerging risk:** Courts are increasingly questioning whether algorithmic curation and recommendation systems cross the line from "passive hosting" to "content creation."

---

## 4. Defamation and Vendor Litigation Risk

### 4.1 Opinion vs. Factual Statement Protection

**First Amendment protection hierarchy:**
1. **Pure opinion** ("I think this vendor is unreliable") — highest protection
2. **Opinion based on disclosed facts** ("Based on three failed purity tests, we rate this vendor poorly") — strong protection
3. **Mixed fact/opinion** ("This vendor sells impure products") — moderate protection, depends on context
4. **False statement of fact** ("This vendor adds filler chemicals") — no protection if false

**For peptide-checker:** Always anchor ratings in disclosed, verifiable methodology. "Based on 12 independent HPLC tests averaging 87.3% purity against a claimed 99%, this product received a D rating under our methodology" is far more defensible than "This vendor sells junk."

### 4.2 Fair Comment and Honest Opinion Defenses

**Fair comment** is a common law defense guaranteeing freedom to express statements on matters of public interest, provided:
- The comment is based on true facts
- The facts on which the comment is based are stated or known
- The comment represents the speaker's honest opinion
- The comment is not made with actual malice (ill will, spite, intent to harm)

**For peptide-checker:** Consumer safety in unregulated peptide markets is clearly a matter of public interest. Test results are factual. Ratings derived from transparent methodology represent honest opinion based on disclosed facts.

### 4.3 Anti-SLAPP Laws by State

Anti-SLAPP (Strategic Lawsuit Against Public Participation) laws provide early dismissal of meritless defamation suits and fee-shifting (the plaintiff pays the defendant's legal costs).

**Strong anti-SLAPP states (recommended for incorporation):**
- **California** — broadest protection; covers statements in public forums on public interest matters; mandatory fee-shifting
- **Texas** — strong protections with broad definition of public interest
- **Oregon** — comprehensive anti-SLAPP statute
- **Washington** — strong protections

**Weak or no anti-SLAPP states (avoid incorporating here):**
- Virginia — narrow statute, limited to specific categories
- Several states have no anti-SLAPP law at all

**Strategic consideration:** Incorporate peptide-checker in California or Texas to maximize anti-SLAPP protection. If a vendor files a SLAPP suit, the case can be dismissed early and the vendor pays attorney fees.

### 4.4 ConsumerLab's Defense Model

ConsumerLab's 25+ year survival provides a roadmap:
1. **Transparent methodology** — published testing criteria (identity, potency, purity, bioavailability, consistency)
2. **Independent labs** — testing contracted to third parties, not in-house
3. **Factual reporting** — results presented as data, not editorial opinion
4. **Arms-length purchasing** — products bought retail, not from manufacturers
5. **FTC review** — ConsumerLab proactively engaged with FTC review of its practices
6. **No gag clauses** — does not allow manufacturers to suppress unfavorable results (though paid testing programs do give manufacturers control over whether results are published)

### 4.5 What If a Vendor Sues Over a Low Rating?

**Defense toolkit:**
1. **Truth** — absolute defense. If the test data is accurate, the claim fails
2. **Fair comment/honest opinion** — rating based on disclosed methodology
3. **Anti-SLAPP motion** — early dismissal + fee-shifting in favorable jurisdictions
4. **Consumer Review Fairness Act (CRFA)** — federal law prohibiting businesses from penalizing honest reviews (applies more to user-generated content)
5. **Public interest defense** — consumer safety in unregulated markets
6. **Media liability insurance** — covers defense costs and settlements

**Practical risk assessment:** Defamation suits against testing/review organizations are rare and rarely succeed because:
- The plaintiff must prove *falsity* (difficult when you have lab results)
- The plaintiff must prove *actual malice* for public concern matters
- Anti-SLAPP laws make it expensive for plaintiffs to pursue frivolous claims
- The Streisand Effect deters most rational vendors from suing

---

## 5. API and Data Licensing

### 5.1 Finnrick

- **API:** No public API identified
- **Data access:** "Full Data Access" researcher program available — requires sign-up
- **Recommendation:** Contact Finnrick directly to negotiate data-sharing terms. They publish openly and may welcome integration with a consumer-safety tool. Formal partnership > scraping.

### 5.2 Janoshik Analytical

- **API:** No public API identified
- **Public data:** Verification database at public.janoshik.com is freely accessible
- **Data sharing:** No formal data-sharing agreement program found
- **Recommendation:** Link to public verification pages. For deeper integration, contact Janoshik to discuss partnership terms. Their business model benefits from wider visibility of their testing.

### 5.3 PubMed / NIH / NCBI

- **License:** Public domain (US government works). NCBI places *no restrictions* on use or distribution of its data
- **Automated access:** Rate-limited to 3 requests/second; larger batches restricted to off-peak hours
- **Attribution:** Requested but not required
- **Commercial use:** No blanket prohibition
- **Caveat:** Individual submitters may retain IP rights over specific submitted data
- **Recommendation:** Freely usable. Include attribution as courtesy. Respect rate limits.

### 5.4 ClinicalTrials.gov

- **License:** Public domain — US government database
- **API:** REST API available (v2) with structured access to all trial data
- **Commercial use:** Permitted
- **Recommendation:** Freely usable for any purpose. Reference trial NCT IDs for traceability.

### 5.5 ChEMBL (EMBL-EBI)

- **License:** Open access under Creative Commons Attribution-ShareAlike 3.0 Unported (CC BY-SA 3.0)
- **API:** Full REST API available with compound, target, bioactivity, mechanism, and ADMET data
- **Commercial use:** Permitted under CC BY-SA terms (must attribute and share derivative works under same license)
- **Recommendation:** Freely usable with attribution. If peptide-checker creates derivative datasets, they must be shared under CC BY-SA.

### 5.6 Data Source License Summary

| Source | License | API Available | Commercial Use | Attribution Required |
|--------|---------|---------------|----------------|---------------------|
| PubMed/NCBI | Public domain | Yes (E-utilities) | Yes | Requested, not required |
| ClinicalTrials.gov | Public domain | Yes (REST v2) | Yes | Recommended |
| ChEMBL | CC BY-SA 3.0 | Yes (REST) | Yes | Required |
| Finnrick | Proprietary (public display) | No | Contact for terms | Yes |
| Janoshik | Proprietary (public verification) | No | Contact for terms | Yes |
| Reddit | Proprietary | Yes (paid for commercial) | $0.24/1K calls | Per API terms |
| PubChem | Public domain | Yes (PUG REST) | Yes | Requested |

---

## 6. Best Practices for Peptide-Checker

### 6.1 How to Aggregate Data Legally

1. **Use official APIs first** — always prefer structured, authorized access
2. **Partner over scrape** — contact Finnrick/Janoshik for formal data-sharing agreements
3. **Link, don't copy** — reference external test results with links rather than reproducing full documents
4. **Extract facts, not expression** — purity percentages and potency data are facts; lab report layouts and scoring systems are expression
5. **Build your own database structure** — arrange aggregated facts in your own original schema
6. **Respect robots.txt** — check and honor robots.txt directives on all scraped sites
7. **Honor cease-and-desist notices** — if a source asks you to stop, stop immediately

### 6.2 Attribution Requirements

| Source Type | Attribution Method |
|-------------|-------------------|
| Public government data (NIH, ClinicalTrials.gov) | Courtesy citation; source and access date |
| CC-licensed data (ChEMBL) | Mandatory attribution per license terms |
| Third-party lab results (Finnrick, Janoshik) | Source name, link to original, date accessed |
| User-submitted community reports | Username (if consented) or anonymized |
| Scientific publications | Standard academic citation |

### 6.3 When to Scrape vs. API vs. Manual Entry

| Method | When to Use | Legal Risk |
|--------|-------------|------------|
| **Official API** | Source offers one (NIH, ChEMBL, ClinicalTrials.gov) | Lowest |
| **Partnership/license** | Source has valuable proprietary data (Finnrick, Janoshik) | Low |
| **Manual entry** | Small datasets, one-time collection, no API available | Low |
| **User submission** | Community test reports, personal experiences | Low (Section 230 protection) |
| **Scraping public pages** | No API, no partnership possible, publicly visible data | Moderate |
| **Scraping behind login** | Never | Highest — avoid entirely |

### 6.4 How to Structure Vendor Ratings to Minimize Legal Risk

**DO:**
- Base ratings entirely on objective, reproducible test data
- Publish your complete methodology (how scores are calculated)
- Disclose the number of samples tested and date ranges
- Use comparative language ("below average purity vs. category mean")
- Allow vendors to submit their own test data for inclusion
- Include a vendor response/dispute mechanism
- Clearly label ratings as "based on [methodology name]" not as absolute truth

**DO NOT:**
- Use conclusory language ("dangerous," "fraudulent," "scam") without strong factual support
- Rate vendors based on subjective criteria without disclosure
- Present opinion-based assessments as established fact
- Ignore vendor requests to correct factual errors
- Accept payment to alter ratings (destroys credibility and legal defenses)
- Make claims about vendor *intent* ("they knowingly sell impure products") without evidence

### 6.5 Insurance Coverage

**Media liability insurance** covers defamation claims, copyright infringement, and invasion of privacy.

- **Typical cost:** $78/month average ($936/year) for small operations; $1,200-$3,000/year for mid-sized
- **Coverage:** $500,000-$1,000,000 per claim; $1,000,000 aggregate
- **Covers:** Legal defense costs + damages for defamation, libel, trade libel claims
- **Providers:** Chubb, Insureon, Hiscox, Hartford
- **Recommendation:** Essential for peptide-checker. Budget $1,500-$2,500/year. This is the cost of doing business when publishing vendor ratings.

---

## 7. Data Pipeline Compliance Checklist

### 7.1 Safe to Use (Green Light)

- [ ] PubMed abstracts and metadata (public domain)
- [ ] ClinicalTrials.gov trial data (public domain)
- [ ] ChEMBL compound and bioactivity data (CC BY-SA 3.0)
- [ ] PubChem chemical data (public domain)
- [ ] FDA adverse event reports (public domain — FAERS)
- [ ] Published scientific literature (fair use for factual extraction)
- [ ] User-submitted test reports on your own platform (Section 230)
- [ ] Your own independently commissioned lab tests

### 7.2 Requires Permission or Formal Terms (Yellow Light)

- [ ] Finnrick test results — contact for data-sharing agreement
- [ ] Janoshik COA data — contact for partnership terms; linking is fine
- [ ] Reddit community reports — use official API ($0.24/1K calls for commercial)
- [ ] Vendor websites (product claims, pricing) — check TOS; factual data extraction likely fine
- [ ] Third-party lab reports — link to public pages; do not reproduce PDFs

### 7.3 Avoid Entirely (Red Light)

- [ ] Any data behind login walls without authorization
- [ ] Data obtained by circumventing CAPTCHAs, rate limits, or IP blocks
- [ ] Wholesale reproduction of third-party database structures
- [ ] Personal data of EU residents without GDPR compliance
- [ ] Content from platforms that have sent cease-and-desist notices
- [ ] Proprietary scoring methodologies (Finnrick's A-E system, etc.)
- [ ] Full-text reproduction of copyrighted lab reports or articles

### 7.4 Documentation and Audit Trail

Maintain records for every data source:

1. **Source registry** — document every data source, URL, access method, and legal basis
2. **TOS snapshots** — archive Terms of Service at time of data collection (they change)
3. **robots.txt logs** — record robots.txt directives at time of scraping
4. **Consent records** — for user-submitted data, record consent and terms accepted
5. **Attribution log** — track what attribution is required for each source
6. **Correspondence** — keep all communications with data sources (partnership requests, cease-and-desist notices, permission grants)
7. **Data provenance chain** — for each data point in your database, record: source, date collected, method of collection, any transformations applied
8. **Takedown log** — document any data removed at source request, when, and why

---

## Summary: Legal Risk Matrix for Peptide-Checker

| Activity | US Legal Risk | EU Legal Risk | Recommendation |
|----------|---------------|---------------|----------------|
| Publishing your own test results | Minimal | Minimal | Core activity — do this |
| Linking to Finnrick/Janoshik results | Minimal | Minimal | Do this freely |
| Extracting factual data points from public sources | Low | Moderate (database rights) | Extract facts, not structure |
| Hosting user-submitted reviews | Low (Section 230) | Moderate (GDPR for personal data) | Implement with proper terms |
| Scraping public vendor websites | Moderate | Moderate-High | Check TOS; prefer manual/API |
| Publishing vendor quality ratings | Moderate (defamation risk) | Moderate | Use methodology-based framework |
| Scraping Reddit at scale | High | High | Use official API or avoid |
| Reproducing full lab reports | High (copyright) | High | Link only; extract facts |
| Scraping behind logins | Very High (CFAA) | Very High | Never do this |

---

## Sources

- [hiQ Labs v. LinkedIn — Wikipedia](https://en.wikipedia.org/wiki/HiQ_Labs_v._LinkedIn)
- [Ninth Circuit Holds Data Scraping is Legal — California Lawyers Association](https://calawyers.org/privacy-law/ninth-circuit-holds-data-scraping-is-legal-in-hiq-v-linkedin/)
- [hiQ v. LinkedIn Wrapped Up — ZwillGen](https://www.zwillgen.com/alternative-data/hiq-v-linkedin-wrapped-up-web-scraping-lessons-learned/)
- [Is Web Scraping Legal? 2025 Breakdown — McCarthy Law Group](https://mccarthylg.com/is-web-scraping-legal-a-2025-breakdown-of-what-you-need-to-know/)
- [Is Web Scraping Legal? 2026 Laws & Best Practices — AIMultiple](https://aimultiple.com/is-web-scraping-legal)
- [Google Sues SerpApi — IPWatchdog](https://ipwatchdog.com/2025/12/26/google-sues-serpapi-parasitic-scraping-circumvention-protection-measures/)
- [Reddit's AI Scraping Lawsuit — Techdirt](https://www.techdirt.com/2025/10/24/reddits-ai-scraping-lawsuit-is-an-attack-on-the-open-internet/)
- [Anti-Circumvention: Reddit's Case Against Perplexity — Lexology](https://www.lexology.com/library/detail.aspx?g=bd5431bd-5f54-49a6-b87f-ceb0337f407a)
- [The State of Web Scraping in the EU — IAPP](https://iapp.org/news/a/the-state-of-web-scraping-in-the-eu)
- [AI's Legal Frontier: Europe's Privacy Regulators on Scraping — Zyte](https://www.zyte.com/blog/ai-personal-data-scraping-europe-guidance/)
- [EU Copyright Law: Protection of Databases — EC Digital Strategy](https://digital-strategy.ec.europa.eu/en/policies/protection-databases)
- [Feist Publications v. Rural Telephone — Justia](https://supreme.justia.com/cases/federal/us/499/340/)
- [Copyright for Data — Emory Libraries](https://libraries.emory.edu/research/copyright/copyright-data)
- [Consumer Review Fairness Act — FTC](https://www.ftc.gov/business-guidance/resources/consumer-review-fairness-act-what-businesses-need-know)
- [ConsumerLab FTC Review — FTC Legal Library](https://www.ftc.gov/legal-library/browse/cases-proceedings/staff-letters/consumerlabcom-llc-its-product-review-voluntary-certification-programs-testing-dietary-supplements)
- [ConsumerLab — Wikipedia](https://en.wikipedia.org/wiki/ConsumerLab.com)
- [Section 230 Overview — EFF](https://www.eff.org/issues/cda230)
- [Section 230: An Overview — Congressional Research Service](https://www.congress.gov/crs-product/R46751)
- [Fair Comment — Legal Information Institute](https://www.law.cornell.edu/wex/fair_comment)
- [California Anti-SLAPP Laws — KLW Law](https://www.klw-law.com/california-anti-slapp-laws)
- [Consumer Review Fairness Act — Public Participation Project](https://anti-slapp.org/consumer-review-fairness-act)
- [Finnrick Testing Methodology](https://www.finnrick.com/about/testing-methodology)
- [Janoshik Public Tests](https://public.janoshik.com/)
- [NCBI Website and Data Usage Policies](https://www.ncbi.nlm.nih.gov/home/about/policies/)
- [Media Liability Insurance Cost — Insureon](https://www.insureon.com/media-business-insurance/cost)
- [Media Liability Insurance 2025 — Hotaling Insurance](https://hotalinginsurance.com/hotaling-insurance-blog/media-liability-insurance-what-it-is-and-is-it-worth-it-in-2025)
- [Posting Product Reviews Legal Guide — Romano Law](https://www.romanolaw.com/content-creator-beware-what-you-need-to-know-about-posting-product-reviews/)
