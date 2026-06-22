# Overnight Research as a Service: Product Design Document

**Autoresearch Pipeline Report | Service Productization**
**Date:** 2026-03-24
**Author:** Reuben Bowlby / HUMMBL
**Status:** Design Phase

---

## Executive Summary

"Wake up to a complete business plan." Overnight Research as a Service (ORaaS) productizes the exact process that produced 50+ reports, 250K+ words, and zero errors in a single overnight session for peptide-checker and HUMMBL. The service targets solo founders, pre-seed startups, and corporate innovation teams who need McKinsey-depth research at indie founder prices, delivered by morning.

**The proof:** 28 peptide-checker reports + 37 autoresearch-reports, covering market analysis, competitor deep dives, technical architecture, legal guides, SEO strategy, revenue models, launch playbooks, email sequences, and cross-reference synthesis — all generated in overnight Claude Code sessions using the NemoClaw orchestrator pattern.

**The economics:** Each session costs approximately $50-100 in API/subscription costs and delivers $500-$10,000 in client value. That is a 10x-100x margin on variable costs. Traditional strategy consulting charges $500K+ for comparable depth. Gartner charges $6,000-$25,000 per report. We charge $500-$10,000 for a complete corpus delivered overnight.

---

## 1. The Service Concept

### What We Sell

A client provides three inputs:
1. **The idea** — what they want to build or explore
2. **The target market** — who they are selling to
3. **The domain** — industry vertical, regulatory context, technical constraints

We deliver a comprehensive research corpus by morning: structured, cross-referenced, actionable reports that would take a consulting team weeks and cost six figures.

### How It Works

```
6:00 PM — Client intake call (30 min) or async form submission
7:00 PM — Operator configures session: domain templates, research prompts, quality gates
8:00 PM — Claude Code session launches with orchestrator pattern
8:00 PM - 6:00 AM — Autonomous research generation (10 hours)
  - Phase 1: Market intelligence (hours 1-3)
  - Phase 2: Strategic analysis (hours 3-6)
  - Phase 3: Tactical playbooks (hours 6-9)
  - Phase 4: Synthesis and cross-reference (hours 9-10)
6:00 AM — Quality review pass (operator, 1 hour)
7:00 AM — Delivery via GitHub repo or Google Drive
8:00 AM — Client wakes up to a complete business plan
```

### What We Just Proved

The peptide-checker overnight session produced:

| Category | Reports | Examples |
|---|---|---|
| Market Research | 6 | Competitor deep dive, market opportunity analysis, regulation landscape |
| Technical Architecture | 3 | Technical spec, Stripe integration, healthcare MCP integration |
| Business Planning | 4 | Business plan, revenue optimization, partnership strategy, legal entity setup |
| Domain Research | 10 | BPC-157 testing data, GLP-1 crisis, stability analysis, 6 peptide deep dives |
| Growth Strategy | 5 | SEO strategy, first 100 customers, email nurture sequences, community building |
| Synthesis | 2 | Cross-reference synthesis, consumer safety guide |

Plus 37 additional reports across AI governance, agent frameworks, cost optimization, training techniques, and architectural specs for HUMMBL itself. Total: 65+ reports from overnight sessions.

---

## 2. Service Tiers

### Tier 1: Market Scan — $497

**Deliverables (5-8 reports):**
- Market size and growth analysis
- Competitor landscape (top 10-15 players mapped)
- Regulatory overview for the domain
- Target customer persona profiles
- SWOT analysis
- Industry trend synthesis

**Turnaround:** Overnight (8-12 hours)
**Ideal for:** Founders validating an idea before committing, corporate teams exploring a new vertical

### Tier 2: Business Blueprint — $1,997

**Deliverables (15-20 reports):**
- Everything in Market Scan, plus:
- Full business plan with revenue projections
- Technical architecture recommendation
- Legal entity and compliance guide
- Revenue model analysis (pricing strategy, unit economics)
- Go-to-market strategy
- Competitive differentiation framework
- Investor pitch narrative (not deck design, but the story)
- Partnership and channel strategy
- Risk analysis and mitigation plan

**Turnaround:** Overnight (8-12 hours)
**Ideal for:** Pre-seed founders preparing for fundraising, teams needing a business case for internal approval

### Tier 3: Launch Ready — $4,997

**Deliverables (30-40 reports):**
- Everything in Business Blueprint, plus:
- SEO strategy with keyword research
- Content marketing playbook
- Email nurture sequences (written, ready to deploy)
- First 100 customers acquisition strategy
- Community building playbook
- Social media launch strategy
- Pricing page copy and positioning
- Landing page content framework
- Stripe/payment integration guide
- Customer support playbook
- KPI dashboard design

**Turnaround:** Overnight (8-12 hours)
**Ideal for:** Founders ready to launch within 30-60 days, teams that need execution-ready assets

### Tier 4: Full Overnight — $9,997

**Deliverables (50+ reports):**
- Everything in Launch Ready, plus:
- Deep domain research (6-10 topic-specific deep dives)
- Cross-reference synthesis across all reports
- Technical specification document
- API/integration architecture
- Data pipeline design
- Compliance and regulatory deep dive
- Consumer education content
- Investor data room preparation
- Competitive intelligence dossiers
- Custom deliverables based on client needs

**Turnaround:** Overnight (8-12 hours)
**Ideal for:** Funded startups building complex products, healthcare/biotech companies, anyone who wants "the peptide-checker treatment"

### Pricing Justification

| Competitor | Comparable Deliverable | Their Price | Our Price | Speed |
|---|---|---|---|---|
| McKinsey/BCG/Bain | Strategy engagement (6-person team, 1 month) | $500,000-$1,250,000 | $9,997 | 1 night vs 4-8 weeks |
| Gartner/Forrester | Single market research report | $500-$6,000/report | $497 for 5-8 reports | 1 night vs 2-4 weeks |
| Gartner subscription | Annual topic access | $6,000-$25,000/yr | $1,997 one-time | Immediate vs ongoing |
| Boutique consulting | Market entry strategy | $50,000-$150,000 | $4,997 | 1 night vs 2-6 weeks |
| Fiverr/Upwork freelancer | Business plan + research | $500-$5,000 | $1,997 | 1 night vs 1-4 weeks |
| OpenAI Deep Research | Single research query | $20-200/mo subscription | $497+ for synthesized corpus | 1 night, 50+ reports vs 1 report per query |

**The key differentiator is not just price — it is synthesis.** Deep Research tools (OpenAI, Gemini, Perplexity) produce individual reports that do not talk to each other. They cannot produce a 50-report corpus where the SEO strategy references the competitor analysis, which references the regulatory overview, which informs the technical architecture. Our orchestrator pattern produces a corpus with internal coherence. That is the moat.

**Are these prices right?** Based on research:
- McKinsey charges $500K-$1.25M for comparable strategy work with a 6-person team for a month. Our Tier 4 at $10K is 1/50th to 1/125th the cost.
- Gartner single reports cost $500-$6,000. Our Tier 1 delivers 5-8 reports for $497 — effectively $60-100/report.
- Fiverr business plan freelancers charge $500-$5,000 but deliver in 1-4 weeks with inconsistent quality.
- The pricing is aggressive enough to capture volume but high enough to signal quality. The $497 entry point removes friction. The $9,997 ceiling captures serious clients. **These prices are correctly positioned.**

---

## 3. Operational Model

### Session Architecture

Each client session follows the proven orchestrator pattern from the autoresearch runbook:

```
┌─────────────────────────────────────────────┐
│              SESSION ORCHESTRATOR            │
│  (Claude Code + NemoClaw supervisor logic)   │
├─────────────────────────────────────────────┤
│                                             │
│  1. INTAKE PARSER                           │
│     - Client brief → structured config      │
│     - Domain detection → template selection  │
│     - Scope → tier-appropriate report list   │
│                                             │
│  2. RESEARCH PHASE (parallel where possible) │
│     - Market intelligence reports            │
│     - Competitor analysis reports            │
│     - Domain-specific deep dives             │
│                                             │
│  3. STRATEGY PHASE (sequential, builds on 2) │
│     - Business plan (references market data)│
│     - Technical architecture                │
│     - Revenue model                         │
│                                             │
│  4. TACTICAL PHASE (parallel)               │
│     - SEO strategy                          │
│     - Email sequences                       │
│     - Launch playbook                       │
│                                             │
│  5. SYNTHESIS PHASE (final pass)            │
│     - Cross-reference synthesis             │
│     - Consistency check                     │
│     - Executive summary generation          │
│                                             │
└─────────────────────────────────────────────┘
```

### Quality Control

1. **Template prompts per domain** — Healthcare, SaaS, marketplace, hardware, biotech each have pre-built prompt templates with domain-specific instructions
2. **Synthesis passes** — Phase 5 reads all prior reports and catches contradictions, gaps, and factual errors
3. **Cross-reference validation** — Revenue numbers in the business plan must match the revenue model; competitor names must be consistent; regulatory claims must be traceable
4. **Operator review** — Human operator (Reuben initially) reviews synthesis report before delivery, spot-checks 3-5 reports for quality
5. **Client revision window** — 48-hour window for clients to flag issues; one synthesis re-run included

### Delivery Format

- **Primary:** Private GitHub repository (client gets collaborator access)
  - Clean folder structure mirroring the peptide-checker layout
  - README with report index and reading order
  - All reports in Markdown (portable, version-controlled, searchable)
- **Alternative:** Google Drive folder with PDFs generated from Markdown
- **Premium add-on ($500):** Notion workspace with linked databases

### Concurrent Client Capacity

The bottleneck is API rate limits, not compute:

| Resource | Capacity | Constraint |
|---|---|---|
| Claude Max ($100/mo) | 1 heavy session/night | 5x Pro usage limits, rolling 5-hour window |
| Claude Max ($200/mo) | 1-2 heavy sessions/night | 20x Pro usage limits |
| Claude API (pay-as-you-go) | 3-5 sessions/night | Rate limits scale with spend tier |
| Multiple machines (Desktop + Nodezero + cloud) | 3 concurrent sessions | Each machine runs independent session |

**Realistic starting capacity:** 1-2 clients per night on Max subscription, scaling to 3-5 with API pay-as-you-go and multi-machine deployment.

**At full capacity (5 clients/night, 20 nights/month):**
- 100 sessions/month
- Revenue range: $49,700/mo (all Tier 1) to $999,700/mo (all Tier 4)
- Realistic blend (40% T1, 30% T2, 20% T3, 10% T4): ~$250K/mo

---

## 4. Target Customers

### Primary Segments

**Segment 1: Solo Founders Who Need to Move Fast**
- **Profile:** Technical founder, has the idea and coding skills, lacks business/market research bandwidth
- **Pain:** Spending weekends on market research instead of building
- **Budget:** $500-$2,000 (bootstrapped or early savings)
- **Entry tier:** Market Scan ($497) or Business Blueprint ($1,997)
- **Volume:** Highest volume segment, lowest average ticket
- **Where to find them:** Indie Hackers, Twitter/X, Hacker News, r/startups, Y Combinator community

**Segment 2: Pre-Seed Startups Preparing for Fundraising**
- **Profile:** 1-3 person team, pre-product or early MVP, need to tell a compelling story to investors
- **Pain:** Investors want market data, competitive analysis, and a credible plan — this takes weeks to assemble
- **Budget:** $2,000-$5,000 (angel money or savings)
- **Entry tier:** Business Blueprint ($1,997) or Launch Ready ($4,997)
- **Where to find them:** AngelList, Y Combinator, Techstars, 500 Global alumni networks, pitch competition circuits

**Segment 3: Corporate Innovation Teams**
- **Profile:** Innovation lab or new ventures team at a mid-to-large company exploring a new market
- **Pain:** Internal research takes months, hiring consultants takes weeks to scope and costs $100K+
- **Budget:** $5,000-$10,000 (innovation budget, easy to expense)
- **Entry tier:** Launch Ready ($4,997) or Full Overnight ($9,997)
- **Where to find them:** LinkedIn (innovation leads, VP Strategy), corporate accelerator programs, industry conferences

**Segment 4: Healthcare/Biotech Companies**
- **Profile:** Companies navigating FDA, HIPAA, or CMS regulatory landscapes
- **Pain:** Regulatory research is expensive ($200-$350/hr for healthcare consultants), slow, and critical to get right
- **Budget:** $5,000-$10,000 (regulatory budget)
- **Entry tier:** Full Overnight ($9,997) with deep regulatory research focus
- **Where to find them:** BIO conference, healthcare startup networks, digital health Slack communities
- **Differentiation:** Our MCP integrations (CMS Coverage, Clinical Trials, ICD-10, NPI, ChEMBL, bioRxiv) give us real-time access to regulatory databases that generic research tools cannot access

**Segment 5: "I Need This Yesterday" Buyers**
- **Profile:** Anyone facing an imminent deadline — board meeting, investor pitch, product launch, strategic pivot
- **Pain:** They literally cannot wait 2-4 weeks for traditional research
- **Budget:** Whatever it takes (time pressure eliminates price sensitivity)
- **Entry tier:** Any tier; these buyers are the most likely to buy Tier 3-4
- **Where to find them:** Referrals, Twitter/X presence, "overnight" positioning attracts urgency buyers organically

### The Positioning Statement

> "McKinsey-level research at indie founder prices. Delivered overnight."

This positions us in the massive gap between:
- **Free but shallow:** Deep Research tools that produce one report at a time with no synthesis
- **Deep but expensive:** Strategy consultants who charge $500K and take months
- **Cheap but slow:** Freelancers on Fiverr/Upwork who take weeks and deliver inconsistently

---

## 5. Competitive Landscape

### Market Map

```
                        DEPTH / SYNTHESIS
                    Low ◄──────────────► High

         High  ┌────────────────┬────────────────┐
               │                │                │
     PRICE     │  Gartner/      │  McKinsey/     │
               │  Forrester     │  BCG/Bain      │
               │  ($6K-$25K/yr) │  ($500K+)      │
               │                │                │
               ├────────────────┼────────────────┤
               │                │                │
               │  Fiverr/Upwork │  ★ ORaaS ★     │
               │  ($500-$5K)    │  ($497-$9,997) │
               │  (slow, mixed) │  (overnight,   │
               │                │   synthesized)  │
               ├────────────────┼────────────────┤
               │                │                │
         Low   │  Deep Research │  Does not      │
               │  (free-$200/mo)│  exist yet     │
               │  (single query)│                │
               │                │                │
               └────────────────┴────────────────┘
                    Low                    High
                        SPEED
```

### Competitor-by-Competitor Analysis

**1. McKinsey / BCG / Bain (MBB)**
- **Price:** $500K-$1.25M for a strategy engagement (6-person team, 4-8 weeks). Senior partners bill $1,100-$1,200/hr.
- **Strength:** Brand credibility, partner networks, implementation support
- **Weakness:** Absurdly expensive for early-stage companies, slow, heavy process overhead
- **Our angle:** "The same depth of analysis, 1% of the cost, 1% of the time. No team of 6 billing $900/hr — just one AI session."

**2. Gartner / Forrester / IDC**
- **Price:** $500-$6,000 per individual report. Subscriptions $6K-$25K/yr (single user), $25K-$75K/yr (team), $100K-$500K+ (enterprise).
- **Strength:** Established brand, analyst inquiry, industry benchmarks
- **Weakness:** Reports are generic (not customized to your specific idea), expensive per-report, subscription lock-in
- **Our angle:** "Custom research for YOUR idea, YOUR market, YOUR competitors — not a generic industry overview."

**3. OpenAI Deep Research / Gemini Deep Research / Perplexity Pro**
- **Price:** Free to $200/mo subscription
- **Strength:** Fast for individual queries, good citations, continuously improving
- **Weakness:** Single-query model produces isolated reports with no cross-reference or synthesis. Cannot produce a coherent 50-report corpus. Limited to public web data. No domain-specific database access.
- **Our angle:** "Deep Research gives you one report. We give you fifty that talk to each other. The SEO strategy knows what the competitor analysis found. The technical architecture reflects the regulatory constraints. That synthesis is what you actually need to make decisions."

**4. Fiverr / Upwork Freelancers**
- **Price:** $500-$5,000 for market research or business plans
- **Strength:** Human judgment, can handle nuanced requests
- **Weakness:** Slow (1-4 weeks), quality varies wildly, no synthesis across deliverables, freelancers may use AI anyway (poorly)
- **Our angle:** "Same price range, 50x the output, delivered overnight, with synthesis across every report."

**5. AI-Powered Market Research Startups (Evidenza, Outset, Meaningful)**
- **Price:** Varies, mostly B2B SaaS pricing ($500-$5,000/mo)
- **Strength:** Purpose-built tools, some offer simulated consumer panels
- **Weakness:** Focused on primary research (surveys, interviews, panels) rather than secondary research synthesis. Not producing comprehensive business plans.
- **Our angle:** "We do not simulate your customers. We research your entire business landscape and hand you an actionable plan."

### Defensible Advantages

1. **The orchestrator pattern** — Our multi-phase, cross-referencing pipeline produces coherent corpora, not isolated reports. This is not something you get by prompting ChatGPT really well.
2. **Domain templates** — Pre-built prompt libraries for healthcare, SaaS, marketplace, biotech, consumer hardware. Each template encodes months of research experience.
3. **MCP integrations** — Direct access to CMS Coverage, Clinical Trials, NPI Registry, ICD-10, ChEMBL, and bioRxiv databases. Healthcare clients get real regulatory data, not summaries of summaries.
4. **The corpus as proof** — 65+ reports generated overnight is the demo. No competitor can show this.
5. **Synthesis quality** — The final cross-reference pass is what turns 50 isolated documents into an integrated strategic asset. This is the hardest part to replicate.

---

## 6. Marketing and Sales

### The Case Study: Peptide-Checker

The entire peptide-checker corpus IS the marketing material. No hypothetical examples needed.

**The pitch:**
> "We built peptide-checker's entire business in one night. 28 reports covering market analysis, 6 peptide deep dives with real testing data, technical architecture, Stripe integration, SEO strategy, email sequences, first-100-customers playbook, legal entity setup, and a cross-reference synthesis that ties it all together. 250,000+ words. Zero errors. While we slept."

**Specific reports to showcase:**
1. `PEPTIDE_CHECKER_BUSINESS_PLAN.md` — full business plan with revenue projections
2. `COMPETITOR_DEEP_DIVE_2026.md` — 15+ competitors mapped and analyzed
3. `FIRST_100_CUSTOMERS_STRATEGY.md` — actionable acquisition playbook
4. `CROSS_REFERENCE_SYNTHESIS.md` — the synthesis report that proves coherence
5. `glp1_fda_enforcement_2026.md` — deep domain research with regulatory data
6. `EMAIL_NURTURE_SEQUENCES.md` — ready-to-deploy email campaigns

### Twitter/X Launch Thread

**Thread structure (10-12 tweets):**

1. "I built an entire business plan overnight. 50+ reports. 250K words. While I slept. Here is what I learned about AI-powered research at scale. (thread)"
2. Show the file listing — screenshot of 28 peptide reports
3. "Traditional strategy consulting charges $500K for this depth. Gartner charges $6K per report. We did it for the cost of a Claude subscription."
4. Explain the orchestrator pattern — how reports build on each other
5. Show the cross-reference synthesis — "this is the part AI research tools can not do"
6. Healthcare angle — "We have direct access to CMS, clinical trials, NPI databases"
7. Speed — "Client gives us the idea at 6 PM. By 8 AM, complete business plan."
8. Show actual report excerpts (redacted if needed)
9. Pricing reveal — "Starting at $497. Full overnight treatment: $9,997."
10. CTA — link to landing page

### Landing Page Design Concept

**Hero section:**
- Headline: "Wake Up to a Complete Business Plan"
- Subhead: "Overnight AI research sessions deliver McKinsey-depth analysis at indie founder prices"
- CTA: "See a Sample Corpus" / "Book Your Overnight Session"

**Social proof section:**
- "65+ reports generated" | "250,000+ words" | "Zero errors" | "One night"
- Scrolling list of actual report titles from peptide-checker

**How it works section:**
- 3-step visual: Submit your idea → We research overnight → Wake up to your business plan
- Clock animation showing the 8PM-8AM window

**Tier comparison section:**
- 4-column pricing table (Market Scan / Business Blueprint / Launch Ready / Full Overnight)
- "Most Popular" badge on Business Blueprint
- Each tier lists deliverable count and key reports

**FAQ section:**
- "How is this different from ChatGPT/Deep Research?" → synthesis explanation
- "Can I trust AI-generated research?" → quality control process, human review, cross-reference validation
- "What if I need revisions?" → 48-hour revision window included
- "What industries do you cover?" → any, with specialization in healthcare/biotech, SaaS, consumer products

**Footer CTA:**
- "Your competitors are sleeping. Your business plan does not have to." (or less aggressive variant)

### Pricing Page Structure

```
┌──────────────┬──────────────┬──────────────┬──────────────┐
│ MARKET SCAN  │  BUSINESS    │ LAUNCH READY │    FULL      │
│              │  BLUEPRINT   │              │  OVERNIGHT   │
│   $497       │   $1,997     │   $4,997     │   $9,997     │
│              │  ★ POPULAR   │              │              │
├──────────────┼──────────────┼──────────────┼──────────────┤
│ 5-8 reports  │ 15-20 reports│ 30-40 reports│ 50+ reports  │
│              │              │              │              │
│ ✓ Market     │ ✓ Everything │ ✓ Everything │ ✓ Everything │
│   analysis   │   in Scan    │   in Blueprint│  in Launch  │
│ ✓ Competitor │ ✓ Business   │ ✓ SEO        │ ✓ Deep domain│
│   landscape  │   plan       │   strategy   │   research   │
│ ✓ Regulatory │ ✓ Technical  │ ✓ Email      │ ✓ Cross-ref  │
│   overview   │   architecture│  sequences  │   synthesis  │
│ ✓ Customer   │ ✓ Revenue    │ ✓ Launch     │ ✓ Custom     │
│   personas   │   model      │   playbook   │   deliverables│
│ ✓ SWOT       │ ✓ Legal guide│ ✓ First 100  │ ✓ Investor   │
│              │ ✓ Go-to-mkt  │   customers  │   data room  │
│              │ ✓ Pitch      │ ✓ Community  │ ✓ Competitive│
│              │   narrative  │   playbook   │   dossiers   │
├──────────────┼──────────────┼──────────────┼──────────────┤
│  [Get Scan]  │ [Get Blueprint│[Get Launch] │[Go Full]     │
└──────────────┴──────────────┴──────────────┴──────────────┘
```

### Sales Channel Strategy

| Channel | Effort | Expected Conversion | Priority |
|---|---|---|---|
| Twitter/X organic (case study threads) | Low | High (proof is the product) | P0 — launch here |
| Indie Hackers / Hacker News posts | Low | Medium | P0 — launch simultaneously |
| LinkedIn outreach to innovation leads | Medium | High for T3-T4 | P1 — after initial traction |
| ProductHunt launch | Medium | High for T1-T2 | P1 — within 30 days |
| Referral program (20% commission) | Low | High (warm leads) | P1 — after first 10 clients |
| Podcast appearances (indie founder shows) | Medium | Medium | P2 — after 20+ clients |
| SEO content (blog posts on AI research) | High | Long-term compounding | P2 — ongoing |

---

## 7. Scalability

### Multi-Machine Deployment

| Machine | Specs | Role | Sessions/Night |
|---|---|---|---|
| Desktop (Windows) | RTX 3080 Ti, 64GB RAM | Primary operator station | 1-2 (Claude Code on Max) |
| Nodezero (Mac Mini M4 Pro) | 48GB unified memory | Secondary station | 1-2 (separate Claude account) |
| Cloud VPS | Any Linux instance | Tertiary station | 1-2 (API pay-as-you-go) |

**Total concurrent capacity:** 3-6 sessions/night across machines.

### API Cost Analysis

| Model | Input Cost | Output Cost | Est. Tokens/Session | Cost/Session |
|---|---|---|---|---|
| Claude Sonnet 4.6 | $3/MTok | $15/MTok | ~2M in, ~1M out | ~$21 |
| Claude Opus 4.6 | $5/MTok | $25/MTok | ~2M in, ~1M out | ~$35 |
| Blended (mostly Sonnet, Opus for synthesis) | — | — | ~3M total | ~$25-40 |

**On Max subscription ($100/mo):** Effectively unlimited for 1 session/night if within rolling usage windows. Marginal cost per session approaches $0 until hitting limits.

**On Max subscription ($200/mo):** 20x Pro limits. Comfortably 1-2 sessions/night. Marginal cost still approaches $0.

**On API pay-as-you-go:** ~$25-40 per session for a 50-report corpus. At scale, this is the model.

### Margin Analysis

| Tier | Revenue | API Cost | Operator Time (1hr) | Total COGS | Gross Margin | Margin % |
|---|---|---|---|---|---|---|
| T1 Market Scan | $497 | $15-25 | $50 | $65-75 | $422-432 | 85-87% |
| T2 Business Blueprint | $1,997 | $25-35 | $50 | $75-85 | $1,912-1,922 | 96% |
| T3 Launch Ready | $4,997 | $30-40 | $75 | $105-115 | $4,882-4,892 | 98% |
| T4 Full Overnight | $9,997 | $35-50 | $100 | $135-150 | $9,847-9,862 | 98-99% |

**These are software-like margins on a services business.** The operator time is the primary cost, not the AI. As templates mature and quality improves, operator review time decreases.

### Scaling Scenarios

**Phase 1: Solo Operator (Months 1-3)**
- Capacity: 1 client/night, 20 clients/month
- Revenue (blended avg $2K): $40K/month
- Costs: $200/mo (Max sub) + $100/mo (misc) = $300/mo
- Profit: ~$39,700/month
- Reuben's time: 1-2 hours/day (intake + review)

**Phase 2: Multi-Machine (Months 3-6)**
- Capacity: 3 clients/night, 60 clients/month
- Revenue (blended avg $2.5K): $150K/month
- Costs: $400/mo (subs) + $1,500/mo (API overflow) + $2K/mo (tools) = $3,900/mo
- Profit: ~$146K/month
- Reuben's time: 3-4 hours/day (intake + review + client mgmt)

**Phase 3: Hired Operators (Months 6-12)**
- Capacity: 5 clients/night, 100 clients/month
- Revenue (blended avg $3K): $300K/month
- Costs: $400/mo (subs) + $3K/mo (API) + $8K/mo (2 operators at $4K) + $2K (tools) = $13,400/mo
- Profit: ~$286K/month
- Reuben's role: Quality oversight, template development, sales

### Hiring Operators vs. Staying Solo

**Stay solo if:**
- Demand stays under 2 clients/night
- Reuben values time flexibility over revenue maximization
- Quality control requires deep domain knowledge per session

**Hire operators if:**
- Demand exceeds 2 clients/night consistently
- Templates are mature enough for a trained operator to configure sessions
- Reuben's time is better spent on sales, HUMMBL development, or high-value client relationships

**Operator profile:** Someone who understands prompt engineering, can customize templates per client domain, and can do quality review on generated reports. Not an AI researcher — a "research operations" role. Pay: $3,000-$5,000/month for US-based part-time, or $1,500-$2,500/month for international.

---

## 8. Integration with HUMMBL

### The Strategic Loop

```
ORaaS Client Sessions
        │
        ├──► Revenue funds HUMMBL development
        │
        ├──► Each session produces structured reasoning traces
        │    (hypothesis → research → analysis → synthesis)
        │
        ├──► Reasoning traces become training data for HUMMBL models
        │
        ├──► HUMMBL improvements make ORaaS sessions better
        │
        └──► ORaaS IS the live demo of HUMMBL GaaS
             (every client session proves the agent orchestration pattern works)
```

### ORaaS as HUMMBL Product Validation

1. **The orchestrator pattern IS HUMMBL** — Every overnight session runs the NemoClaw supervisor-worker pipeline. Each successful delivery validates the pattern.
2. **Client diversity = training data diversity** — SaaS founders, biotech companies, and hardware startups all generate different reasoning traces, making HUMMBL more general.
3. **Revenue before product** — ORaaS generates cash flow immediately while HUMMBL is being built. The service IS the product in its earliest form.
4. **Natural upgrade path** — ORaaS clients who love the research may want ongoing HUMMBL agent access. "You liked the overnight session? Here is the tool that runs it — HUMMBL GaaS."

### Data Flywheel

Every ORaaS session produces:
- **Structured research corpora** (training data for domain knowledge)
- **Orchestrator execution logs** (training data for planning/sequencing)
- **Cross-reference synthesis traces** (training data for reasoning quality)
- **Client feedback on report quality** (RLHF signal for HUMMBL models)

After 100 sessions across diverse domains, HUMMBL will have:
- Domain templates covering 20+ verticals
- Thousands of structured reasoning traces
- Real-world quality benchmarks from paying clients
- A defensible dataset no competitor can replicate (because they do not run the service)

### The Founder Mode Connection

ORaaS validates HUMMBL. HUMMBL powers Founder Mode. The pipeline:

```
ORaaS (service, immediate revenue)
  └──► HUMMBL (reasoning engine, trained on ORaaS data)
         └──► Founder Mode GaaS (product, Dan + Reuben)
                └──► Enterprise HUMMBL (future, agent orchestration platform)
```

Each layer funds and validates the next. No layer requires the subsequent one to succeed, but each makes the next one better.

---

## 9. Risk Analysis and Mitigations

| Risk | Severity | Mitigation |
|---|---|---|
| Anthropic rate limits reduce capacity | High | Multi-machine deployment, API fallback, consider OpenAI/Gemini as backup orchestrators |
| Client expects human-written quality | Medium | Clear positioning as "AI-generated, human-reviewed"; synthesis pass catches most issues; revision window |
| Competitor copies the approach | Medium | Moat is templates + MCP integrations + 65-report proof corpus. Speed to market matters — launch fast. |
| API pricing increases | Medium | Lock in annual subscriptions; shift to local models (Ollama) for non-synthesis phases; margins can absorb 2-3x cost increase |
| Quality failure damages reputation | High | Never skip synthesis pass; operator reviews every delivery; start with trusted early clients; iterate on templates |
| Demand exceeds capacity | Low-Medium | Good problem. Raise prices on T3-T4; hire operators; add machines; waitlist creates urgency |
| Legal liability for research accuracy | Medium | Clear TOS: "research starting point, not professional advice"; do not give legal/medical/financial advice; always include disclaimers |

---

## 10. 30-Day Launch Plan

**Week 1: Foundation**
- [ ] Build landing page (simple: Carrd or single-page Next.js)
- [ ] Set up Stripe for payment processing (4 products, 4 price points)
- [ ] Create intake form (Typeform or Tally)
- [ ] Write and publish Twitter/X launch thread
- [ ] Post on Indie Hackers with peptide-checker case study

**Week 2: First Clients**
- [ ] Offer 3 free/discounted Tier 2 sessions to trusted contacts (case study generation)
- [ ] Refine templates based on first sessions
- [ ] Collect testimonials from beta clients
- [ ] Post results thread on Twitter/X ("here is what we built for Client #1")

**Week 3: Scale Marketing**
- [ ] ProductHunt launch
- [ ] LinkedIn outreach campaign (innovation leads at mid-size companies)
- [ ] Publish blog post: "How We Built a Business Plan Overnight"
- [ ] Set up referral program

**Week 4: Optimize**
- [ ] Analyze conversion data (which tiers sell, where clients come from)
- [ ] Refine pricing if needed (may raise Tier 1 to $597 if conversion holds)
- [ ] Template v2 based on first 10 sessions
- [ ] Begin healthcare vertical specialization marketing

---

## 11. Key Metrics to Track

| Metric | Target (Month 1) | Target (Month 3) | Target (Month 6) |
|---|---|---|---|
| Clients/month | 5-10 | 20-30 | 50-60 |
| Revenue/month | $5K-$15K | $40K-$75K | $150K-$200K |
| Avg ticket size | $1,500 | $2,500 | $3,000 |
| Report quality score (client NPS) | 8+ | 9+ | 9+ |
| Repeat client rate | — | 20% | 30% |
| Referral rate | — | 15% | 25% |
| Operator time per session | 2 hours | 1.5 hours | 1 hour |
| API cost per session | $30 | $25 | $20 (template efficiency) |

---

## 12. The One-Liner

**For investors:** "We productized overnight AI research — McKinsey depth, indie founder prices, delivered while you sleep."

**For clients:** "Give us your idea at 6 PM. By 8 AM, you have a complete business plan, market research, technical architecture, and launch playbook. Starting at $497."

**For the market:** "The 50-report overnight research session is real. We built it. We proved it. Now we sell it."

---

## Sources

- [McKinsey/BCG/Bain Consulting Fees](https://www.rocketblocks.me/guide/business-model.php)
- [Management Consulting Fees: How McKinsey Prices Projects](https://slideworks.io/resources/management-consulting-fees-how-mc-kinsey-prices-projects)
- [Gartner Pricing and Alternatives](https://www.tsia.com/blog/alternatives-to-gartner)
- [Gartner/Forrester Subscription Costs](https://www.quora.com/What-does-it-cost-to-subscribe-to-services-from-analysts-like-Gartner-or-Forrester)
- [Claude API Pricing 2026](https://platform.claude.com/docs/en/about-claude/pricing)
- [Claude API Pricing Breakdown](https://www.metacto.com/blogs/anthropic-api-pricing-a-full-breakdown-of-costs-and-integration)
- [AI-Powered Market Research Companies 2026](https://touchstoneresearch.com/ai-powered-market-research-companies/)
- [AI Market Research — Andreessen Horowitz](https://a16z.com/ai-market-research/)
- [OpenAI Deep Research Comparison](https://www.helicone.ai/blog/openai-deep-research)
- [Google Deep Research vs Perplexity vs ChatGPT 2026](https://freeacademy.ai/blog/google-deep-research-vs-perplexity-vs-chatgpt-comparison-2026)
- [Claude Code Rate Limits Guide](https://www.truefoundry.com/blog/claude-code-limits-explained)
- [Claude Max Subscription Pricing](https://intuitionlabs.ai/articles/claude-pricing-plans-api-costs)
- [Fiverr vs Upwork 2026 Comparison](https://www.jobbers.io/fiverr-vs-upwork-vs-freelancer-vs-jobbers-complete-comparison-2026/)
- [AI Agent Predictions 2026 — CB Insights](https://www.cbinsights.com/research/ai-agent-predictions-2026/)
