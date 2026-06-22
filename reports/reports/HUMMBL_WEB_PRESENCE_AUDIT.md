# HUMMBL Web Presence Audit

**Date:** 2026-03-24
**Prepared for:** Reuben Bowlby, Chief Engineer, HUMMBL LLC

---

## Table of Contents

1. [hummbl.io Site Assessment](#1-hummbl-io-site-assessment)
2. [HUMMBL Brand Presence Across the Web](#2-hummbl-brand-presence-across-the-web)
3. [Reuben Bowlby Personal Brand](#3-reuben-bowlby-personal-brand)
4. [Related Brands & Projects](#4-related-brands--projects)
5. [Competitor Presence Comparison](#5-competitor-presence-comparison)
6. [Domain & Trademark Status](#6-domain--trademark-status)
7. [Overall Assessment & Recommendations](#7-overall-assessment--recommendations)

---

## 1. hummbl.io Site Assessment

### Current State: Professional Landing Page (Live Product)

The site at **hummbl.io** is a polished, cyberpunk-themed landing page for HUMMBL Base120 -- not parked, not under construction. It presents as an active SaaS product.

**What's on the page:**
- Hero section: "120 validated mental models your agents can call via API"
- Stats bar: 6 API endpoints, 5 vendor runtimes, 66 AI agents integrated
- Interactive "Try It Now" problem analyzer
- Claude Desktop MCP server integration instructions (npm install)
- Use case sections covering LangChain, CrewAI, prompt engineering, knowledge systems
- CTA buttons to discovery calls and model exploration

**Navigation links exist for:** Explorer, Playground, Docs, Pricing, Cases, Blog, Changelog, GitHub

**Footer:** "HUMMBL Base120 (c) 2026" with links to API docs, npm package, contact scheduling, Terms, Privacy, Status

### Sub-pages Audit

| Page | Status | Notes |
|------|--------|-------|
| `/docs` | Live | Moderately comprehensive. 3 sections (Getting Started, Endpoints, Reference). 6 endpoints documented with curl examples. Sparse on use cases and model selection guidance. |
| `/pricing` | Live | 3 tiers: Free ($0, 100 req/min, all models), Pro ($29/mo, coming soon), Enterprise (custom, coming soon). Generous free tier strategy. |
| `/blog` | Exists but empty | Framework is built with category filters (Announcement, Technical, AI, Security, API) but `posts.json` returns no content. Shows "Loading posts..." |
| `/changelog` | Unknown | Linked in nav but not independently verified. |
| `/playground` | Linked | Referenced on landing page. |
| `/explorer` | Linked | Referenced on landing page. |

### Subdomains

No evidence found of app.hummbl.io, docs.hummbl.io, or other subdomains. All content appears served from the root domain.

### Technical Notes
- HTTPS active
- Appears to be a static site with API backend
- No-signup API access (beta period, no auth required)
- Latency monitoring mentioned on landing page

---

## 2. HUMMBL Brand Presence Across the Web

### Search Results for "HUMMBL"

| Platform | Present? | Details |
|----------|----------|---------|
| Google Search | Yes | Appears for "HUMMBL AI", "HUMMBL reasoning", "HUMMBL MCP server" |
| GitHub (hummbl-dev) | Yes | **48 repositories**, Pro account. Key repos: base120 (Python), mcp-server (TypeScript, 3 stars), hummbl-agent (TypeScript, 2 stars), hummbl-governance (Python, 157 tests), HUMMBL-Unified-Tier-Framework |
| GitHub (hummbl) | Yes | Separate older account with a Jabber client (psi) -- likely unrelated or legacy |
| Glama.ai | Yes | MCP server listed with triple-A grades (security, license, quality). Listed as "confirmed to work" |
| LobeHub Marketplace | Yes | CO5 Emergence skill listed. 1 star on backing repo |
| Skillsmp / claude-plugins.dev | Yes | HUMMBL Claude skills listed (UI/UX designer skill, others) |
| npm | Partially | @hummbl-dev/mcp-server package exists (403 on direct page -- may be scoped/private or low traffic) |
| Reddit | **No** | Zero results |
| Hacker News | **No** | Zero results |
| Product Hunt | **No** | Zero results |
| Indie Hackers | **No** | Zero results |
| Twitter/X | **No** | No HUMMBL brand account found |
| LinkedIn | **No** | No HUMMBL company page found (search returns HUMBL LLC, the fintech company) |
| Blog posts / articles | **No** | No third-party coverage, no guest posts, no press mentions |
| Podcasts / conferences | **No** | No evidence of talks or appearances |

### Key Listing Details

**Glama.ai listing** (https://glama.ai/mcp/servers/@hummbl-dev/mcp-server):
- Version: 1.0.0-beta.2
- Language: TypeScript
- License: MIT
- 8 tools listed (get_model, list_all_models, search_models, recommend_models, workflow tools)
- Triple-A quality rating

**LobeHub listing** (https://lobehub.com/skills/hummbl-dev-hummbl-agent-co5-emergence):
- CO5 Emergence skill for detecting emergent phenomena in multi-agent systems
- Category: coding-agents-ides
- Minimal adoption (1 star)

---

## 3. Reuben Bowlby Personal Brand

### Online Profiles Found

| Platform | URL | Status |
|----------|-----|--------|
| GitHub | https://github.com/hummbl-dev | Active. 48 repos, Pro account. Bio: "building HUMMBL, AI Agent Builder - Systems Architect" |
| LinkedIn | https://www.linkedin.com/in/reuben-bowlby-395a11307 | Exists. Listed as "Self-employed" |
| LinkedIn (2nd) | https://www.linkedin.com/in/reuben-bowlby-a31b2236b | Exists. Listed as "working" |
| Instagram | https://www.instagram.com/reubenbowlby/ | Active. Bio: "Context Engineer & AI Educator" / "HUMMBL Human-Centered AI" |
| Twitter/X | https://twitter.com/reub42 | Legacy account. Last visible activity from 2014 (McKendree University era). Not used for HUMMBL |
| Gravatar | https://reubenbowlby.live/ | Minimal profile. Lists "Certified Strength and Conditioning Specialist". No AI/HUMMBL content |

### Key Observations

- **Two LinkedIn profiles** -- fragmented presence. Neither appears to be fully built out with HUMMBL details visible in search snippets
- **Instagram** is the only platform where "HUMMBL Human-Centered AI" branding is present in the bio
- **Twitter/X** (@reub42) is dormant and carries old personal content, not HUMMBL branding
- **Gravatar** profile still shows fitness credentials, not updated for AI/HUMMBL identity
- **No personal blog, Medium, Substack, or Dev.to** presence found
- **No conference talks, podcast appearances, or press interviews** found

### Historical Background (from search)
- Former student-athlete at McKendree University
- Previously a Certified Strength and Conditioning Specialist
- Career pivot to AI/tech appears relatively recent

---

## 4. Related Brands & Projects

### Founder Mode
- **Search results:** No public GitHub repository named "founder-mode" found under hummbl-dev
- The concept appears in HUMMBL's internal documentation (scope expansion modes: SCOPE EXPANSION, SELECTIVE EXPANSION, HOLD SCOPE, SCOPE REDUCTION)
- **foundermode.ai** is a separate, unrelated SaaS product for founder leadership coaching
- **Dan Matha** appears online as a fitness/performance coach and former WWE executive -- no public AI/startup connection found in search results
- **Assessment:** The "Founder Mode" project has zero public web presence currently

### Peptide Checker
- **Search results:** The top GitHub result for "peptide-checker" is https://github.com/evanmunro/peptide-checker -- a C++ utility for solid-phase peptide synthesis side products. This is **unrelated** to HUMMBL
- No HUMMBL-associated peptide checker project found in public search results
- The `peptides/` directory exists in the autoresearch-reports folder locally but has no public web presence

### HUMMBL LLC
- Referenced as the company entity on GitHub profile
- No state business registration records surfaced in web search
- No Crunchbase, AngelList, or startup directory listings found

---

## 5. Competitor Presence Comparison

### LangChain (langchain.com)

| Dimension | LangChain | HUMMBL |
|-----------|-----------|--------|
| Landing page | Enterprise-grade, animated, GSAP-powered | Professional, cyberpunk-themed |
| Social proof | Klarna, LinkedIn, Cloudflare, Lyft + 20 logos | None listed |
| Metrics on page | "100M+ monthly downloads", "6K+ customers", "5 of Fortune 10" | "6 endpoints, 5 runtimes, 66 agents" |
| Blog | Active, regular content | Empty (framework exists, no posts) |
| GitHub stars | 100K+ (langchain repo) | 3 (mcp-server) |
| Community | Massive Discord, active Reddit, YouTube | None |
| Funding | $25M+ raised | Bootstrapped solo founder |

### CrewAI (crewai.com)

| Dimension | CrewAI | HUMMBL |
|-----------|--------|--------|
| Landing page | Enterprise-grade, video backgrounds, animations | Professional, cyberpunk-themed |
| Social proof | DocuSign, IBM, PwC + 16 logos | None listed |
| Metrics on page | "450M+ workflows/month", "60% of Fortune 500", "4K+ signups/week" | Internal metrics only |
| Blog | Active | Empty |
| GitHub stars | 25K+ | 3 |
| Community | Active Discord, growing community | None |

### What HUMMBL Can Learn

1. **Social proof is table stakes.** Even early-stage competitors list user counts, company logos, and testimonials prominently
2. **Content marketing drives discovery.** Both competitors maintain active blogs, YouTube channels, and documentation-as-marketing strategies
3. **Community platforms matter.** Discord servers and Reddit presence create organic word-of-mouth
4. **Case studies with measurable outcomes** ("80% reduction in resolution time") are more compelling than feature lists
5. **HUMMBL occupies a unique niche** -- mental models as an API is genuinely differentiated. The competitors do agent orchestration; HUMMBL does cognitive frameworks. This positioning advantage is currently invisible because nobody knows about it

---

## 6. Domain & Trademark Status

### Domain Inventory

| Domain | Status | Notes |
|--------|--------|-------|
| **hummbl.io** | **Active, owned** | Primary domain. Live site. |
| hummbl.com | Expired/Available | Was registered with GoDaddy Jan 2020, expired Jan 2021. Currently appears to be available or held by a third party. "Coming soon" placeholder last seen. |
| hummbl.ai | Unknown | No evidence of ownership. Likely available for registration. High strategic value for an AI company. |
| humbl.com | Owned by HUMBL Inc. (now TAP Real Estate Technologies) | The fintech company acquired this in 2022. Different entity entirely. |

### Trademark Status

| Mark | Filing Status |
|------|--------------|
| **HUMMBL** (with double-M) | **No USPTO filing found.** No evidence of trademark registration or pending application. |
| HUMBL (single-M) | Registered by HUMBL, LLC (fintech). Covers electronic payments software. First use: April 2018. Serial: 88240846. |

### Brand Confusion Risk

**MODERATE RISK.** HUMBL, Inc. (ticker: HMBL) was a publicly traded fintech company that:
- Was the subject of a Hindenburg Research short report alleging it was "propped up by techno-babble"
- Is under investigation by Robbins LLP
- Has rebranded to TAP Real Estate Technologies as of March 2026
- Previously owned HUMBL trademark for payments software

While the fintech HUMBL is fading (rebranding away), the brand confusion potential persists in search results. LinkedIn searches for "HUMMBL" return the fintech "HUMBL LLC" prominently. The Hindenburg association could create negative brand confusion for anyone who conflates the two.

**The double-M in HUMMBL provides some differentiation**, but without a trademark filing, there is no legal protection.

### Recommendations
1. **Register hummbl.ai immediately** -- this is the most strategically valuable domain for an AI company and likely still available
2. **Consider acquiring hummbl.com** if affordable
3. **File a USPTO trademark application for HUMMBL** in relevant classes (SaaS, AI tools, developer tools)

---

## 7. Overall Assessment & Recommendations

### Online Visibility Score: 3/10

**Breakdown:**
- Website quality: 7/10 (polished, functional, professional)
- Search discoverability: 3/10 (appears for branded searches only, zero organic/non-branded traffic signals)
- Social proof: 1/10 (no testimonials, no user counts, no company logos)
- Community presence: 1/10 (zero Reddit, HN, Product Hunt, Twitter/X, LinkedIn company page)
- Content marketing: 1/10 (blog framework exists but is empty)
- Developer ecosystem: 4/10 (GitHub repos exist, MCP server listed on directories, but minimal stars/adoption)
- Personal brand (founder): 3/10 (GitHub is solid, everything else is fragmented or dormant)
- Press/media: 0/10 (no coverage found anywhere)

### What's Working

1. **The product website is genuinely good.** Professional design, clear value proposition, interactive demo, working API, documentation, pricing page. This is above average for a solo founder project.
2. **GitHub presence is solid.** 48 repos, Pro account, clear bio, active development. The case study document on the mcp-server repo is well-written.
3. **MCP ecosystem listings** on Glama.ai and LobeHub provide legitimate third-party discoverability.
4. **Unique positioning.** "120 mental models as an API" is genuinely differentiated from LangChain/CrewAI/AutoGen. Nobody else is doing this.
5. **Free tier with no auth** is a smart developer acquisition strategy for beta.

### What's Missing (Critical Gaps)

1. **No social media presence for the brand.** No Twitter/X, no LinkedIn company page, no Bluesky. In AI/dev tools, Twitter/X is where deals start.
2. **Empty blog.** The framework is built but zero posts published. This is the single highest-leverage gap.
3. **No community platforms.** No Discord, no Reddit engagement, no HN submissions.
4. **No social proof on the website.** Zero testimonials, user counts, or company logos.
5. **Fragmented personal brand.** Two LinkedIn profiles, dormant Twitter, outdated Gravatar. The Instagram bio is the only place "HUMMBL Human-Centered AI" appears.
6. **No trademark protection.** The HUMBL fintech association is a ticking time bomb for brand confusion.
7. **No press or content distribution.** The case study buried in GitHub docs could be a standalone blog post or Dev.to article.
8. **hummbl.ai domain not secured.** For an AI company, this is a significant miss.

### Biggest Opportunities for Immediate Improvement

**Tier 1 -- This Week (high impact, low effort):**
1. Create a Twitter/X account for @hummbl or @hummbl_io and post the first thread explaining what Base120 is
2. Create a LinkedIn company page for HUMMBL LLC
3. Publish the first blog post (repurpose the GitHub case study)
4. Register hummbl.ai domain
5. Update the Gravatar profile and consolidate LinkedIn to one profile

**Tier 2 -- This Month (high impact, moderate effort):**
6. Submit to Product Hunt (mental models API is a compelling PH launch)
7. Post on Hacker News (Show HN: 120 mental models as an API for AI agents)
8. Write 3-5 blog posts (how Base120 improves agent reasoning, comparison with raw prompting, integration guides)
9. Add social proof to website (even beta user quotes, GitHub stars count, API call volume)
10. File USPTO trademark application for HUMMBL

**Tier 3 -- Next 90 Days (compound growth):**
11. Create a Discord community
12. Start a Dev.to or Hashnode blog for cross-posting
13. Record a demo video for YouTube
14. Pitch to AI newsletters (Ben's Bites, The Rundown, TLDR AI)
15. Engage in Reddit communities (r/LocalLLaMA, r/MachineLearning, r/ChatGPT) where mental models discussions happen

### The Core Problem

HUMMBL has a **product-market readiness gap**, not a product quality gap. The product is genuinely good and differentiated. The website is professional. The API works. But outside of direct branded searches and a couple of MCP directories, HUMMBL is invisible to the broader AI/developer community.

The irony: the case study on GitHub demonstrates that Base120 was built by a solo founder in 18 months with 9.2/10 validation quality using multi-agent coordination -- and almost nobody has seen it. That story itself is the marketing.

---

*Audit conducted 2026-03-24 using web search, site fetching, and public data analysis.*
