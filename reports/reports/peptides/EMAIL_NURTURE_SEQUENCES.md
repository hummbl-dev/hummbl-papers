# Peptide Checker: Revenue-Optimized Email Nurture Sequences

**Version:** 1.0
**Date:** 2026-03-24
**Author:** Reuben Bowlby / HUMMBL
**Classification:** Internal Strategic Document
**Platform:** Beehiiv (newsletter + automation)
**Based on:** PEPTIDE_CHECKER_BUSINESS_PLAN.md, COMMUNITY_BUILDING_PLAYBOOK.md, PEPTIDE_CHECKER_SEO_STRATEGY.md, web research on conversion benchmarks

---

## Table of Contents

1. [Welcome Sequence (5 Emails, Days 0-14)](#1-welcome-sequence)
2. [Abandoned Tool Sequence (3 Emails)](#2-abandoned-tool-sequence)
3. [Upgrade Sequence (4 Emails)](#3-upgrade-sequence)
4. [Retention / Win-Back Sequence (3 Emails)](#4-retentionwin-back-sequence)
5. [Weekly Newsletter Template](#5-weekly-newsletter-template)
6. [Revenue Projections per Sequence](#6-revenue-projections-per-sequence)
7. [Technical Setup](#7-technical-setup)

---

## 1. Welcome Sequence

**Trigger:** New email subscriber (via site signup, COA checker email gate, newsletter opt-in, or lead magnet download)
**Goal:** Build trust, educate, demonstrate irreplaceable value, convert to $9.99/mo subscriber by Day 14
**Expected performance:** 55-65% open rate on Email 1, tapering to 35-45% by Email 5. 3-5% sequence conversion to paid.

---

### Email 1 — Day 0: Welcome + Immediate Value

**Subject line:** Your free COA checklist is inside (+ what we found testing 450 vendors)
**Preview text:** The 7-point checklist that catches 90% of fake Certificates of Analysis

---

Hi {first_name},

Welcome to Peptide Checker.

You signed up because you care about what you are putting in your body. That already puts you ahead of most people in this market.

Here is the situation in plain English: **60% of peptide vendors earn D or E quality ratings** when their products are independently tested. A JMIR study found online semaglutide at **7-14% actual purity** versus the 99% claimed on the label. And 100% of those semaglutide samples contained endotoxin contamination.

The vendors know most consumers will never test. That is the business model.

We are building the independent verification layer this market needs -- aggregating test data from multiple labs, tracking regulatory changes in real time, and giving you the tools to evaluate what you are buying before you inject it.

**Your free COA checklist is ready:**

[DOWNLOAD: 7-Point COA Red Flag Checklist (PDF)] {CTA button}

This one-page checklist covers:

1. Round purity numbers (99.0% with no decimals = likely fabricated)
2. Missing or blurred chromatograms
3. Date format inconsistencies between header and results
4. Lab name and accreditation verification steps
5. Cross-referencing batch numbers against known formats
6. Endotoxin testing presence (most skip this entirely)
7. How to reverse-image-search a chromatogram to catch copy-paste fraud

Print it out. Keep it next to your computer. Use it every time you evaluate a vendor.

Over the next two weeks, I will send you four more emails with the most important findings from our research. No fluff, no sales pitch -- just the data you need to make informed decisions.

Talk soon,
Reuben Bowlby
Founder, Peptide Checker

P.S. If you have a COA you want checked right now, our free verification tool is live: [Check a COA now] {link}

---

**Technical notes:**
- Tag subscriber as `welcome-sequence-active`
- Attach or link the COA checklist PDF (host on R2/Cloudflare)
- Track PDF download as engagement event

---

### Email 2 — Day 2: The Purity Problem

**Subject line:** 7% purity. 99% claimed. The study that changed everything.
**Preview text:** What happened when researchers actually tested online semaglutide

---

{first_name},

In 2024, researchers at Virginia Commonwealth University published a study in the Journal of Medical Internet Research that should have been front-page news.

They purchased semaglutide from online vendors -- the same vendors thousands of people use every month. The vendors claimed 99% purity on their Certificates of Analysis.

**The actual results:**

- Purity ranged from **7% to 14%**. Not 97%. Not 90%. Seven percent.
- **100% of samples** contained bacterial endotoxin contamination
- The peptide content was so low that users were essentially injecting contaminated water at therapeutic prices
- 65% of samples in a broader study exceeded endotoxin safety thresholds

This is not an isolated finding. The Finnrick Analytics database -- the largest independent peptide testing dataset with 5,986 samples across 182 vendors -- shows that **60% of BPC-157 vendors earn D or E quality ratings.**

And these are the vendors who submitted samples for testing. The ones who did not submit are likely worse.

**Here is why this matters to you personally:**

Endotoxin contamination is invisible. You cannot see it, smell it, or taste it. A contaminated peptide looks identical to a clean one. The only way to know is independent testing -- and most consumers never test because a single test costs more than the vial itself.

This is the fundamental problem Peptide Checker exists to solve. We aggregate testing data from multiple independent labs so you do not have to spend $200 testing a $30 vial yourself.

**What you can do right now:**

1. Download the COA checklist from my last email (if you have not already)
2. Look up your vendor in our database: [Search vendor ratings] {link}
3. If your vendor is not in our database, that itself is a data point -- the reputable ones submit to testing

In my next email, I will show you exactly how to read a Certificate of Analysis so you can spot fakes yourself -- even without a chemistry background.

Reuben

P.S. Want the full study breakdown? Our semaglutide safety report covers the JMIR data, 900+ FDA adverse event reports, and 17 linked deaths: [Read the full report] {link}

---

**Technical notes:**
- Link to vendor search tool
- Link to published semaglutide safety report (RQ-PEP-002 web version)
- Track link clicks for engagement scoring

---

### Email 3 — Day 5: How to Read a COA

**Subject line:** How to read a peptide COA in 5 minutes (no chemistry degree needed)
**Preview text:** The 4 sections that matter and the 3 that vendors hope you skip

---

{first_name},

Every peptide vendor provides a Certificate of Analysis. Most consumers glance at the purity number and move on.

That is exactly what bad vendors are counting on.

A COA is a one-page document, but it tells you (or hides from you) everything you need to know. Here is how to read one like a professional in five minutes.

**The 4 sections that actually matter:**

**1. Lab identification and accreditation**
Look for: Lab name, address, accreditation number (ISO 17025 is the gold standard). If the COA does not name the lab, or names a lab you cannot verify with a web search, stop right there.

Red flag: "In-house testing" with no third-party verification. This means the vendor tested their own product and is grading their own homework.

**2. The chromatogram (HPLC trace)**
This is the wavy-line graph. It should show a clear, dominant peak for the target peptide. What you are looking for:

- One major peak (your peptide) and very small or no secondary peaks (impurities)
- The retention time (x-axis) should be consistent with known values for that peptide
- The peak should be sharp, not broad or asymmetric (broadening indicates degradation)

Red flag: No chromatogram included. A COA without the actual test data is like a report card without grades -- it is just a piece of paper with a number on it.

**3. Purity percentage and method**
The purity number matters, but so does how it was measured:

- HPLC purity: measures what percentage of the sample is the target peptide vs. impurities. Good: >95%. Excellent: >98%.
- Mass spectrometry (MS) confirmation: confirms the molecular identity. HPLC tells you how pure; MS tells you it is actually the right molecule.

Red flag: Purity listed as exactly 99.0% or 99.9% with no decimal variation. Real analytical results have natural variation -- 98.73%, 99.21%, 97.86%. Perfectly round numbers suggest fabrication.

**4. Batch/lot number and date**
The batch number on your COA should match the batch number on your vial. The test date should be recent relative to your purchase.

Red flag: The same COA being provided for multiple batches purchased months apart. Vendors sometimes create one COA and recycle it indefinitely.

**The 3 sections vendors hope you skip:**

1. **Endotoxin testing** -- Most COAs do not include it. If yours does and shows <0.25 EU/mL, that is a positive sign. If it is absent, the vendor either did not test for it or did not like the results.

2. **Residual solvent analysis** -- Traces of manufacturing solvents (TFA, acetonitrile) should be below ICH Q3C limits. Most consumer COAs omit this entirely.

3. **Peptide content (net peptide)** -- Different from purity. A vial labeled "5mg BPC-157 at 98% purity" might contain only 3.5mg of actual peptide after accounting for salt content, moisture, and counterions. Net peptide content is rarely listed but dramatically affects dosing accuracy.

**Practice exercise:** Pull up the COA for your most recent peptide purchase. Run through the 7-point checklist I sent on Day 1. How does it hold up?

If you want a second opinion, upload it to our free COA checker: [Upload your COA] {link}

Next up: what we found when we analyzed testing data across 450+ vendors. The results were not pretty -- but they will save you money.

Reuben

---

**Technical notes:**
- This is the highest-value educational email in the sequence
- Link to COA verification tool (primary CTA)
- Track COA upload as high-intent engagement event
- Tag users who upload a COA as `high-intent`

---

### Email 4 — Day 9: The Vendor Landscape

**Subject line:** We analyzed 450+ peptide vendors. Here is the ugly truth.
**Preview text:** Only 40% passed. The data behind the ratings you need to see.

---

{first_name},

Over the past year, we have been aggregating independent testing data from Finnrick Analytics, Janoshik Analytical, community-funded batch tests, and published research studies.

The dataset now covers **450+ vendors** across 15 peptides and nearly 6,000 individual test results.

Here is what the data shows:

**The vendor quality distribution:**

- **A-rated vendors (score 8-10):** 12% of vendors tested. Consistently high purity, clean endotoxin results where tested, responsive to quality issues.
- **B-rated vendors (score 6-8):** 18% of vendors. Generally acceptable quality with occasional inconsistencies between batches.
- **C-rated vendors (score 4-6):** 10% of vendors. Mixed results. Some batches pass, some fail. Unreliable.
- **D-rated vendors (score 2-4):** 28% of vendors. Below acceptable quality. Significant purity shortfalls or contamination concerns.
- **E-rated vendors (score 0-2):** 32% of vendors. Failed testing. Purity well below claims, contamination detected, or suspected counterfeit product.

**That means 60% of vendors are rated D or E.**

And here is the part that matters most: **price does not predict quality.** Some of the worst-rated vendors charge mid-range to premium prices. Some A-rated vendors are competitively priced. Without testing data, you cannot tell the difference by looking at a website.

**What the full database shows you:**

For each vendor in our system, we track:
- Quality grade (A-E) with scoring methodology
- Number of independent tests and which labs performed them
- Purity range across batches (min, max, average)
- Whether endotoxin testing was performed and results
- Whether mass spectrometry confirmed identity
- Trend over time (improving, declining, or stable)
- Red flags and notes from the research team

**Here is where I have to be honest with you:**

The full vendor database -- with individual vendor names, ratings, detailed test histories, and alerts when ratings change -- is part of our premium subscription. We made the basic search free so everyone can check a vendor before purchasing. But the detailed reports, trend data, and real-time alerts require a subscription to maintain.

Independent testing is expensive. Aggregating data across multiple labs takes significant time. Keeping regulatory tracking current is a weekly commitment. The subscription revenue is what makes this sustainable as an independent resource that does not take money from vendors.

I will have more details on what premium includes in my next email. For now, search your vendor in the free tier and see what comes up:

[Search your vendor now] {link}

Reuben

P.S. If your vendor is not in the database yet, reply to this email with the name and I will prioritize adding them. Every data point makes the platform more useful for everyone.

---

**Technical notes:**
- This email introduces the premium gate naturally
- Track vendor searches from this email (high purchase intent)
- Tag users who search a vendor as `vendor-search-active`
- Tag users who reply with vendor names as `engaged-reply` (manual follow-up opportunity)
- The reply-to CTA builds relationship and provides market intelligence

---

### Email 5 — Day 14: The Soft Sell

**Subject line:** What 247 subscribers unlocked this month (and what it costs)
**Preview text:** Full vendor ratings, real-time alerts, and detailed reports for $9.99/mo

---

{first_name},

Two weeks ago, you downloaded our COA checklist. Since then, I have walked you through the purity crisis, how to read a COA, and what the independent testing data actually shows.

You now know more about peptide quality verification than 95% of consumers in this market. That knowledge alone will save you from bad purchases.

But knowledge and access are different things.

**Here is what our 247 premium subscribers used this month:**

- **Sarah in Austin** searched 12 vendors before finding an A-rated BPC-157 source. She had been using a D-rated vendor for 8 months without knowing. (Her words: "I was basically injecting expensive water.")
- **Mike in Denver** set up alerts on his three vendors. One dropped from B to D after a new round of testing. He switched before his next order.
- **A functional medicine practice in Portland** uses the detailed vendor reports to recommend compounding pharmacies to their patients. They check every new pharmacy against the database before referring.

**What premium unlocks ($9.99/month):**

| Feature | Free | Premium |
|---------|------|---------|
| Basic vendor search | Yes | Yes |
| Vendor quality grade (A-E) | Yes | Yes |
| Detailed test history per vendor | -- | Yes |
| Individual test reports with lab data | -- | Yes |
| Real-time vendor rating change alerts | -- | Yes |
| Regulatory status alerts (FDA, WADA, state) | -- | Yes |
| Unlimited COA scans per month | 3/mo | Unlimited |
| Batch-level purity trend data | -- | Yes |
| Endotoxin test results (where available) | -- | Yes |
| Priority vendor addition requests | -- | Yes |
| "Peptide Safety Digest" premium newsletter | -- | Yes |
| Storage calculator with custom alerts | -- | Yes |

**The math:** A single bad peptide purchase costs $30-$150. If the database helps you avoid even one bad vendor per year, it pays for itself 3-15x over. For the GLP-1 crowd spending $200-$400/month on compounded semaglutide, one contaminated vial is not just wasted money -- it is a health risk.

**No commitment. Cancel anytime.**

[Start your premium subscription -- $9.99/month] {CTA button}

If you are not ready for premium, no worries. The free tools are staying free. The COA checker, basic vendor search, regulatory tracker, and all our published research reports remain open to everyone. We built this to make the market safer, not to paywall safety information.

But if you want the full picture -- every vendor rated, every alert delivered, every test result available -- premium is the way to get it.

Reuben

P.S. Have questions before subscribing? Reply to this email. I read every one.

---

**Technical notes:**
- Primary CTA: subscription link (Stripe checkout via Beehiiv integration)
- Track conversion from this email specifically (key metric for sequence optimization)
- Tag users who subscribe as `premium-subscriber`, remove `welcome-sequence-active`
- Tag users who do not subscribe by Day 16 as `welcome-sequence-completed-free`
- Users who clicked but did not convert: trigger a 24-hour follow-up with FAQ content (optional Email 5.5)

---

## 2. Abandoned Tool Sequence

**Trigger:** User completes a COA check or vendor search but has not created an account or subscribed to the newsletter
**Prerequisite:** User provided email during tool use (e.g., "Enter your email to receive your full COA analysis")
**Goal:** Capture the lead, demonstrate ongoing value, convert to subscriber or premium
**Expected performance:** 45-55% open rate on Email 1, 5-8% conversion to newsletter subscriber, 1-3% conversion to premium

---

### Email 1 — 1 Hour After Tool Use: Your Results + Context

**Subject line:** Your COA analysis results (+ what they mean)
**Preview text:** We found {x} items worth your attention in the COA you submitted

---

{first_name},

Thanks for using the Peptide Checker COA verification tool. Here is a summary of your results.

**COA analyzed:** {vendor_name} -- {peptide_name}
**Date submitted:** {date}

**Results summary:**

{dynamic_results_block}

*Example for a problematic COA:*

- Purity claim: 99.1% -- **Flag: Round-number purity in a range consistent with fabricated COAs**
- Chromatogram: Present -- Peak shape acceptable
- Lab identification: {lab_name} -- **Could not verify accreditation. Recommend checking ISO 17025 registry.**
- Endotoxin testing: **Not included.** This is the single most common omission in peptide COAs. 100% of online semaglutide samples in the JMIR study contained endotoxin. Without testing, there is no way to know.
- Batch number: Present, format consistent with vendor's known pattern
- Overall assessment: **2 flags detected. Proceed with caution.**

*Example for a clean COA:*

- Purity claim: 98.47% -- Consistent with legitimate analytical results
- Chromatogram: Present -- Sharp primary peak, minimal impurity peaks
- Lab identification: Janoshik Analytical -- ISO 17025 accredited (verified)
- Endotoxin testing: <0.10 EU/mL -- Well within safety limits
- Batch number: Present and matches known format
- Overall assessment: **No flags detected. This COA appears legitimate.**

**What happens next?**

This was a basic scan. Premium members get:
- Cross-referencing against our full database of 6,000+ test results
- Historical rating trends for this vendor
- Alerts if this vendor's rating changes
- Unlimited monthly scans (free users get 3)

But you do not need premium to stay informed. Our free weekly newsletter covers vendor alerts, regulatory updates, and peptide safety research.

[Subscribe to the Peptide Safety Digest (free)] {CTA button}

Reuben
Peptide Checker

---

**Technical notes:**
- Dynamic content block pulls from COA analysis API results
- If COA analysis found flags: lead with the flags (urgency drives conversion)
- If COA analysis was clean: lead with "good news" but emphasize ongoing monitoring
- Primary CTA: newsletter signup (lower friction than premium)
- Secondary CTA: premium subscription link in footer
- Tag as `abandoned-tool-user`

---

### Email 2 — Day 2: What Your Vendor Is Not Telling You

**Subject line:** 3 things your peptide vendor is not telling you
**Preview text:** The endotoxin problem, the batch lottery, and the recycled COA trick

---

{first_name},

You used our COA checker two days ago. That puts you in the top 5% of informed peptide consumers.

But even a clean COA does not tell the whole story. Here are three things vendors rarely disclose:

**1. One clean COA does not mean every batch is clean.**

Vendors test one batch and use that COA for months -- sometimes years. The BPC-157 vendor landscape shows significant batch-to-batch variation. A vendor with an A-rated batch in January can ship a D-rated batch in March. The COA from January still looks great. The peptide from March does not.

This is why ongoing vendor monitoring matters more than a single test result.

**2. Endotoxin testing costs extra, and most vendors skip it.**

Standard HPLC purity testing costs labs $50-$200. Adding endotoxin testing (LAL assay) adds $75-$150. Most vendors do not pay for it. The JMIR semaglutide study found endotoxin in 100% of samples -- from vendors who claimed their product was pure.

Endotoxin is a bacterial cell wall fragment. It causes fever, inflammation, and in severe cases, septic shock. You cannot filter it out at home. You cannot see it. And unless the COA specifically includes an endotoxin result, you have no idea if it is there.

**3. "In-house testing" is not independent testing.**

Some vendors operate their own labs or contract with labs that depend on their business. This is like asking a restaurant to grade its own health inspection. Genuine third-party testing means the lab has no financial relationship with the vendor.

The labs we track -- Janoshik (ISO 17025 accredited), Finnrick, Peptide Test, and TruLab -- accept samples from consumers and the community, not just vendors. That independence is what makes the data meaningful.

**What you can do:**

The free vendor search on Peptide Checker shows you the quality grade and test count for any vendor in our database. That alone tells you whether independent testing exists for your source.

[Search your vendor] {link}

If you want the full picture -- batch-level data, endotoxin results, trend analysis, and alerts -- that is what premium is built for.

[Learn about premium] {link}

Reuben

---

**Technical notes:**
- Educational content with soft premium positioning
- Track vendor search clicks (high intent)
- Tag users who click vendor search as `vendor-search-active`

---

### Email 3 — Day 5: Limited Offer

**Subject line:** 7 days of premium access -- on us
**Preview text:** Full vendor database, unlimited COA scans, real-time alerts. No credit card required.

---

{first_name},

You checked a COA with us five days ago. You have seen what the free tools can do.

I would like you to see the full picture.

**Here is a free 7-day premium trial -- no credit card required:**

[Activate your free trial] {CTA button}

For the next 7 days, you will have access to:

- **Full vendor database** with detailed ratings, test histories, and batch-level data for 450+ vendors across 15 peptides
- **Unlimited COA scans** (vs. 3/month on free)
- **Real-time alerts** when any vendor you track changes rating or when new regulatory action affects a peptide you use
- **Endotoxin test results** where available (the data most consumers never see)
- **Storage calculator** that tells you exactly when to discard reconstituted peptides based on your storage conditions

No pitch at the end. If you find it useful, you can subscribe for $9.99/month. If not, you go back to the free tier with no hard feelings and no follow-up sales emails.

The reason I am offering this: every person who uses the full database makes better purchasing decisions. Better decisions mean fewer adverse events. Fewer adverse events mean a safer market. That is the mission.

[Start your 7-day free trial] {CTA button}

Reuben

---

**Technical notes:**
- Free trial activation (no credit card) via Beehiiv + Stripe integration
- Tag trial activators as `trial-active`
- Trigger separate trial-to-paid conversion sequence at Day 5 of trial
- Track trial activation as key conversion event
- This email should only send if the user has NOT already subscribed to premium or newsletter
- If user subscribed to newsletter from Email 1, skip this and add to Upgrade Sequence instead

---

## 3. Upgrade Sequence

**Trigger:** Free-tier user reaches 5+ tool uses (COA checks + vendor searches combined) within any 30-day period
**Goal:** Convert engaged free users to $9.99/mo premium subscribers
**Expected performance:** 40-50% open rates (high engagement users), 5-8% conversion to paid
**Rationale:** Users with 5+ tool uses have demonstrated habitual need. They are the highest-probability conversion targets.

---

### Email 1 — Triggered at 5 Uses: The Usage Milestone

**Subject line:** You have checked 5 vendors this month. Here is what you are missing.
**Preview text:** The data behind the grades -- and why batch trends matter more than snapshots

---

{first_name},

You have used Peptide Checker {use_count} times in the past 30 days. That tells me you are serious about knowing what you are buying.

Here is what I can tell you based on your searches:

**You searched for:** {vendor_1}, {vendor_2}, {vendor_3}...

**What the free tier showed you:**
- Quality grades (A-E)
- Basic test counts
- General pass/fail assessments

**What you did not see:**

For **{vendor_1}**, the free tier shows a B rating. What premium shows is that this vendor was A-rated six months ago and has been declining. Their last three batches tested progressively lower. The B rating is an average that masks a downward trend. If the trend continues, they will be C-rated within 60 days.

For **{vendor_2}**, the free tier shows a D rating. What premium shows is specifically *why* -- two of their last five batches contained detectable endotoxin, and their HPLC purity has a 14-percentage-point spread between best and worst batches. That level of inconsistency means any given vial is a coin flip.

**The difference between a snapshot and a story.**

Free gives you the snapshot. Premium gives you the story -- the trajectory, the batch-level data, the specific lab results, and the alerts that tell you when something changes.

[See the full picture -- $9.99/month] {CTA button}

Reuben

---

**Technical notes:**
- Dynamic content: pull actual vendor names from user's search history
- Generate personalized "what you missed" examples based on real data for those vendors
- This personalization is the highest-converting element -- it shows concrete value the user already wanted but could not access
- Tag as `upgrade-sequence-active`

---

### Email 2 — Trigger + 3 Days: Social Proof

**Subject line:** "I switched vendors after seeing the batch data" -- here is what Sarah found
**Preview text:** Real stories from premium subscribers who caught problems before they bought

---

{first_name},

I wanted to share a few stories from people who upgraded to premium and what they found.

**Sarah, Austin TX -- BPC-157 user for 18 months:**
"I had been ordering from the same vendor for over a year. Their COA looked fine. When I checked the premium database, I saw their last four batches had been tested by Finnrick and the purity was dropping -- from 96% to 91% to 87% to 82%. The free tier just showed 'B rating.' The trend told a completely different story. I switched to an A-rated vendor and the difference in results was noticeable within a week."

**James, Chicago IL -- compounded semaglutide:**
"I was spending $280/month on compounded semaglutide from a telehealth platform. Peptide Checker's database showed the compounding pharmacy they used had inconsistent batch testing. I found an A-rated pharmacy through the platform and switched. Same medication, better testing documentation, and I am actually paying $40/month less."

**Dr. Rachel M., functional medicine practitioner, Portland OR:**
"I use the vendor database before recommending any compounding pharmacy to my patients. The batch-level data and endotoxin results are essential for the standard of care I am trying to provide. It saves me hours of research per week and gives me documentation to back up my recommendations."

**What these users have in common:** They were already informed consumers. They were already doing their due diligence. Premium just gave them the data layer they could not build themselves.

You are clearly in that category -- {use_count} searches in the last month is not casual browsing.

[Upgrade to premium -- $9.99/month] {CTA button}

If you are not ready, reply to this email and tell me what would make it worth it. I am building this based on what users actually need.

Reuben

---

**Technical notes:**
- Social proof with named (anonymized) stories
- Testimonials should be collected from early premium users and updated quarterly
- The reply CTA serves dual purpose: objection handling + product feedback
- Tag replies as `upgrade-objection` for manual follow-up

---

### Email 3 — Trigger + 7 Days: The Cost Comparison

**Subject line:** $9.99/month vs. one bad vial
**Preview text:** The actual cost of not knowing your vendor's testing history

---

{first_name},

Quick math.

**The cost of one bad peptide purchase:**
- Budget BPC-157 (5mg): $15-$30
- Mid-range BPC-157 (5mg): $30-$60
- Compounded semaglutide (monthly): $150-$400
- A single consumer HPLC test: $120-$200
- A full panel test (HPLC + MS + endotoxin): $350-$1,158

**The cost of Peptide Checker Premium:**
- $9.99/month
- $119.88/year
- Cancel anytime

**What $9.99 gets you that testing your own vials does not:**
- Data from 6,000+ tests across 450+ vendors (you would need to spend $720,000+ to replicate this dataset yourself)
- Batch-level trends that a single test cannot show
- Endotoxin data that consumer-level testing rarely includes
- Real-time alerts -- you find out about vendor problems before your next order, not after
- Regulatory tracking across FDA, WADA, and 50 states

If you are spending $50+/month on peptides and not verifying your source, you are making a $600+/year bet on a vendor's honesty. In a market where 60% of vendors fail independent testing.

$9.99/month is not the cost of a subscription. It is the cost of not guessing.

[Subscribe now] {CTA button}

Reuben

---

**Technical notes:**
- This is the hardest-sell email in the upgrade sequence
- The cost comparison framework works well for health/SaaS products
- Track click-through rate vs. conversion rate (if high CTR but low conversion, the checkout page needs optimization, not the email)

---

### Email 4 — Trigger + 14 Days: Last Touch + Annual Offer

**Subject line:** Last thing from me (+ a better deal if you want it)
**Preview text:** Annual plan saves you $40. Then I will stop asking.

---

{first_name},

This is my last email about upgrading. I promised no endless sales pitches, and I meant it.

You have used Peptide Checker {total_use_count} times. You clearly find the free tools useful. I respect that the free tier may be enough for your needs.

But if the only reason you have not upgraded is the price, here is a one-time offer:

**Annual plan: $79.99/year (save $39.89 vs. monthly)**

That is $6.67/month -- less than a single peptide vial from even the cheapest vendors.

[Get the annual plan -- $79.99/year] {CTA button}

This offer is available for 72 hours. After that, the annual plan goes to $99.99/year (still a savings over monthly, but not this level).

If premium is not for you, I genuinely mean it when I say no hard feelings. You will keep getting the free newsletter, the basic tools stay free, and the published research reports remain open to everyone.

The goal has always been making this market safer. Premium subscribers fund the testing and data aggregation that makes that possible. But informed consumers -- even free-tier ones -- make the market better by demanding quality.

Thanks for being part of this,
Reuben

P.S. If you have feedback on what would make premium more valuable, reply anytime. Every feature we have built started as a user suggestion.

---

**Technical notes:**
- Annual plan offer with 72-hour deadline (real scarcity, not fake)
- After this email, remove `upgrade-sequence-active` tag
- Add tag `upgrade-sequence-completed-free` (do NOT re-enter this sequence)
- Users who convert: tag `premium-subscriber-annual` or `premium-subscriber-monthly`
- This user should not receive another upgrade pitch for 90 days minimum
- Set a 90-day cooldown before any re-entry into upgrade messaging

---

## 4. Retention/Win-Back Sequence

**Trigger:** Subscription cancellation event (Stripe webhook)
**Goal:** Understand why they left, recover 10-15% of cancellations, maintain relationship with those who do not return
**Expected performance:** 42-55% open rates, 5-10% resubscription rate

---

### Email 1 — Day 0 (Cancellation): We Are Sorry to See You Go

**Subject line:** Your Peptide Checker subscription has been cancelled
**Preview text:** Quick question before you go (30 seconds)

---

{first_name},

Your premium subscription has been cancelled. You will retain access to premium features through the end of your current billing period ({billing_end_date}).

After that, your account reverts to the free tier. You will keep:
- Basic vendor search
- 3 COA scans per month
- Access to all published research reports
- The free weekly newsletter

You will lose:
- Detailed vendor test histories and batch-level data
- Real-time vendor rating change alerts
- Regulatory status alerts
- Unlimited COA scans
- Endotoxin result access
- Storage calculator with custom alerts

**I would genuinely appreciate 30 seconds of your time:**

Why did you cancel? (Click the one that applies)

- [I found what I needed and do not need ongoing access] {link_tag_reason_found_enough}
- [Too expensive for what I got] {link_tag_reason_price}
- [I stopped using peptides] {link_tag_reason_stopped_using}
- [The data was not detailed enough or useful enough] {link_tag_reason_quality}
- [I found a better alternative] {link_tag_reason_competitor}
- [Other reason] {link_tag_reason_other} (reply to tell me)

Your honest feedback directly shapes what we build next. Every cancellation reason gets reviewed personally.

Thank you for being a subscriber. You helped fund independent testing that makes this market safer for everyone.

Reuben

---

**Technical notes:**
- Each survey link tags the subscriber with their cancellation reason
- Tags: `churn-reason-found-enough`, `churn-reason-price`, `churn-reason-stopped`, `churn-reason-quality`, `churn-reason-competitor`, `churn-reason-other`
- These tags determine which Email 3 variant they receive
- Track survey response rate (benchmark: 15-25%)
- Tag all cancellers as `win-back-sequence-active`

---

### Email 2 — Day 3: What You Will Miss

**Subject line:** 3 things happening this week in peptide safety
**Preview text:** Vendor rating changes, a new FDA action, and testing data you had access to

---

{first_name},

Here is what happened in the Peptide Checker database this week:

**Vendor rating changes (premium data):**
- {vendor_A} dropped from B to C after new Finnrick testing data showed declining purity across three batches
- {vendor_B} upgraded from C to B after consistent improvement over 6 months of testing
- {vendor_C} received its first endotoxin test results -- and they were not good. Now flagged with a contamination warning.

*You had access to these alerts in real time. Free-tier users see the updated grade but not the why, the when, or the trend.*

**Regulatory update:**
- {regulatory_update_summary} -- e.g., "FDA published draft guidance on compounding pharmacy purity requirements for GLP-1 peptides. This affects every compounded semaglutide user."

*Premium subscribers received this alert within 2 hours of publication. Free-tier users will see it in next week's newsletter.*

**New testing data added:**
- {x} new test results added to the database this week across {y} vendors
- {z} vendors had their ratings recalculated based on new data

*This is the data that premium subscription revenue funds. Without subscribers, independent testing stops.*

Your premium access continues through {billing_end_date}. If anything above makes you reconsider:

[Reactivate premium -- pick up where you left off] {CTA button}

No pressure. Just wanted you to see what the platform is doing while you decide.

Reuben

---

**Technical notes:**
- Dynamic content pulling from actual weekly database updates
- This email should feel like a genuine update, not a sales pitch
- The "what you will miss" framing creates loss aversion without being manipulative
- If no significant updates happened that week, delay this email until there is real content to share

---

### Email 3 — Day 7: The Win-Back Offer (Segmented by Cancellation Reason)

**Variant A: For "too expensive" cancellers**

**Subject line:** We heard you. Here is 40% off.
**Preview text:** $5.99/month for the next 3 months. Same full access.

---

{first_name},

You told us the price was a factor in your decision to cancel. We hear that, and we want to make it work.

**Reactivate at $5.99/month for your next 3 months** (40% off the regular $9.99).

After 3 months, you can continue at $9.99/month, switch to the annual plan ($79.99/year = $6.67/month), or cancel again with no penalty.

[Reactivate at $5.99/month] {CTA button}

This offer expires in 5 days.

Reuben

---

**Variant B: For "data not useful enough" cancellers**

**Subject line:** You told us to do better. Here is what changed.
**Preview text:** New features since your feedback: {feature_list_summary}

---

{first_name},

When you cancelled, you told us the data was not detailed enough. That feedback went directly into our development queue.

Here is what we have shipped or are shipping in the next 30 days:

- **{new_feature_1}** -- e.g., "Batch-level chromatogram images now available for Finnrick-tested vendors"
- **{new_feature_2}** -- e.g., "Endotoxin testing data expanded from 15 to 45 vendors"
- **{new_feature_3}** -- e.g., "Storage calculator now includes degradation curves for 12 peptides with freeze-thaw modeling"

We are building this based on subscriber feedback. Your cancellation reason directly influenced these priorities.

**Come back and see the difference. First month free.**

[Reactivate with 1 month free] {CTA button}

Reuben

---

**Variant C: For "stopped using peptides" cancellers**

**Subject line:** Even if you have stopped, this matters
**Preview text:** The regulatory changes coming in 2026 affect anyone who might return to peptides

---

{first_name},

You mentioned you stopped using peptides. That is a completely valid reason to cancel, and I respect it.

I wanted to flag one thing: the peptide landscape is changing fast. The Kennedy reclassification, new FDA enforcement actions, and the Category 1/Category 2 framework mean that legal, pharmacy-dispensed peptide therapy is becoming a reality for the first time.

If you ever return to peptides -- even through a legitimate prescriber and compounding pharmacy -- verification will matter more, not less. The legitimate market needs quality oversight just as much as the gray market did.

Your free newsletter subscription is still active. You will get weekly updates on the regulatory landscape so you can stay informed without paying.

If you ever want premium back, it will be here.

Reuben

---

**Variant D: For all other cancellers (found enough / competitor / other)**

**Subject line:** A thank you (and one offer before you go)
**Preview text:** 25% off annual plan if you change your mind in the next 7 days

---

{first_name},

Thank you for being a premium subscriber. The revenue from subscribers like you directly funds independent peptide testing.

If you change your mind in the next 7 days:

**Annual plan at 25% off: $59.99/year** (normally $99.99, or $79.99 if you caught the early pricing)

[Reactivate at $59.99/year] {CTA button}

Either way, the free tools and newsletter are yours to keep. Thank you for supporting the mission.

Reuben

---

**Technical notes:**
- Variant selection is automated based on the cancellation reason tag from Email 1
- If no survey response (no tag), send Variant D (generic offer)
- All discount offers should be time-limited and enforced (do not honor expired offers -- it trains customers to wait)
- After Email 3, remove `win-back-sequence-active` tag
- Add `win-back-completed` tag
- Do NOT re-enter this sequence if they cancel again within 6 months -- send a single "we're sorry to see you go" email without the full sequence
- Track reactivation rate by variant for optimization

---

## 5. Weekly Newsletter Template

**Name:** Peptide Safety Digest
**Frequency:** Weekly (Tuesday morning, 7:00 AM ET)
**Platform:** Beehiiv
**Audience:** All subscribers (free + premium)
**Goal:** Maintain engagement, drive tool usage, build authority, create premium upgrade opportunities
**Target production time:** Under 1 hour per week using AI-assisted workflow

---

### Newsletter Structure

**Subject line formula:** [Peptide Safety Digest] {headline_of_the_week} + {one compelling detail}

Examples:
- [Peptide Safety Digest] FDA issues 3 new warning letters + the vendor rating that dropped this week
- [Peptide Safety Digest] New endotoxin data on compounded semaglutide + WADA 2026 update
- [Peptide Safety Digest] Major vendor shuts down + what to do if you ordered from them

---

**Section 1: The Lead (100-150 words)**
The single most important development of the week. Written in plain English. Could be regulatory, a vendor event, new testing data, or a safety alert.

Format:
> **This week:** [One-sentence summary of the top story]
>
> [2-3 paragraph explanation: what happened, why it matters, what consumers should do]
>
> [Link to full analysis or tool]

---

**Section 2: Regulatory Radar (75-100 words)**
Quick-hit updates on FDA, WADA, state-level enforcement, and Kennedy reclassification progress.

Format:
> **Regulatory Radar**
>
> - **FDA:** [Update or "No new actions this week"]
> - **States:** [Any state AG activity, enforcement, or legislative changes]
> - **WADA:** [Relevant only during list update periods or TUE guidance changes]
> - **Reclassification watch:** [Status of Category 1/2 formal rulemaking -- "Still no Federal Register notice as of {date}"]

---

**Section 3: Vendor Alert (50-100 words) -- PREMIUM TEASER**
Highlight 1-2 vendor rating changes from the week. Free subscribers see the vendor name and direction of change. Premium subscribers see the full detail.

Format:
> **Vendor Alert**
>
> - {Vendor_A}: Rating changed from {old} to {new}. [Premium members: see full test data] {premium_link}
> - {Vendor_B}: First endotoxin results published. [Results available in premium database] {premium_link}
>
> *Want the full vendor database with real-time alerts? [Upgrade to premium] {link}*

This section is the primary premium conversion driver in the newsletter. It shows tangible value that free users cannot access.

---

**Section 4: Peptide of the Week (100-150 words)**
Rotating deep dive on a specific peptide. Covers: what it is, evidence tier, key safety considerations, testing recommendations, regulatory status.

Rotation schedule (13-week cycle):
1. BPC-157
2. Semaglutide (compounded)
3. Tirzepatide (compounded)
4. TB-500 (Thymosin Beta-4)
5. Ipamorelin
6. CJC-1295
7. GHK-Cu
8. PT-141 (Bremelanotide)
9. Selank
10. Semax
11. MK-677 (Ibutamoren)
12. DSIP (Delta Sleep-Inducing Peptide)
13. AOD-9604

Format:
> **Peptide of the Week: {name}**
>
> **What it is:** [1 sentence]
> **Evidence tier:** [Clinical trials / animal studies only / in vitro only]
> **Key safety note:** [The one thing every user should know]
> **Current regulatory status:** [FDA status, Category 1/2 status, WADA status]
> **Testing recommendation:** [What to test for, which lab, approximate cost]
>
> [Link to full peptide guide on site]

---

**Section 5: New Research (50-75 words)**
One recent preprint or published study relevant to peptide safety, quality, or efficacy. Brief summary with link.

Format:
> **New Research**
>
> "{Study title}" -- {Journal/Preprint server}, {date}
>
> [2-3 sentence summary of findings and relevance to consumers]
>
> [Link to study or Peptide Checker analysis]

---

**Section 6: Quick Links + CTA**

> **Quick links:**
> - [Check a COA] | [Search a vendor] | [Regulatory tracker] | [Storage calculator]
>
> **Share this newsletter:** [Referral link -- Beehiiv built-in referral program]
>
> *Know someone buying peptides? Forward this email. Independent information saves people from bad vendors.*

---

### AI-Assisted Production Workflow (Under 1 Hour)

**Weekly schedule: Monday evening (30-45 minutes) + Tuesday morning (15 minutes)**

**Monday evening (30-45 minutes):**

1. **Source collection (10 minutes):**
   - Check FDA warning letters page (bookmarked): any new letters since last week?
   - Check Peptide Checker database: any vendor rating changes this week?
   - Check Google Scholar alerts for "peptide purity," "BPC-157," "compounded semaglutide" (pre-configured alerts deliver to inbox)
   - Check r/Peptides top posts for the week (3-minute scroll)
   - Check state AG press releases (bookmarked for top 10 states)

2. **AI draft generation (10 minutes):**
   - Paste source material into Claude/GPT with the following prompt template:

   ```
   You are drafting the weekly Peptide Safety Digest newsletter for Peptide Checker.

   Here are this week's inputs:
   - FDA updates: {paste}
   - Vendor rating changes: {paste from database}
   - New research: {paste abstract or summary}
   - Peptide of the week: {name from rotation schedule}
   - Any notable events: {paste}

   Write the newsletter following this exact structure:
   1. The Lead (100-150 words): Top story of the week
   2. Regulatory Radar (75-100 words): Quick-hit FDA/state/WADA/reclassification updates
   3. Vendor Alert (50-100 words): Rating changes with premium teaser
   4. Peptide of the Week (100-150 words): {peptide_name} -- what it is, evidence tier, safety note, regulatory status, testing recommendation
   5. New Research (50-75 words): Summary of {study}
   6. Quick Links: Standard footer

   Tone: Direct, data-driven, no hype. Write like a knowledgeable friend who happens to have a chemistry background. No emojis. No exclamation points. No "exciting news!" framing.

   Total length: 500-700 words.
   ```

3. **Edit and personalize (15-20 minutes):**
   - Review AI draft for accuracy (critical -- never publish health information without manual fact-check)
   - Add personal observations or context the AI cannot know
   - Verify all linked URLs work
   - Adjust vendor alert section to match actual database changes
   - Write the subject line manually (AI subject lines underperform human-written ones by 10-15% in A/B tests for health content)

**Tuesday morning (15 minutes):**

4. **Load into Beehiiv (10 minutes):**
   - Paste into Beehiiv editor
   - Format sections with headers
   - Add links and CTAs
   - Set premium teaser content blocks
   - Preview on mobile (60%+ of health newsletter opens are mobile)

5. **Schedule and verify (5 minutes):**
   - Schedule for 7:00 AM ET Tuesday
   - Send test email to yourself
   - Verify all links in test email
   - Confirm segmentation (free vs. premium content blocks)

**Total weekly time: 45-60 minutes**

---

### Newsletter Growth Targets

| Month | Subscribers | Open Rate | Click Rate | Premium Conversion |
|-------|------------|-----------|------------|-------------------|
| 1 | 200-500 | 55-65% | 8-12% | 1-2% |
| 3 | 500-1,500 | 45-55% | 6-10% | 2-3% |
| 6 | 1,500-5,000 | 40-50% | 5-8% | 2-4% |
| 12 | 5,000-15,000 | 35-45% | 4-7% | 3-5% |

---

## 6. Revenue Projections per Sequence

### 6.1 Industry Benchmarks Applied to Peptide Checker

| Metric | Industry Average | Health/SaaS Specific | Peptide Checker Estimate |
|--------|-----------------|---------------------|------------------------|
| Welcome sequence conversion to paid | 2-5% | 3-6% (health has higher urgency) | 3-5% |
| Welcome email open rate | 50-70% | 55-65% | 60% |
| Abandoned tool recovery to newsletter | 5-10% | 6-9% | 7% |
| Abandoned tool recovery to paid | 1-3% | 1-2% | 1.5% |
| Freemium to paid (upgrade sequence) | 2-5% | 3-7% (with usage-based trigger) | 5-8% |
| Win-back / resubscription rate | 5-10% | 8-12% (health = high switching cost) | 8-10% |
| Monthly subscriber churn | 5-8% | 5-7% | 6% |
| Newsletter-to-premium conversion (ongoing) | 1-3% per month | 1-2% | 1.5% |

Sources: [Klaviyo 2026 Email Marketing Benchmarks](https://www.klaviyo.com/products/email-marketing/benchmarks), [First Page Sage SaaS Freemium Conversion Rates 2026](https://firstpagesage.com/seo-blog/saas-freemium-conversion-rates/), [Baremetrics Win-Back Email Guide](https://baremetrics.com/blog/winback-email), [Rejoiner Abandoned Cart Statistics](https://www.rejoiner.com/resources/abandoned-cart-email-statistics)

### 6.2 Revenue Per Sequence (Month 6 Projections)

Assumptions at Month 6:
- 5,000 newsletter subscribers (per SEO strategy growth targets)
- 20,000 monthly site visitors
- 500 premium subscribers ($9.99/mo)
- 2,000 free-tier tool users/month
- 6% monthly churn on premium

**Welcome Sequence:**

| Metric | Value |
|--------|-------|
| New subscribers entering sequence/month | 800 |
| Sequence completion rate | 70% (560 complete all 5 emails) |
| Conversion to premium | 4% of completers = 22 new premium subs/month |
| Revenue per conversion | $9.99/month, LTV = $166.50 (at 6% monthly churn = ~16.7 month avg lifetime) |
| Monthly revenue generated | $219.78 (first month) |
| Annual LTV generated per month of new cohort | $3,663 |
| **Annual revenue from this sequence** | **$43,956** |

**Abandoned Tool Sequence:**

| Metric | Value |
|--------|-------|
| Tool users without account/month | 1,200 (60% of 2,000 tool users) |
| Email capture rate at tool use | 40% = 480 enter sequence |
| Newsletter conversion | 7% = 34 new newsletter subs/month |
| Direct premium conversion | 1.5% = 7 new premium subs/month |
| Monthly revenue generated | $69.93 |
| **Annual LTV generated** | **$13,986** |

**Upgrade Sequence:**

| Metric | Value |
|--------|-------|
| Free users hitting 5+ uses/month | 300 (15% of 2,000 free users) |
| Conversion to premium | 6% = 18 new premium subs/month |
| Monthly revenue generated | $179.82 |
| **Annual LTV generated** | **$35,964** |

**Win-Back Sequence:**

| Metric | Value |
|--------|-------|
| Monthly churn (cancellations) | 30 (6% of 500 subscribers) |
| Win-back resubscription rate | 10% = 3 recovered/month |
| Average discount on resubscription | 20% (blended across variants) |
| Monthly revenue recovered | $23.97 (at avg $7.99/mo blended) |
| **Annual LTV recovered** | **$4,794** |

**Weekly Newsletter (Ongoing Premium Conversion):**

| Metric | Value |
|--------|-------|
| Free newsletter subscribers (non-premium) | 4,500 |
| Monthly conversion to premium from newsletter | 1.5% = 67.5 per month |
| But overlap with other sequences | ~50% are already in another sequence |
| Incremental conversions | ~34/month |
| Monthly revenue generated | $339.66 |
| **Annual LTV generated** | **$67,932** |

### 6.3 Total Revenue Attribution by Sequence

| Sequence | Annual LTV Generated | % of Total | Priority |
|----------|---------------------|-----------|----------|
| Weekly Newsletter (ongoing) | $67,932 | 41% | **Highest ROI -- consistent, low effort** |
| Welcome Sequence | $43,956 | 26% | **Second highest -- first impression matters** |
| Upgrade Sequence | $35,964 | 22% | High -- targets highest-intent users |
| Abandoned Tool Sequence | $13,986 | 8% | Medium -- feeds the newsletter funnel |
| Win-Back Sequence | $4,794 | 3% | Low absolute value, but nearly free to run |
| **Total** | **$166,632** | 100% | |

**Key insight:** The weekly newsletter is the single most valuable email asset. It drives 41% of projected email revenue through steady, low-pressure premium conversion. The welcome sequence is second at 26%, making the first 14 days the most critical window. Invest the most A/B testing effort into these two.

### 6.4 LTV Modeling

| Scenario | Monthly Churn | Avg Lifetime (months) | LTV at $9.99/mo | LTV at $6.67/mo (annual) |
|----------|--------------|----------------------|------------------|--------------------------|
| Optimistic | 4% | 25 | $249.75 | $166.75 |
| Base case | 6% | 16.7 | $166.83 | $111.39 |
| Pessimistic | 8% | 12.5 | $124.88 | $83.38 |

Annual plan subscribers have structurally lower churn (they committed upfront) and should be modeled at 3-4% monthly churn equivalent, producing LTV of $166-$250.

**Break-even CAC:** At base-case LTV of $166.83 and a target LTV:CAC ratio of 8:1, maximum CAC is ~$20.85 per subscriber. Since email sequences have near-zero marginal cost (the subscriber is already in the system), all email-driven conversions have effectively infinite LTV:CAC ratios. This is why email is the highest-ROI channel.

### 6.5 Year 1 vs. Year 2 Projections

| Metric | Year 1 (Months 4-12) | Year 2 |
|--------|----------------------|--------|
| Newsletter subscribers (end of year) | 5,000-8,000 | 15,000-25,000 |
| Premium subscribers (end of year) | 500-800 | 2,000-3,500 |
| Email-attributed premium revenue | $60K-$100K | $240K-$420K |
| Email-attributed % of total revenue | 40-50% | 35-45% |

Email's share of total revenue decreases in Year 2 as testing referrals and vendor certification revenue grow, but absolute email revenue more than triples.

---

## 7. Technical Setup

### 7.1 Beehiiv Automation Capabilities

Beehiiv (Scale plan, $99/month) provides the automation infrastructure needed for all five sequences.

**What Beehiiv handles natively:**

| Feature | Capability | Notes |
|---------|-----------|-------|
| Automation sequences | Multi-step email flows with time delays | Supports day-based delays between emails |
| Trigger types | Subscriber signup, tag addition, segment entry | Cannot trigger from email opens/clicks natively |
| Segmentation | By tags, custom fields, engagement, survey responses, referral count | Dynamic segments update daily |
| A/B testing | Subject lines, send times, content variants | Built-in with statistical significance reporting |
| Newsletter templates | Reusable templates with sections | Supports premium content blocks |
| Referral program | Built-in referral tracking and rewards | Use for newsletter growth |
| AI writing assistant | Draft generation within editor | Useful for newsletter production workflow |
| Analytics | Open rate, click rate, subscriber growth, revenue attribution | Integrates with Stripe |

**What requires workarounds:**

| Limitation | Workaround |
|-----------|-----------|
| Cannot trigger automation from email clicks | Use Zapier: email click -> Zapier -> add tag in Beehiiv -> tag triggers automation |
| No abandoned cart/tool trigger | Webhook from Peptide Checker app -> Zapier -> Beehiiv tag |
| No usage-count trigger (5+ tool uses) | Peptide Checker app tracks usage, fires webhook at threshold -> Zapier -> Beehiiv tag |
| Cancellation trigger | Stripe cancellation webhook -> Zapier -> Beehiiv tag |
| Dynamic content (vendor names, results) | Use Beehiiv custom fields populated via API; for complex dynamic content, generate the email externally and send via Beehiiv API |

**Zapier is the glue.** Budget $29-$49/month for Zapier Starter/Professional to connect Peptide Checker app events to Beehiiv automation triggers.

### 7.2 Tagging and Segmentation Strategy

**Tag Taxonomy:**

```
SOURCE TAGS (how they found us):
  source-organic-search
  source-reddit
  source-twitter
  source-newsletter-referral
  source-direct
  source-youtube

SEQUENCE TAGS (which automation they are in):
  welcome-sequence-active
  abandoned-tool-sequence-active
  upgrade-sequence-active
  win-back-sequence-active
  trial-active

STATUS TAGS (where they are in the funnel):
  free-user
  premium-subscriber-monthly
  premium-subscriber-annual
  trial-active
  trial-expired
  churned

ENGAGEMENT TAGS (behavioral):
  coa-uploaded            (used COA checker)
  vendor-search-active    (searched vendors)
  high-intent             (3+ tool uses in 7 days)
  engaged-reply           (replied to an email)
  pdf-downloaded          (downloaded lead magnet)

INTEREST TAGS (what peptides they care about):
  interest-bpc157
  interest-semaglutide
  interest-tirzepatide
  interest-glp1
  interest-tb500
  interest-ipamorelin
  interest-ghk-cu
  interest-athlete        (searched WADA-related content)

CHURN REASON TAGS (from cancellation survey):
  churn-reason-found-enough
  churn-reason-price
  churn-reason-stopped
  churn-reason-quality
  churn-reason-competitor
  churn-reason-other

SEQUENCE COMPLETION TAGS:
  welcome-sequence-completed-free
  welcome-sequence-completed-paid
  upgrade-sequence-completed-free
  upgrade-sequence-completed-paid
  win-back-completed
  win-back-recovered
```

**Dynamic Segments (auto-updating daily in Beehiiv):**

| Segment | Definition | Use |
|---------|-----------|-----|
| High-intent free users | `free-user` + `high-intent` + NOT `upgrade-sequence-active` | Upgrade sequence entry |
| Premium at risk | `premium-subscriber-*` + no opens in 30 days | Pre-churn intervention |
| Newsletter-only engaged | `free-user` + opened 3+ of last 5 newsletters + NOT `upgrade-sequence-*` | Soft upgrade nudge in newsletter |
| New subscribers (7 days) | Subscribed within last 7 days + `welcome-sequence-active` | Exclude from other promotions |
| Semaglutide interested | `interest-semaglutide` OR `interest-glp1` | Targeted content in newsletter |
| Athletes | `interest-athlete` | WADA-specific content |
| Win-back eligible | `churned` + NOT `win-back-sequence-active` + cancelled 1-90 days ago | Win-back sequence entry |

### 7.3 A/B Testing Plan

**Priority 1: Welcome Email 1 Subject Lines (Test first)**

| Variant | Subject Line |
|---------|-------------|
| A (Control) | Your free COA checklist is inside (+ what we found testing 450 vendors) |
| B | The 7-point checklist that catches 90% of fake peptide COAs |
| C | 60% of peptide vendors fail testing. Here is how to find the good ones. |
| D | Welcome to Peptide Checker -- your COA checklist is ready |

Test: 4 variants, 25% each. Run for 500 subscribers minimum per variant. Measure open rate + click rate (not just opens).

**Priority 2: Upgrade Sequence Email 3 CTAs**

| Variant | CTA |
|---------|-----|
| A (Control) | Subscribe now -- $9.99/month |
| B | Start protecting your peptide purchases -- $9.99/month |
| C | See your vendor's full test history -- $9.99/month |
| D | Join 247 subscribers who verify before they buy |

Test: Measure click-through rate and actual conversion (Stripe checkout completion).

**Priority 3: Welcome Email 5 Price Presentation**

| Variant | Approach |
|---------|----------|
| A (Control) | $9.99/month, positioned as "less than one bad vial" |
| B | $9.99/month with annual option prominently shown ($79.99/year) |
| C | Lead with annual: $79.99/year ($6.67/month) with monthly as alternative |
| D | Free 7-day trial, then $9.99/month |

Test: Measure conversion rate AND average revenue per subscriber (ARPS). Variant D may get higher conversion but lower ARPS if trial users do not convert.

**Priority 4: Newsletter Premium Teaser Format**

| Variant | Format |
|---------|--------|
| A (Control) | Vendor name + direction + "Premium members see full data" |
| B | Vendor name + one specific data point blurred + "Unlock full results" |
| C | "3 vendor ratings changed this week. See which ones." + premium link |

Test: Measure premium upgrade clicks from newsletter.

**Testing cadence:** Run one A/B test per sequence at a time. Each test needs minimum 500 subscribers per variant to reach statistical significance. At early subscriber counts (<2,000), run tests for 4-6 weeks. At scale (5,000+), tests can resolve in 1-2 weeks.

### 7.4 Deliverability Best Practices for Health Content

Health and supplement content faces elevated spam filter scrutiny. These practices are non-negotiable.

**Authentication (set up before sending a single email):**

- **SPF record:** Configure for Beehiiv's sending IPs
- **DKIM signing:** Enable via Beehiiv custom domain settings
- **DMARC policy:** Start with `p=none` for monitoring, move to `p=quarantine` after 30 days of clean sending
- **Custom sending domain:** Use `mail.peptidechecker.com` or `digest.peptidechecker.com` -- never send from a free email provider

**Content rules for health email (avoid spam filters):**

| Do | Do Not |
|----|--------|
| Use specific data points ("7-14% purity") | Use vague health claims ("miracle results") |
| Link to published studies (JMIR, PubMed) | Use urgency language without substance ("ACT NOW") |
| Write in plain language at 8th-grade reading level | Use ALL CAPS in subject lines or body |
| Include a physical mailing address (CAN-SPAM) | Use excessive exclamation points |
| Provide clear unsubscribe in every email | Use spam trigger words: "guaranteed," "risk-free," "100% safe," "miracle," "cure" |
| Maintain 60%+ text-to-image ratio | Send image-heavy emails with minimal text |
| Keep subject lines under 50 characters | Use deceptive subject lines ("Re:" or "Fwd:" when not a reply) |
| Warm up new sending domain gradually | Blast full list from a new domain on Day 1 |

**Health-specific content warnings:**

The following phrases WILL trigger spam filters in health email:

- "Cure," "treat," "heal," "remedy" (even in educational context)
- "FDA approved" (unless linking to actual FDA approval documentation)
- "Weight loss guaranteed" or any guaranteed health outcome
- "Doctor recommended" without specific attribution
- "Buy now," "limited supply," "act fast" combined with health claims
- Drug names in subject lines (semaglutide, tirzepatide) -- use sparingly and only with educational framing

**Safe alternatives:**

| Instead of | Use |
|-----------|-----|
| "BPC-157 cures inflammation" | "BPC-157: what the clinical evidence shows" |
| "Guaranteed purity" | "Independently verified purity data" |
| "FDA approved peptides" | "FDA regulatory status of peptides in 2026" |
| "Buy safe peptides" | "How to evaluate peptide vendor quality" |
| "Miracle recovery peptide" | "BPC-157 clinical trial results and evidence tier" |

**Domain warm-up schedule (for new peptidechecker.com sending domain):**

| Week | Daily Send Volume | Target |
|------|------------------|--------|
| 1 | 50 | Send to most engaged existing contacts only |
| 2 | 100-200 | Add next engagement tier |
| 3 | 500 | Expand to full engaged segment |
| 4 | 1,000+ | Full list sends begin |
| 5+ | Full list | Monitor and maintain |

**Ongoing list hygiene:**

- Remove subscribers who have not opened any email in 90 days (suppress, do not delete -- they can re-engage via website)
- Monitor bounce rate weekly (keep below 2%)
- Monitor spam complaint rate (keep below 0.1%)
- Run re-engagement campaign at 60 days of inactivity before suppressing at 90 days
- Never purchase email lists -- every subscriber must be opt-in

**Deliverability monitoring:**

- Check Google Postmaster Tools weekly for domain reputation
- Monitor Beehiiv's built-in deliverability metrics
- Send seed emails to Gmail, Outlook, Yahoo, and Apple Mail accounts before each major campaign
- If inbox placement drops below 90%, pause sending and investigate before continuing

---

## Appendix A: Email Calendar Overview

| Day | Sequence | Email | Purpose |
|-----|----------|-------|---------|
| 0 | Welcome | Email 1 | Welcome + COA checklist |
| 0 | Abandoned Tool | Email 1 (1hr) | COA results delivery |
| 2 | Welcome | Email 2 | The purity problem |
| 2 | Abandoned Tool | Email 2 | 3 things vendors hide |
| 5 | Welcome | Email 3 | How to read a COA |
| 5 | Abandoned Tool | Email 3 | Free trial offer |
| 7 | Newsletter | Weekly digest | Ongoing engagement |
| 9 | Welcome | Email 4 | 450 vendors data teaser |
| 14 | Welcome | Email 5 | Soft sell premium |
| T+0 | Upgrade | Email 1 | Usage milestone |
| T+3 | Upgrade | Email 2 | Social proof |
| T+7 | Upgrade | Email 3 | Cost comparison |
| T+14 | Upgrade | Email 4 | Annual offer |
| C+0 | Win-Back | Email 1 | Cancellation survey |
| C+3 | Win-Back | Email 2 | What you will miss |
| C+7 | Win-Back | Email 3 | Segmented offer |

**Conflict resolution rules:**
1. A subscriber should never receive more than 2 emails from Peptide Checker in a single day
2. Welcome sequence takes priority over all other sequences
3. Newsletter sends regardless of active sequences (it is the core product)
4. Upgrade sequence pauses during welcome sequence (users should complete welcome first)
5. Win-back sequence overrides upgrade sequence (if someone cancels during upgrade, enter win-back)

---

## Appendix B: Sequence Metrics Dashboard

Track these metrics weekly in a simple spreadsheet or Beehiiv analytics:

**Per-sequence metrics:**

| Metric | Welcome | Abandoned | Upgrade | Win-Back | Newsletter |
|--------|---------|-----------|---------|----------|-----------|
| Emails sent | | | | | |
| Open rate (per email) | | | | | |
| Click rate (per email) | | | | | |
| Conversion to premium | | | | | |
| Revenue attributed | | | | | |
| Unsubscribe rate | | | | | |

**Monthly aggregate metrics:**

| Metric | Target |
|--------|--------|
| Total new email subscribers | 800+/month by Month 6 |
| Email-attributed premium conversions | 100+/month by Month 6 |
| Email-attributed MRR | $1,000+/month by Month 6 |
| Overall email list growth rate | 15-20%/month |
| Premium subscriber churn rate | <6%/month |
| Email deliverability rate | >95% |
| Spam complaint rate | <0.1% |

---

## Appendix C: Research Sources

- [Klaviyo 2026 Email Marketing Benchmarks](https://www.klaviyo.com/products/email-marketing/benchmarks)
- [Sequenzy SaaS Email Marketing Benchmarks](https://www.sequenzy.com/blog/saas-email-marketing-benchmarks)
- [First Page Sage SaaS Freemium Conversion Rates 2026](https://firstpagesage.com/seo-blog/saas-freemium-conversion-rates/)
- [Rejoiner Abandoned Cart Email Statistics](https://www.rejoiner.com/resources/abandoned-cart-email-statistics)
- [Klaviyo Abandoned Cart Benchmark Report](https://www.klaviyo.com/blog/abandoned-cart-benchmarks)
- [Baremetrics SaaS Win-Back Emails](https://baremetrics.com/blog/winback-email)
- [Recurly Customer Win-Back Strategies](https://recurly.com/blog/customer-winback-strategies-for-subscriptions/)
- [Mailmend Win-Back Campaign Statistics](https://mailmend.io/blogs/win-back-campaign-statistics)
- [Moosend Email Deliverability Guide 2026](https://moosend.com/blog/email-deliverability/)
- [Beehiiv Segmentation Features](https://www.beehiiv.com/features/segmentation)
- [Beehiiv Automation Features](https://www.beehiiv.com/features/automations)
- [Beehiiv AI Newsletter Generator](https://www.beehiiv.com/features/artificial-intelligence)
- [Hoppy Copy AI Newsletter Automation](https://www.hoppycopy.co/blog/how-to-automate-90-of-your-newsletter)

---

*Email nurture sequences designed 2026-03-24 | Based on HUMMBL peptide-checker strategic documents + industry conversion benchmarks*
*This is an internal strategic document. Not for public distribution without review.*
