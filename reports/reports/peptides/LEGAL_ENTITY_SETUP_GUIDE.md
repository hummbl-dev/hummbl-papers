# Peptide Checker: Legal Entity Setup Guide

**Date:** 2026-03-24
**Author:** Reuben Bowlby / HUMMBL
**Classification:** Internal Strategic Document
**Cross-references:** PEPTIDE_CHECKER_BUSINESS_PLAN.md, peptide_regulation_landscape_2026.md

---

## Table of Contents

1. [LLC Formation](#1-llc-formation)
2. [Business Banking](#2-business-banking)
3. [Insurance](#3-insurance)
4. [Terms of Service](#4-terms-of-service)
5. [Privacy Policy](#5-privacy-policy)
6. [Intellectual Property](#6-intellectual-property)
7. [Tax Setup](#7-tax-setup)
8. [Compliance Checklist](#8-compliance-checklist)
9. [Cost Summary](#9-cost-summary)

---

## 1. LLC Formation

### 1.1 Best State: Wyoming vs. Delaware vs. Home State

For a solo-founder online health information platform, the decision tree is straightforward:

| Factor | Wyoming | Delaware | Home State |
|--------|---------|----------|------------|
| **Filing fee** | $100 | $90 | Varies ($50-$500) |
| **Annual report** | $60/year | $300+/year | Varies ($0-$800) |
| **State income tax** | None | None on out-of-state income | Varies |
| **Privacy** | Strong (no public member disclosure) | Moderate | Varies |
| **Legal system** | Standard | Court of Chancery (VC-friendly) | Standard |
| **Registered agent** | Required ($100-$300/year) | Required ($100-$300/year) | Can self-serve |
| **Foreign registration needed?** | Yes, if you live elsewhere | Yes, if you live elsewhere | No |

**Recommendation: Wyoming LLC.**

Rationale for Peptide Checker specifically:
- **No venture capital planned** (solo founder, bootstrapped) -- eliminates the main reason to choose Delaware
- **Online-only business** with no physical storefront -- no need for home-state registration if you avoid creating nexus (though this is a gray area if you work from home)
- **Lowest ongoing costs** -- $100 formation + $60/year renewal vs. Delaware's $300+/year
- **Strong privacy protections** -- important for a platform that may attract attention from peptide vendors or supplement industry litigants
- **No state income tax** -- pass-through income taxed only at federal level and your resident state level
- **Instant online filing** -- can be operational same day

**Caveat:** If you physically operate from a home office in another state, that state may require you to register as a foreign LLC there. This adds $50-$300 in fees plus an additional annual report. Consult a tax professional about your specific situation. Many solo online businesses form in Wyoming without foreign-registering in their home state, but this carries some risk.

### 1.2 Formation Cost Breakdown (Wyoming)

| Item | Cost | Frequency |
|------|------|-----------|
| Articles of Organization filing | $100 | One-time |
| Registered agent service | $100-$300 | Annual |
| Operating agreement (self-drafted from template) | $0 | One-time |
| EIN application (IRS) | $0 | One-time |
| **Total Year 1** | **$200-$400** | |
| **Ongoing annual cost** | **$160-$360** | (annual report + registered agent) |

### 1.3 Single-Member LLC Tax Treatment

A single-member LLC is a **"disregarded entity"** for federal income tax purposes:

- **No separate business tax return** -- all income and expenses flow through to your personal Form 1040, Schedule C
- **Self-employment tax** -- you pay both the employer and employee portions of Social Security and Medicare (15.3% on net earnings up to the Social Security wage base, then 2.9% above that)
- **Qualified Business Income (QBI) deduction** -- you may deduct up to 20% of qualified business income under Section 199A, subject to income limitations
- **No double taxation** -- unlike a C-corp, profits are taxed once
- **Optional S-corp election** -- once revenue exceeds ~$40-50K net profit, electing S-corp treatment (Form 2553) can reduce self-employment taxes by paying yourself a "reasonable salary" and taking remaining profit as distributions. Consult a CPA when you reach this threshold.

### 1.4 Operating Agreement Essentials

Even though Wyoming does not legally require an operating agreement, you **must have one** to:
- Establish the LLC as a separate legal entity (critical for liability protection)
- Define your management authority as sole member
- Document capital contributions
- Set rules for adding future members (if ever)
- Establish dissolution procedures

**Key clauses for a solo-founder operating agreement:**

1. **Formation details** -- LLC name, state, date of formation, registered agent
2. **Purpose** -- "To operate an online health information and verification platform and related services"
3. **Member information** -- Your name, ownership percentage (100%), capital contribution
4. **Management structure** -- Member-managed (you make all decisions)
5. **Capital contributions** -- Initial contribution amount and rules for additional contributions
6. **Distributions** -- How and when profits are distributed to you
7. **Banking authority** -- Who can open accounts and sign checks
8. **Tax elections** -- Default disregarded entity treatment (or future S-corp election)
9. **Transfer restrictions** -- Conditions under which membership interest can be transferred
10. **Dissolution** -- Under what circumstances the LLC dissolves and how assets are distributed
11. **Indemnification** -- Protection for you as manager acting in good faith

**Template resources:**
- Northwest Registered Agent (free template included with registered agent service)
- eForms.com (free, updated February 2026)
- LegalNature.com (guided template, ~$35)
- LawDepot.com (free basic template)

### 1.5 EIN Application

An Employer Identification Number (EIN) is your business's tax ID. Even though a single-member LLC without employees technically does not require one, **you need an EIN** because:
- Banks require it to open a business account
- Payment processors (Stripe) require it
- It avoids giving your SSN to vendors and partners
- It is needed if you ever hire employees or contractors

**How to apply:**
1. Go to [IRS EIN Online Application](https://www.irs.gov/businesses/small-businesses-self-employed/apply-for-an-employer-identification-number-ein-online)
2. Select "Limited Liability Company" as entity type
3. Select "1" member
4. Complete the online form (takes ~10 minutes)
5. **Receive your EIN immediately** -- print the confirmation letter

**Cost:** Free (never pay a service to do this)
**Timeline:** Instant online, or 4 weeks by mail (Form SS-4)

### 1.6 Formation Timeline

| Step | Time Required | Running Total |
|------|---------------|---------------|
| Choose registered agent service | 30 minutes | 30 min |
| File Articles of Organization online (Wyoming) | 15 minutes | 45 min |
| Receive approval | Instant (online filing) | 45 min |
| Apply for EIN online | 10 minutes | 55 min |
| Draft operating agreement | 1-2 hours | ~2-3 hours |
| Open business bank account | 10-30 minutes (online) | ~3 hours |
| **Total: Same day** | | **~3 hours of active work** |

---

## 2. Business Banking

### 2.1 Bank Comparison

| Feature | Mercury | Relay | Novo | Chase Business |
|---------|---------|-------|------|----------------|
| **Monthly fee** | $0 | $0 | $0 | $15 (waivable) |
| **FDIC insurance** | $5M (sweep) | $3M (sweep) | $250K | $250K |
| **Savings APY** | 4.0%+ | 0.91% | 1.10% | 0.01% |
| **ACH transfers** | Free | Free | Free | Free |
| **Wires** | Free incoming | Free incoming | Free incoming | $15-$30 |
| **Debit card** | Yes | Yes | Yes | Yes |
| **Integrations** | Stripe, QBO, Xero | QBO, Xero, Gusto | QBO, Xero, Stripe | Limited |
| **Approval speed** | ~10 minutes | Same day | Same day | In-person visit |
| **Best for** | Tech founders | Budget-conscious | Solo founders | Need physical branch |

**Recommendation: Mercury.**

Rationale:
- Designed for tech founders and startups
- Highest FDIC coverage ($5M through partner bank sweep)
- Competitive savings APY
- Clean API and Stripe integration
- Approves in ~10 minutes with just EIN and Articles of Organization
- No minimum balance
- Treasury feature for idle cash

**Alternative:** Relay is excellent if you want multiple "buckets" for organizing money (e.g., separate virtual accounts for taxes, operating expenses, and profit).

### 2.2 Separating Personal and Business Finances

This is **non-negotiable** for LLC liability protection. Commingling funds is the fastest way to "pierce the corporate veil" and lose personal liability protection.

**Rules:**
- All business income goes into the business account
- All business expenses come from the business account
- Pay yourself via "owner's draw" (transfer from business to personal)
- Never use your personal card for business expenses (or if you must, reimburse immediately with documentation)
- Keep a paper trail for every transfer between personal and business accounts

### 2.3 Payment Processing (Stripe)

**Setup requirements:**
- Business name and EIN
- Business bank account (for deposits)
- Business address
- Personal SSN (for identity verification as beneficial owner)
- Business website URL

**Stripe pricing (2026):**

| Transaction Type | Fee |
|------------------|-----|
| Online card payments (domestic) | 2.9% + $0.30 |
| International cards | +1.5% |
| Currency conversion | +1.0% |
| ACH debit | 0.8% (capped at $5) |
| Recurring billing (Stripe Billing) | +0.7% per invoice |
| Chargebacks | $15 per dispute |
| Monthly/annual fee | $0 |

**For a $19.99/month subscription:**
- Card processing: $0.58 + $0.30 = $0.88
- Stripe Billing surcharge: $0.14
- **Total per transaction: ~$1.02 (5.1% effective rate)**

**For a $149/year subscription:**
- Card processing: $4.32 + $0.30 = $4.62
- Stripe Billing surcharge: $1.04
- **Total per transaction: ~$5.66 (3.8% effective rate)**

Annual billing yields a better effective rate. Consider offering both monthly and annual options with a discount for annual.

**Stripe Tax:** Stripe offers an automated sales tax calculation and collection add-on (0.5% per transaction) that handles multi-state compliance. Worth considering once you have customers in taxable states.

---

## 3. Insurance

### 3.1 Insurance Requirements for a Health Information Platform

Peptide Checker faces a **unique risk profile**: it provides information about health-related substances where misinformation could lead to consumer harm. This is not practicing medicine, but it is close enough to the line that proper insurance is critical.

### 3.2 Coverage Types and Estimated Costs

| Coverage Type | What It Covers | Est. Annual Cost | Priority |
|---------------|----------------|------------------|----------|
| **E&O / Professional Liability** | Claims that your information was wrong, incomplete, or misleading and caused harm | $700-$1,500 | CRITICAL |
| **Cyber Liability** | Data breaches, hacking, ransomware, notification costs | $500-$2,000 | HIGH |
| **General Liability** | Bodily injury, property damage, advertising injury | $400-$750 | MEDIUM |
| **Media Liability** (often bundled with E&O) | Defamation, copyright infringement in content | Included in E&O | HIGH |
| **Total estimated** | | **$1,600-$4,250/year** | |

### 3.3 What Specifically to Insure Against

**E&O / Professional Liability scenarios:**
- A user relies on your vendor rating to purchase peptides that turn out to be contaminated, and suffers adverse health effects
- Your COA verification tool incorrectly validates a fraudulent certificate
- Your regulatory status tracker shows a peptide as "legal" in a state where it is not
- A vendor sues claiming your rating is defamatory and caused business harm (media liability)
- Your content is cited in a lawsuit as having contributed to a consumer's decision to use an unapproved substance

**Cyber Liability scenarios:**
- Data breach exposing user email addresses, search histories, or health-adjacent browsing data
- MHMDA violation (consumer health data exposure) -- which carries a private right of action
- Ransomware attack on your infrastructure
- Third-party API breach affecting user data

**General Liability scenarios:**
- Less critical for an online-only business, but covers slip-and-fall at any in-person events, advertising injury claims, and provides a baseline of coverage many contracts require

### 3.4 Recommended Providers

| Provider | Best For | Notes |
|----------|----------|-------|
| **Hiscox** | E&O + General Liability bundle | Strong with small tech/info businesses; online quotes |
| **Hartford** | General liability | Low-cost starting at ~$17/month; A+ rated |
| **Coalition** | Cyber liability | Tech-focused; active risk monitoring included |
| **NEXT Insurance** | E&O from $19/month | Fast online quotes; good for startups |
| **Vouch** | Tech startup bundle | Designed for startups; combines E&O + Cyber + GL |
| **Insureon** | Comparison shopping | Broker that quotes from multiple carriers |

**Recommendation:** Start with **Hiscox or Vouch** for a bundled E&O + General Liability policy, then add a standalone **Coalition** cyber policy. Get quotes from Insureon to compare.

### 3.5 When to Get Insurance

- **Before public launch.** Do not go live without E&O coverage.
- Cyber liability can be added once you are collecting user data (even email addresses count).
- General liability can wait until you have revenue, but is inexpensive enough to bundle from day one.

---

## 4. Terms of Service

### 4.1 Key Clauses for a Health Information Platform

Your Terms of Service (ToS) must address the unique risks of operating a platform that provides health-related information without being a healthcare provider.

#### 4.1.1 Medical Disclaimer (CRITICAL)

This is the single most important legal protection on your site. It must be:
- Prominently displayed (not buried in fine print)
- Present on every page with health information (footer link at minimum)
- Acknowledged during account creation

**Essential language elements:**

```
MEDICAL DISCLAIMER

The information provided by Peptide Checker is for educational and
informational purposes only. It is NOT intended as a substitute for
professional medical advice, diagnosis, or treatment.

Peptide Checker does NOT:
- Recommend, endorse, or prescribe any peptide, supplement, or medication
- Provide medical advice or clinical guidance
- Diagnose or treat any medical condition
- Guarantee the safety, efficacy, or legality of any product

Peptide Checker DOES:
- Aggregate publicly available research and testing data
- Report on regulatory status from official government sources
- Provide tools for consumers to evaluate third-party test results
- Track vendor quality metrics based on verifiable data

Always consult a licensed healthcare provider before using any peptide
or supplement. If you are experiencing a medical emergency, call 911 or
your local emergency number immediately.

By using this platform, you acknowledge that you have read and understood
this disclaimer and that you use all information at your own risk.
```

#### 4.1.2 Limitation of Liability

```
TO THE MAXIMUM EXTENT PERMITTED BY LAW, PEPTIDE CHECKER AND ITS
OFFICERS, DIRECTORS, EMPLOYEES, AND AGENTS SHALL NOT BE LIABLE FOR
ANY INDIRECT, INCIDENTAL, SPECIAL, CONSEQUENTIAL, OR PUNITIVE
DAMAGES ARISING FROM:

(a) Your use of or inability to use the platform
(b) Any errors or omissions in platform content
(c) Any action taken based on information provided by the platform
(d) Any third-party products or services evaluated on the platform
(e) Unauthorized access to your data

IN NO EVENT SHALL OUR TOTAL LIABILITY EXCEED THE AMOUNT YOU PAID
TO US IN THE TWELVE (12) MONTHS PRECEDING THE CLAIM.
```

#### 4.1.3 User-Generated Content (COA Submissions)

If consumers submit COAs for verification:
- Users grant you a license to display, analyze, and store submitted documents
- Users represent they have the right to submit the content
- You are not responsible for the accuracy of user-submitted COAs
- You may remove any submission at your discretion
- Submitted COAs may be used in aggregate (anonymized) for platform ratings
- Users retain ownership of their submissions

#### 4.1.4 Arbitration Clause

```
BINDING ARBITRATION AND CLASS ACTION WAIVER

Any dispute arising from these Terms shall be resolved through binding
arbitration administered by the American Arbitration Association (AAA)
under its Consumer Arbitration Rules.

- Arbitration shall be conducted by a single arbitrator
- Location: [Your state] or by video conference
- Each party bears its own costs; AAA fees split per AAA rules
- The arbitrator's decision is final and binding

CLASS ACTION WAIVER: You agree to resolve disputes individually and
waive any right to participate in a class action lawsuit or class-wide
arbitration.

OPT-OUT: You may opt out of this arbitration agreement by sending
written notice within 30 days of creating your account.
```

**Note:** Some states (notably California) have restrictions on mandatory arbitration. Consult an attorney to ensure your arbitration clause is enforceable in key jurisdictions.

#### 4.1.5 Additional Key Clauses

- **Acceptable use policy** -- prohibit using the platform to facilitate illegal drug purchases, circumvent regulations, or harass vendors
- **Vendor rating methodology disclosure** -- transparency about how ratings are calculated (reduces defamation risk)
- **Intellectual property** -- your content, ratings, and analyses are copyrighted; users may not scrape or republish without permission
- **Termination** -- you may terminate accounts for ToS violations
- **Modification** -- you may update ToS with notice; continued use constitutes acceptance
- **Governing law** -- specify Wyoming law (or your home state)
- **Severability** -- if one clause is unenforceable, the rest survive

### 4.2 Template Resources and Services

| Resource | Cost | Notes |
|----------|------|-------|
| **Termly.io** | Free basic / $15/month premium | Generates ToS, privacy policy, disclaimers; CCPA/GDPR templates |
| **TermsFeed** | $15-$50 one-time | Medical disclaimer templates included |
| **Rocket Lawyer** | $39.99/month | Attorney-reviewed templates; on-call legal Q&A |
| **LegalZoom** | $79+ one-time | Custom ToS generation |
| **Actual attorney review** | $500-$2,000 | **Strongly recommended** for a health information platform |

**Recommendation:** Draft using Termly.io or TermsFeed, then pay an attorney ($500-$1,500) to review and customize for your specific health information use case. The health information angle makes generic templates insufficient on their own.

---

## 5. Privacy Policy

### 5.1 Why This Matters More Than Most Startups

Peptide Checker collects **consumer health data** by definition. Users searching for peptide safety information, submitting COAs, and viewing regulatory status pages are generating health-adjacent data. This triggers:

1. **MHMDA (Washington My Health My Data Act)** -- the strictest US health data privacy law
2. **CCPA/CPRA (California)** -- broad consumer privacy requirements
3. **General privacy expectations** -- even without state-specific laws, users expect health browsing data to be protected

### 5.2 MHMDA Compliance (Washington State)

The MHMDA applies to **any entity** that collects consumer health data from Washington residents, regardless of where the business is located. There is **no minimum revenue or user threshold**.

**Key requirements:**

| Requirement | What You Must Do |
|-------------|------------------|
| **Standalone health data privacy policy** | Create a SEPARATE policy (not combined with general privacy policy) that covers only consumer health data |
| **No marketing language** | The health data policy must be purely informational -- no promotional content |
| **Category disclosure** | List every category of consumer health data you collect |
| **Third-party disclosure** | Name specific third parties and affiliates that receive health data |
| **Consent before collection** | Obtain affirmative consent before collecting any consumer health data |
| **Separate consent for sharing** | Get additional consent before sharing health data with third parties |
| **Written authorization to sell** | Selling health data requires a signed consumer authorization (effectively a ban for most businesses) |
| **Consumer rights** | Provide access, deletion, and consent withdrawal; respond within 45 days |
| **Data security program** | Administrative, technical, and physical safeguards |
| **Private right of action** | Consumers can sue you directly for violations -- no need to wait for AG enforcement |

**What counts as "consumer health data" for Peptide Checker:**
- Search queries for specific peptides (reveals health interests/conditions)
- COA submissions (reveals what substances a user is purchasing)
- Saved peptides or watchlists
- Vendor browsing history on your platform
- Any data that could identify a consumer's health condition, status, or treatment

**Critical note:** The private right of action makes MHMDA violations extremely dangerous for small companies. A single class action could be existential. Take this seriously from day one.

### 5.3 CCPA/CPRA Compliance (California)

The CCPA applies if you meet any of these thresholds:
- Annual gross revenue > $25 million, OR
- Buy, sell, or share personal information of 100,000+ consumers, OR
- Derive 50% or more of revenue from selling/sharing personal information

**You likely will not meet these thresholds at launch**, but you should build CCPA-compliant practices from the start because:
- California users will expect it
- The thresholds can be reached faster than expected
- It is easier to build compliant from day one than retrofit later

**2026 CCPA updates to note:**
- Neural data is now classified as sensitive personal information
- Risk assessments required for data practices posing significant privacy risks
- Geofencing restrictions near healthcare facilities (relevant if you ever have a mobile app)
- Businesses collecting data from anyone under 16 -- that data is automatically classified as sensitive

### 5.4 Data Peptide Checker Collects and How to Handle It

| Data Type | Collection Method | Sensitivity | Retention Policy |
|-----------|-------------------|-------------|------------------|
| Email address | Account registration | Standard PII | Until account deletion + 30 days |
| Search queries | Platform usage | **Health data (MHMDA)** | Anonymize after 90 days; delete after 1 year |
| COA submissions | User upload | **Health data (MHMDA)** | Until user requests deletion; anonymized data retained for ratings |
| Peptide watchlists | User-created | **Health data (MHMDA)** | Until account deletion |
| Browsing history on platform | Analytics | **Health data (MHMDA)** | Anonymize after 30 days |
| Payment information | Stripe (you never store this) | Financial PII | Handled entirely by Stripe |
| IP address | Server logs | Standard PII | Anonymize after 7 days |
| Device/browser info | Analytics | Standard | Anonymize after 30 days |

### 5.5 Cookie Policy

If using analytics (e.g., Plausible, PostHog, Google Analytics):

| Cookie Type | Examples | Consent Required? |
|-------------|----------|-------------------|
| Strictly necessary | Session cookies, CSRF tokens | No |
| Analytics | Plausible, GA4, PostHog | Yes (MHMDA, CCPA) |
| Marketing | Facebook Pixel, Google Ads | Yes (explicit) |
| Preferences | Theme, language | No |

**Recommendation:** Use **Plausible Analytics** (privacy-focused, no cookies, GDPR/CCPA compliant by default, $9/month). This eliminates the need for cookie consent banners entirely for analytics purposes.

### 5.6 Data Retention and Deletion

**Retention schedule:**
- Active accounts: data retained while account is active
- Inactive accounts (no login for 2 years): send retention notice, delete after 30 days if no response
- Deletion requests: complete within 45 days (MHMDA) or 45 days (CCPA)
- Anonymized/aggregated data: may be retained indefinitely (for vendor ratings)
- Server logs: rotate and purge after 90 days
- Backups: purge personal data from backups within 6 months of deletion request

**Deletion process:**
1. User submits deletion request (in-app or email)
2. Verify identity
3. Delete personal data from production systems within 30 days
4. Delete from backups within 6 months
5. Confirm deletion to user
6. Retain anonymized/aggregated data only

---

## 6. Intellectual Property

### 6.1 Trademark: "Peptide Checker"

**Step 1: Preliminary search**
Before filing, search the USPTO Trademark Electronic Search System (TESS) for existing registrations:
- Search "peptide checker" as an exact phrase
- Search "peptide" in Class 42 (computer services) and Class 44 (medical information)
- Search phonetic equivalents and similar marks
- Also search state trademark databases and common-law usage (Google, domain registrations)

**Step 2: File application**
- File through the [USPTO Trademark Center](https://www.uspto.gov/trademarks) (replaced the old TEAS system in late 2025)
- Identity verification via ID.me required
- **Filing basis:** "Intent to Use" (1(b)) if not yet launched, or "Use in Commerce" (1(a)) if already operating
- **Class:** International Class 42 (Software as a Service; providing online non-downloadable software for health information verification) and/or Class 44 (Providing health information)
- **Filing fee:** $350 per class

**Step 3: Timeline**

| Phase | Expected Duration |
|-------|-------------------|
| Application filed | Day 1 |
| Initial examination by USPTO examiner | 8-10 months |
| Publication for opposition (30 days) | ~Month 10-12 |
| Registration (if no opposition) | ~Month 12-18 |
| **Total** | **12-18 months** |

**Step 4: Maintenance**
- Declaration of Use (Section 8): Between 5th and 6th year after registration
- Renewal (Section 9): Every 10 years ($650 per class)

**Estimated total cost:**
- Filing: $350-$700 (1-2 classes)
- Attorney assistance (recommended): $500-$1,500
- **Total: $850-$2,200**

### 6.2 Domain Strategy

| Domain | Priority | Est. Cost | Notes |
|--------|----------|-----------|-------|
| **peptidechecker.com** | Must-have | $10-$15/year (if available) or $500-$5,000 (if parked) | Check availability immediately |
| **peptide-checker.com** | High | $10-$15/year | Hyphenated alternative |
| **peptidechecker.io** | Medium | $30-$50/year | Tech-credibility signal |
| **peptidechecker.org** | Medium | $10-$15/year | Suggests nonprofit/public-interest angle |
| **peptidechecker.health** | Nice-to-have | $50-$70/year | Industry-specific TLD |
| **checkpeptides.com** | Backup | $10-$15/year | Alternative branding |

**Action items:**
1. Search domain availability on Namecheap or Cloudflare Registrar immediately
2. Register all affordable variants of your chosen name to prevent squatting
3. Point secondary domains to primary via 301 redirects
4. Use Cloudflare Registrar for at-cost domain pricing

### 6.3 Copyright

Your original content is automatically copyrighted upon creation:
- Research reports and analyses
- Vendor rating methodology documentation
- Educational content and guides
- Platform UI/UX design
- Marketing materials

**Optional:** Register key works with the US Copyright Office ($65 per online registration) for enhanced statutory damages in infringement cases. Low priority unless someone is actively copying your content.

### 6.4 Open Source Licensing

If you open-source any part of the codebase:

| License | Use Case | Implications |
|---------|----------|--------------|
| **MIT** | Utility libraries, tools | Maximum adoption; no copyleft |
| **Apache 2.0** | Larger projects | Patent protection included |
| **AGPL-3.0** | Core platform (if open-sourcing) | Requires derivative works to be open-sourced, including SaaS usage |
| **Proprietary** | Verification algorithms, rating models | Default -- no license means all rights reserved |

**Recommendation:** Keep the core verification logic, rating algorithms, and data models proprietary. If releasing utility tools or client libraries, use MIT or Apache 2.0.

---

## 7. Tax Setup

### 7.1 Quarterly Estimated Tax Payments

As a single-member LLC owner, you must make quarterly estimated payments if you expect to owe $1,000+ in tax for the year.

**2026 due dates:**

| Quarter | Period Covered | Due Date |
|---------|---------------|----------|
| Q1 | January - March | April 15, 2026 |
| Q2 | April - May | June 15, 2026 |
| Q3 | June - August | September 15, 2026 |
| Q4 | September - December | January 15, 2027 |

**How to calculate:**
1. Estimate total annual net business income
2. Subtract standard/itemized deductions
3. Apply tax rates (federal + state if applicable)
4. Add self-employment tax (15.3% on net earnings)
5. Subtract any withholding from other income sources
6. Divide by 4

**Safe harbor:** Pay at least 100% of last year's total tax liability (110% if AGI > $150K) to avoid underpayment penalties, even if you owe more at filing time.

**Payment method:** IRS Direct Pay (irs.gov/payments) or EFTPS (Electronic Federal Tax Payment System)

### 7.2 Business Expense Deductions

All "ordinary and necessary" business expenses are deductible on Schedule C:

| Expense Category | Examples | Est. Annual Cost | Deductible? |
|------------------|----------|------------------|-------------|
| **API costs** | OpenAI/Anthropic API, data feeds | $1,200-$6,000 | Yes, 100% |
| **Hosting/infrastructure** | Vercel, AWS, Cloudflare | $600-$2,400 | Yes, 100% |
| **Domain names** | peptidechecker.com, etc. | $50-$200 | Yes, 100% |
| **Insurance** | E&O, cyber, GL | $1,600-$4,250 | Yes, 100% |
| **Software/tools** | GitHub, Stripe, analytics, design tools | $500-$2,000 | Yes, 100% |
| **Home office** | Dedicated workspace percentage of rent/mortgage, utilities | Varies | Yes (simplified: $5/sq ft, max 300 sq ft = $1,500) |
| **Internet** | Business percentage of home internet | $300-$600 | Yes, business % |
| **Phone** | Business percentage | $200-$500 | Yes, business % |
| **Legal fees** | Attorney review, trademark filing | $1,000-$3,000 | Yes, 100% |
| **Accounting** | CPA or software | $0-$500 | Yes, 100% |
| **Education/research** | Industry conferences, publications | $200-$1,000 | Yes, if business-related |
| **Marketing** | SEO tools, content, ads | $500-$3,000 | Yes, 100% |
| **Registered agent** | Wyoming annual fee | $100-$300 | Yes, 100% |

### 7.3 Sales Tax on Digital Subscriptions

As of 2026, SaaS/digital subscription taxability varies by state:

**Taxable states (full rate):** Texas (80% of charges), New York, Pennsylvania, Washington, Ohio, Massachusetts, South Carolina, Hawaii, Connecticut, and others (25 states tax some form of SaaS)

**Non-taxable states:** California, Virginia, Florida, Missouri, and others

**When you need to collect sales tax:**
- When you have **economic nexus** in a state (typically $100K+ in sales or 200+ transactions)
- You likely will not have nexus anywhere in Year 1
- Monitor thresholds as revenue grows

**Recommendation:** Do not worry about sales tax until you approach $50K+ annual revenue. At that point, use **Stripe Tax** (0.5% per transaction, automated) or **TaxJar** ($19/month starting) to handle multi-state compliance.

### 7.4 Accounting Software

| Software | Cost | Best For |
|----------|------|----------|
| **Wave** | Free | Solo founders with simple needs; unlimited invoices and transactions |
| **QuickBooks Solopreneur** | $20/month | More features; better tax preparation integration |
| **QuickBooks Simple Start** | $38/month | If you need more robust reporting |
| **Xero** | $15/month | If you prefer Xero's interface; strong bank feed integration |

**Recommendation: Wave (free)** for Year 1. It handles income/expense tracking, invoicing, and basic tax reporting. Switch to QuickBooks when you need payroll, inventory, or more sophisticated reporting. Wave has no transaction limits and generates the reports you need for Schedule C filing.

---

## 8. Compliance Checklist

### 8.1 Day 1 Requirements (Before Any Public Presence)

- [ ] **Form LLC** -- File Articles of Organization in Wyoming
- [ ] **Get EIN** -- Apply online at IRS.gov
- [ ] **Draft operating agreement** -- Use template, customize for your business
- [ ] **Open business bank account** -- Mercury or Relay
- [ ] **Medical disclaimer** -- Draft and position prominently on all pages
- [ ] **Terms of Service** -- Draft initial version (even in beta)
- [ ] **Privacy policy** -- Draft initial version covering data collection practices
- [ ] **MHMDA standalone health data policy** -- Separate from general privacy policy
- [ ] **Separate business and personal finances** -- All business transactions through business account only

### 8.2 Week 1 Requirements (Before Accepting Users)

- [ ] **E&O insurance** -- Obtain professional liability coverage before public launch
- [ ] **Stripe account** -- Set up with business EIN and bank account
- [ ] **Cookie/analytics consent** -- Implement consent mechanism (or use Plausible to avoid cookies)
- [ ] **Data collection consent flow** -- Implement MHMDA-compliant consent before collecting health data
- [ ] **Contact information** -- Publish business contact email for legal/privacy inquiries
- [ ] **DMCA designated agent** -- Register with US Copyright Office if hosting user-submitted content ($6)

### 8.3 Month 1 Requirements (First 30 Days of Operation)

- [ ] **Cyber liability insurance** -- Add once collecting user data
- [ ] **General liability insurance** -- Bundle with E&O if affordable
- [ ] **Trademark search** -- Conduct preliminary search on USPTO TESS
- [ ] **File trademark application** -- If search is clear, file Intent to Use application ($350/class)
- [ ] **Set up accounting** -- Wave or QuickBooks; connect bank account; categorize expenses
- [ ] **Establish data deletion process** -- Document procedure for handling MHMDA/CCPA requests
- [ ] **Review vendor rating methodology disclosure** -- Ensure transparency to reduce defamation risk
- [ ] **Attorney review of ToS and Privacy Policy** -- Budget $500-$1,500

### 8.4 Ongoing Requirements (Monthly/Quarterly/Annual)

| Frequency | Task |
|-----------|------|
| **Monthly** | Reconcile business bank account in Wave/QBO |
| **Monthly** | Review and categorize business expenses |
| **Quarterly** | Pay estimated federal taxes (Form 1040-ES) |
| **Quarterly** | Pay estimated state taxes (if applicable) |
| **Quarterly** | Review insurance coverage adequacy |
| **Annually** | File Wyoming annual report ($60) |
| **Annually** | Pay registered agent fee ($100-$300) |
| **Annually** | Renew domain names |
| **Annually** | Renew insurance policies |
| **Annually** | File federal tax return (Schedule C on Form 1040) by April 15 |
| **Annually** | Review and update ToS, Privacy Policy, MHMDA policy |
| **Annually** | Review sales tax nexus thresholds in all states |
| **As needed** | Respond to data deletion requests within 45 days |
| **As needed** | Update regulatory status data as FDA rules change |
| **5 years post-trademark** | File trademark Declaration of Use (Section 8) |

---

## 9. Cost Summary

### 9.1 Total Setup Cost (One-Time)

| Item | Low Estimate | High Estimate |
|------|-------------|---------------|
| Wyoming LLC filing | $100 | $100 |
| Registered agent (Year 1) | $100 | $300 |
| EIN application | $0 | $0 |
| Operating agreement | $0 | $35 |
| Domain names (2-3 domains) | $25 | $100 |
| Trademark filing (1-2 classes) | $350 | $700 |
| Attorney review of ToS/Privacy | $500 | $2,000 |
| DMCA agent registration | $6 | $6 |
| **Total setup** | **$1,081** | **$3,241** |

### 9.2 Monthly Ongoing Costs

| Item | Low Estimate | High Estimate |
|------|-------------|---------------|
| Insurance (E&O + Cyber + GL) | $133 | $354 |
| Accounting software (Wave) | $0 | $0 |
| Banking | $0 | $0 |
| Stripe fees (on $1K MRR) | $40 | $55 |
| Analytics (Plausible) | $9 | $9 |
| **Total monthly** | **$182** | **$418** |

### 9.3 Annual Ongoing Costs

| Item | Annual Cost |
|------|-------------|
| Insurance | $1,600-$4,250 |
| Wyoming annual report | $60 |
| Registered agent | $100-$300 |
| Domain renewals | $25-$100 |
| Accounting software | $0 (Wave) |
| CPA tax preparation (optional) | $200-$800 |
| **Total annual (non-revenue costs)** | **$1,985-$5,510** |

### 9.4 Priority Order: What to Do First vs. What Can Wait

**Do immediately (Week 0 -- before writing any code for public release):**
1. Form Wyoming LLC ($100)
2. Get EIN (free, instant)
3. Open Mercury bank account (free, 10 minutes)
4. Draft operating agreement (free, 1-2 hours)

**Do before public launch (Week 1-2):**
5. Draft medical disclaimer, ToS, and privacy policy
6. Draft MHMDA standalone health data policy
7. Get E&O insurance quote and bind policy (~$60/month)
8. Set up Stripe (~30 minutes)
9. Register primary domain name ($10-$15)

**Do in first month of operation:**
10. Add cyber liability insurance (~$50-$150/month)
11. Set up Wave accounting and connect bank account
12. File trademark application ($350-$700)
13. Pay for attorney review of legal documents ($500-$1,500)

**Can wait 3-6 months:**
14. General liability insurance (if not bundled already)
15. Register additional domain variants
16. Copyright registration for key content
17. Sales tax setup (TaxJar/Stripe Tax -- only when approaching nexus thresholds)
18. Consider S-corp election (only when net profit exceeds ~$40-50K)

---

## Appendix A: Key Legal Resources

| Resource | URL | Use |
|----------|-----|-----|
| Wyoming Secretary of State | https://sos.wyo.gov | LLC filing |
| IRS EIN Online Application | https://www.irs.gov/businesses/small-businesses-self-employed/apply-for-an-employer-identification-number-ein-online | EIN |
| USPTO Trademark Center | https://www.uspto.gov/trademarks | Trademark filing |
| USPTO TESS (Trademark Search) | https://tmsearch.uspto.gov | Trademark preliminary search |
| MHMDA Full Text | https://app.leg.wa.gov/RCW/default.aspx?cite=19.373&full=true | Washington health data law |
| CCPA Full Text | https://oag.ca.gov/privacy/ccpa | California privacy law |
| IRS Direct Pay | https://www.irs.gov/payments | Quarterly tax payments |
| Mercury | https://mercury.com | Business banking |
| Stripe | https://stripe.com | Payment processing |
| Hiscox | https://www.hiscox.com | E&O insurance |
| Coalition | https://www.coalitioninc.com | Cyber insurance |
| Wave | https://www.waveapps.com | Free accounting |
| Plausible Analytics | https://plausible.io | Privacy-first analytics |
| Termly.io | https://termly.io | ToS/Privacy policy generator |

## Appendix B: Attorney Checklist

When you engage an attorney for review, ask them to specifically address:

1. **Health information liability exposure** -- Is the medical disclaimer sufficient for a peptide information platform?
2. **Defamation risk from vendor ratings** -- Are your rating methodology disclosures adequate to establish fair comment/opinion defense?
3. **MHMDA compliance** -- Does the standalone health data policy meet all statutory requirements?
4. **Arbitration enforceability** -- Is the arbitration clause enforceable in California, Washington, and New York?
5. **User-submitted COA handling** -- What additional protections are needed for user-generated content?
6. **Foreign LLC registration** -- Do you need to register as a foreign LLC in your home state?
7. **Section 230 applicability** -- Does Section 230 of the Communications Decency Act protect your platform for third-party content?

**Estimated cost for this review: $500-$2,000**
**Recommended timing: Before public launch, after you have drafted all documents**

---

*This guide is for informational purposes only and does not constitute legal advice. Consult a licensed attorney for guidance specific to your situation.*

*Generated 2026-03-24 | Peptide Checker Legal Infrastructure Planning*
