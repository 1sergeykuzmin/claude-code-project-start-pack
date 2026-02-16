---
name: prd
description: Generate a Product Requirements Document (PRD) from a product idea. Use when asked to create a PRD, document product requirements, or start a new product. Invoked as "/prd <product description>". Supports --team flag for multi-perspective generation using agent teams with optional domain specialists.
metadata:
  author: custom
  version: "2.3.0"
  argument-hint: [--team] <product-description>
---

# Product Requirements Document Generator

Generate comprehensive Product Requirements Documents following industry best practices. This skill gathers information about a product idea through structured questions and produces a well-organized PRD.

Supports two modes:
- **Solo mode** (default): Single-agent PRD generation with adaptive questioning
- **Team mode** (`--team`): Multi-perspective PRD using agent teams with Product, UX, and Tech analysts, plus optional domain specialists (Business, Design, SEO, Mobile, Enterprise, Growth, AI)

## Input Format

```
/prd <product description>              # Solo mode (default)
/prd --team <product description>       # Team mode (multi-perspective)
```

The product description can be a brief idea, a detailed concept, or anything in between. The skill will adapt its approach based on what information is provided.

## Mode Selection

### Detecting Mode

1. If the input contains `--team`, use **Team Mode**
2. Otherwise, use **Solo Mode**

### When to Suggest Team Mode

If solo mode is invoked but the idea meets ANY of these criteria, **suggest** (don't force) team mode:
- Consumer product with likely competitors
- Multi-stakeholder product (B2B2C, marketplace, platform)
- Complex product spanning multiple domains
- User explicitly says "comprehensive" or "thorough"

Suggestion format:
```
This product could benefit from multi-perspective analysis.
Would you like to use team mode (/prd --team) for a more
comprehensive PRD with Product, UX, and Technical research?
```

If the user declines, proceed with solo mode normally.

### Team Mode Prerequisites

Team mode requires `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` to be enabled. If not enabled and `--team` is used:
```
Team mode requires agent teams to be enabled.
Add to your settings.json:
  "env": { "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1" }

Proceeding with solo mode instead.
```

---

# SOLO MODE

The default PRD generation process using a single agent.

## Solo Process

### Step 1: Analyze Initial Input

Parse the product description to identify:
- **Provided information**: What details are already clear
- **Missing information**: What gaps need to be filled
- **Ambiguities**: What needs clarification

Map the input against the PRD framework sections to determine what questions to ask.

### Step 2: Ask Follow-up Questions

Use the AskUserQuestion tool to gather missing information. Ask **up to 10 questions** to complete the picture. Questions should be:

- **Targeted**: Address specific gaps in the PRD
- **Prioritized**: Most critical information first
- **Clear**: Easy to understand and answer
- **Actionable**: Answers directly inform the PRD

**Question Categories (prioritized):**

| Priority | Category | Purpose |
|----------|----------|---------|
| 1 | Problem & Users | Who has this problem? How painful is it? |
| 2 | Goals & Success | What does success look like? How to measure? |
| 3 | Core Features | What are the must-have capabilities? |
| 4 | User Experience | How will users interact with the product? |
| 5 | Scope & Constraints | What's in/out? What limitations exist? |
| 6 | Resources & Constraints | Team size, budget range, hard deadlines? |
| 7 | Technical Context | Platform, integrations, technical requirements? |
| 8 | Business Context | Monetization, competition (direct & indirect), go-to-market? |
| 9 | Ethics & Content Safety | Content boundaries, sensitive topics, moderation needs? (conditional — see below) |
| 10 | Risks & Dependencies | What could go wrong? What do we depend on? |

**Ethics & Content Safety Detection:**
Ask Priority 9 questions ONLY if the product involves ANY of:
- AI-generated or AI-curated content
- Health, wellness, or medical adjacent topics
- Financial advice or predictions
- Content targeting vulnerable populations (minors, elderly, those in crisis)
- User-generated content at scale
- Personal data with sensitive implications

**Question Selection Logic:**

```
1. Review initial input for each PRD section
2. Identify sections with insufficient information
3. Prioritize questions by impact on PRD quality
4. Group related questions when possible (max 4 options per question)
5. Skip questions where reasonable defaults exist
6. Stop when you have enough for a solid PRD (don't force 10 questions)
```

**Example Question Patterns:**

```
Problem & Users:
- "Who is the primary target user for this product?"
- "What problem does this solve and how do users currently handle it?"

Goals & Success:
- "What would make this product successful? Any specific metrics?"
- "What is the primary goal users should accomplish?"

Core Features:
- "What are the 3-5 must-have features for the initial version?"
- "Are there features explicitly NOT needed for v1?"

User Experience:
- "What platforms should this support (web, mobile, desktop)?"
- "Should this integrate with any existing tools or services?"

Scope & Constraints:
- "What's the expected scale (users, data volume)?"
- "Any hard constraints (budget, timeline, tech stack)?"

Technical Context:
- "Are there preferred technologies or existing systems to integrate with?"
- "Any performance requirements (load times, response times)?"

Resources & Constraints:
- "What's the expected team size (solo dev, small team, large org)?"
- "Is there a budget range for development and infrastructure?"
- "Are there hard deadlines or launch windows?"

Business Context:
- "Is this B2B, B2C, or internal tooling?"
- "How will this be monetized (if applicable)?"
- "Who are the indirect competitors or alternative approaches users might use?"

Ethics & Content Safety (conditional):
- "What content should the product never generate or recommend?"
- "Are there sensitive topics that need special handling or disclaimers?"
- "What happens when a user receives potentially harmful advice?"
```

### Step 3: Generate the PRD

After gathering information, create a comprehensive PRD at `dev-docs/prd.md` using the **Solo PRD Template** (see below).

### Step 3.5: Quality Gate Validation

Before presenting the PRD, run all quality gates and fix any ERROR-level issues. WARNING-level issues should be noted but do not block generation.

| Gate ID | Name | Severity | Detection Logic |
|---------|------|----------|-----------------|
| QG-001 | Revenue Math Consistency | ERROR | **Conditional**: If Business Analyst specialist was NOT activated, mark N/A. Otherwise, if monetization section exists: verify all arithmetic (price × users × conversion = revenue). **Show your work**: write out the calculation step-by-step inline (e.g., "500 users × 10% conversion × $25/mo = $1,250/mo"). Require tier mix table if multiple pricing tiers. Flag mismatches between revenue projections and user forecasts. Every row in the Financial Scenarios table must pass: users × conversion × ARPU = revenue. |
| QG-002 | Phase Dependency Validation | ERROR | For each phased feature: verify no Phase N feature depends on a feature scheduled for Phase N+1 or later. Build a dependency DAG across all FRs — check that all edges point forward (Phase 1→2→3, never backward). Flag circular dependencies (FR-X depends on FR-Y which depends on FR-X). If any FR has dependencies, list them explicitly in the Dependencies field. |
| QG-003 | KPI Benchmark Requirement | WARNING | Every KPI target must either cite an industry benchmark source or be explicitly labeled `[Hypothesis]`. No unsourced absolute targets. |
| QG-004 | Acceptance Criteria Testability | ERROR | Every acceptance criterion must be objectively verifiable. Reject and rewrite: (a) process-oriented criteria → measurable outcomes ("team reviews regularly" → "review log shows ≥1 entry per sprint"), (b) subjective criteria → quantifiable thresholds ("interface feels intuitive" → "80% of test users complete onboarding in <3 min without help"), (c) vague criteria → specific pass/fail ("works well" → "response time <200ms at P95 under 100 concurrent users"). |
| QG-005 | Claim Attribution | WARNING | Market size claims, user behavior assertions, and growth projections must cite a source or be labeled `[Estimated]`. Flag unsourced statistical claims. |
| QG-006 | Scope-Timeline Feasibility | WARNING | Calculate complexity budget per phase: S=1, M=2, L=4, XL=8 points. **Show your work**: list each FR with its point value and sum per phase (e.g., "Phase 1: FR-001(M=2) + FR-002(L=4) + FR-003(S=1) = 7 points"). Flag phases exceeding 16 points. Add risk note for any XL feature in Phase 1. The claimed total in the PRD must match the actual sum. |
| QG-007 | Complexity Discreteness | ERROR | Each FR complexity must be a single value (S, M, L, or XL). No ranges ("M-L"), no compound values ("M/L"). If uncertain, choose the higher value. |
| QG-008 | Specialist Integration | WARNING | If a specialist was activated: verify that (a) specialist's standalone section (§12A/B/C) exists (except Business Analyst whose standalone is §2 Market Context), (b) at least 2 existing sections were enhanced with specialist subsections labeled `[Added by {Name}]`, (c) specialist-specific quality gates were evaluated. If no specialist was activated, mark N/A. |

### Specialist Quality Gates

Applied ONLY when the corresponding specialist is activated. Each specialist has 1 ERROR gate (must pass) + WARNING gates (noted but non-blocking).

| Gate | Specialist | Severity | Detection Logic |
|------|-----------|----------|-----------------|
| QG-SEO-1 | SEO Strategist | ERROR | Content architecture must include: topic clusters, internal linking strategy, and at least 3 primary keyword clusters with search volume estimates. |
| QG-SEO-2 | SEO Strategist | WARNING | Core Web Vitals targets should include specific LCP/FID/CLS thresholds. |
| QG-MOB-1 | Mobile Platform Strategist | ERROR | Platform strategy must specify: native vs cross-platform decision with rationale, minimum OS versions, and offline behavior. |
| QG-MOB-2 | Mobile Platform Strategist | WARNING | App size budget should be specified with market-appropriate rationale. |
| QG-ENT-1 | Enterprise & Compliance | ERROR | Every applicable regulation must be named with specific compliance requirements (not just "GDPR compliant"). |
| QG-ENT-2 | Enterprise & Compliance | WARNING | Compliance roadmap should include timeline and cost estimates. |
| QG-GRO-1 | Growth Strategist | ERROR | Growth model must identify primary loop with acquisition cost estimates (cite benchmarks or label [Hypothesis]). |
| QG-GRO-2 | Growth Strategist | WARNING | Retention cohort targets (D1/D7/D30) should cite industry benchmarks. |
| QG-AI-1 | AI Prompt Engineer | ERROR | Every AI-facing feature MUST have: a named system prompt with version, at least 1 evaluation metric, defined fallback behavior, and a token cost estimate. |
| QG-AI-2 | AI Prompt Engineer | WARNING | Prompt architecture should include a versioning strategy and regression testing approach. |
| QG-AI-3 | AI Prompt Engineer | WARNING | Safety section should enumerate specific guardrails (not generic "content filtering"), including prompt injection prevention and confidence thresholds. |
| QG-BIZ-1 | Business Analyst | ERROR | Market Context must include: at least 5 direct competitors with feature comparison, market size estimate (TAM/SAM/SOM or equivalent), and monetization model with pricing tiers. |
| QG-BIZ-2 | Business Analyst | WARNING | Financial projections should include sensitivity analysis or multiple scenarios. |
| QG-DES-1 | Designer | ERROR | Design system must include: color palette, typography scale, spacing system, and at least 3 key screen layout descriptions. |
| QG-DES-2 | Designer | WARNING | Component library recommendation should be specific to the tech stack (not generic). |

**Gate enforcement procedure:**
1. After generating the PRD, scan for each universal gate (QG-001 through QG-008)
2. If specialist was activated, also scan specialist-specific gates
3. For ERROR gates: fix the issue inline before presenting
4. For WARNING gates: add a note in the Quality Gate Results section
5. Append a Quality Gate Results table before the Appendix:

```markdown
## Quality Gate Results

| Gate | Status | Notes |
|------|--------|-------|
| QG-001 Revenue Math | PASS / FAIL / N/A | [details if FAIL] |
| QG-002 Phase Dependencies | PASS / FAIL / N/A | [details if FAIL] |
| QG-003 KPI Benchmarks | PASS / WARN | [which KPIs are hypothetical] |
| QG-004 Acceptance Testability | PASS / FAIL | [details if FAIL] |
| QG-005 Claim Attribution | PASS / WARN | [which claims lack sources] |
| QG-006 Scope Feasibility | PASS / WARN | [phase point totals] |
| QG-007 Complexity Discreteness | PASS / FAIL | [details if FAIL] |
| QG-008 Specialist Integration | PASS / WARN / N/A | [specialist name or N/A] |
| [QG-XXX-N Specialist Gates] | PASS / FAIL / WARN | [if specialist activated] |
```

### Step 4: Review and Refine

After quality gate validation:

1. **Completeness Check**: Ensure all sections have meaningful content
2. **Consistency Check**: Verify terminology and priorities are consistent
3. **Clarity Check**: Ensure requirements are specific and testable
4. **Gap Identification**: Note any remaining open questions

---

# TEAM MODE

Multi-perspective PRD generation using agent teams. Spawns 3 core teammates (Product Strategist, UX Researcher, Tech Analyst) plus optional domain specialists who research in parallel, debate findings, and produce a more comprehensive PRD.

## Team Process Overview

```
Lead: Ask 3-4 scoping questions
  ↓
Lead: Detect specialist need (keyword scan → LLM judgment → user confirmation)
  ↓
Lead: Spawn 3 core teammates + 0-3 specialists
  ↓
Teammates: Research in parallel (each produces findings)
  ↓
Lead: Wait for ALL teammates to complete, then broadcast findings
  ↓
Teammates: Debate — challenge assumptions, flag conflicts, propose resolutions
  ↓
Lead: Synthesize into enhanced PRD
  ↓
Lead: Run Quality Gate Validation (8+ gates)
  ↓
Lead: Shut down teammates, clean up team
```

## Team Step 1: Lead Intake

The lead asks **3-4 high-level scoping questions only**. Keep it brief because teammates will research deeply.

Focus on:
- Target market / audience
- Scale of ambition (MVP vs full product)
- Resources & constraints (team size, budget range, timeline)
- Ethics & content safety (conditional — only if the product triggers the Ethics detection criteria above)

Use AskUserQuestion tool. Batch into 1 tool call (3-4 questions max).

**Do NOT ask detailed questions about features, technology, or business model** — those are for the teammates to research.

## Team Step 1.5: Specialist Detection

After scoping questions are answered, run the **Detection Logic** from the Conditional Specialists section:

1. Scan product description + user answers for trigger keywords
2. Apply contextual inference if signal is weak
3. If a specialist is recommended, ask the user via AskUserQuestion
4. If user declines or no match found, proceed with core team only

Record the result: `specialist = {name}` or `specialist = none`

## Team Step 1.9: Create Workspace

Create a temporary workspace directory for intermediate research artifacts:

```bash
mkdir -p .prd-workspace
```

This directory stores research findings and debate responses as persistent files, ensuring they survive context compaction and message delivery issues. The workspace is cleaned up in Team Step 6.

**File naming convention:**
- Research findings: `.prd-workspace/{role}-findings.md` (e.g., `product-findings.md`, `ux-findings.md`, `tech-findings.md`)
- Debate responses: `.prd-workspace/{role}-debate.md` (e.g., `product-debate.md`, `ux-debate.md`, `tech-debate.md`)
- Specialist files use the specialist slug: `business-findings.md`, `designer-findings.md`, `seo-findings.md`, `mobile-findings.md`, `enterprise-findings.md`, `growth-findings.md`, `ai-prompt-findings.md`

Also add `.prd-workspace/` to `.gitignore` if not already present.

**Why files instead of messages:** SendMessage content is ephemeral — if the lead's context compacts or messages are consumed before rendering, the data is lost. Files persist on disk and can be re-read at any time.

## Team Step 2: Spawn Research Team

Create an agent team with 3 core teammates, plus specialists (if activated). Use the spawn prompts below for core teammates and the specialist spawn prompts from the Conditional Specialists section.

| Teammate | Name | Role | Always? |
|----------|------|------|---------|
| 1 | Product Strategist | Product perspective: features, scope, prioritization, requirements, phasing | Yes |
| 2 | UX Researcher | User perspective: personas, journeys, pain points, interactions | Yes |
| 3 | Tech Analyst | Technical perspective: feasibility, architecture, complexity, risks | Yes |
| 4-6 | [Specialists] | Domain-specific analysis (Business / Design / SEO / Mobile / Enterprise / Growth / AI) | If activated (max 3) |

**Spawn configuration:**
- Require plan approval: NO (teammates should research freely)
- Use delegate mode: YES (lead should not implement, only coordinate)
- Model for teammates: Use the same model as the lead session
- Specialist gets the same configuration as core teammates

### Product Strategist Spawn Prompt

```
You are the Product Strategist for a PRD research team. Your job is to deeply
investigate what this product should do, how features should be scoped and
prioritized, and what the functional requirements should be.

RESEARCH STANDARDS (apply to all sections):
- Cite sources when making claims about user behavior or market data
- Distinguish between FACTS (sourced), ESTIMATES (reasonable inference),
  and ASSUMPTIONS (educated guess) using inline labels
- When providing numbers, include ranges rather than single-point estimates
- Ground all recommendations in specific evidence, not generic best practices

PRODUCT IDEA: [insert product description]
USER CONTEXT: [insert lead Q&A answers]

Research and produce a structured findings document covering:

1. PROBLEM-SOLUTION FIT ANALYSIS
   - Does the proposed product actually solve the stated problem?
   - Gap between current solutions and proposed approach
   - Assumptions that must hold for the solution to work
   - What evidence supports or contradicts these assumptions?

2. FEATURE DEFINITION & PRIORITIZATION
   - Core feature set for MVP (P0 features) — minimum set that delivers value
   - Secondary features for v1.1 (P1) — important but not launch-blocking
   - Future considerations (P2) — nice to have, defer to later
   - MoSCoW classification with rationale for each feature
   - What is explicitly OUT of scope and why

3. FUNCTIONAL REQUIREMENTS
   For each P0 and P1 feature, define:
   - Detailed requirement description
   - Acceptance criteria (objectively verifiable, measurable outcomes —
     NOT process-oriented like "team reviews regularly",
     NOT subjective like "interface feels intuitive")
   - Feature dependencies (what must exist before this can work)
   - Success criteria: how to measure if this feature is working

4. PHASING & ROADMAP
   - MVP definition — minimum feature set that delivers core value
   - Phase boundaries with rationale (why this grouping?)
   - Feature dependency DAG (what must come before what)
   - Decision gates between phases (what must be true to proceed)
   - Risk: flag any XL-complexity feature in Phase 1

5. COMPETITIVE FEATURE GAP ANALYSIS
   - Feature-level comparison with 3-5 existing solutions
   - Table stakes features (must match competitors)
   - Differentiating features (what sets this product apart)
   - Features competitors have that we deliberately exclude (and why)

6. SUCCESS METRICS (Product-level)
   - How to measure if each major feature is working
   - Activation metric: what indicates a user "got it"
   - Feature adoption targets (cite benchmarks or label [Hypothesis])
   - North star metric recommendation with rationale

FORMAT: Use structured markdown with clear headers.
Be DECISIVE about scope — clearly state what's in and what's out.
Acceptance criteria must be objectively testable, not vague.
Every feature must have a priority (P0/P1/P2) with justification.

OUTPUT INSTRUCTIONS:
1. Write your complete findings to: .prd-workspace/product-findings.md
2. After writing the file, send a SHORT notification to the team lead
   via SendMessage confirming your findings are ready.
   Do NOT include the full findings in the message — just confirm
   the file is written and give a 2-3 sentence summary.
```

### UX Researcher Spawn Prompt

```
You are the UX Researcher for a PRD research team. Your job is to deeply
investigate the user perspective for this product idea.

RESEARCH STANDARDS (apply to all sections):
- Cite sources when making claims about user behavior or market data
- Distinguish between FACTS (sourced), ESTIMATES (reasonable inference),
  and ASSUMPTIONS (educated guess) using inline labels
- When providing numbers, include ranges rather than single-point estimates
- Ground all recommendations in specific evidence, not generic best practices

PRODUCT IDEA: [insert product description]
USER CONTEXT: [insert lead Q&A answers]

Research and produce a structured findings document covering:

1. USER PERSONAS (2-3 personas)
   For each persona provide:
   - Name and role
   - Demographics and context (MUST reflect the target market demographics
     provided by the user — age range, gender, location, etc.)
   - Goals (what they want to achieve)
   - Pain points (current frustrations — cite source or label [Estimated])
   - Tech savviness (Low/Medium/High)
   - A realistic usage scenario

2. USER JOURNEYS
   Map the key flows:
   - Discovery: How do they find the product?
   - Onboarding: First-time experience
   - Core loop: Daily/regular usage pattern
   - Edge cases: What happens when things go wrong?

3. PAIN POINTS WITH CURRENT SOLUTIONS
   - What do users do today to solve this problem?
   - What frustrates them about existing solutions? (cite sources where possible)
   - What would make them switch?

4. KEY INTERACTIONS
   - Critical UI moments that make or break the experience
   - Features that drive engagement vs features that are expected
   - Interaction patterns that feel natural for this domain

5. ACCESSIBILITY CONSIDERATIONS
   - Inclusive design needs
   - Device/context considerations (when/where do users use this?)

6. CONTENT SAFETY & ETHICAL UX (conditional — include ONLY if the product
   involves AI content, health/wellness, financial advice, vulnerable users,
   or user-generated content at scale)
   - Content boundaries: what the product should NEVER show or recommend
   - Sensitive topic handling: disclaimers, warnings, gating
   - User safety: crisis resources, human escalation paths
   - Dark pattern avoidance: specific UX anti-patterns to avoid

FORMAT: Use structured markdown with clear headers.
Be SPECIFIC — ground everything in realistic user behavior, not generic statements.
Avoid vague personas like "busy professional who wants convenience."

OUTPUT INSTRUCTIONS:
1. Write your complete findings to: .prd-workspace/ux-findings.md
2. After writing the file, send a SHORT notification to the team lead
   via SendMessage confirming your findings are ready.
   Do NOT include the full findings in the message — just confirm
   the file is written and give a 2-3 sentence summary.
```

### Tech Analyst Spawn Prompt

```
You are the Tech Analyst for a PRD research team. Your job is to deeply
investigate the technical feasibility and implications of this product idea.

RESEARCH STANDARDS (apply to all sections):
- Cite sources when making claims about user behavior or market data
- Distinguish between FACTS (sourced), ESTIMATES (reasonable inference),
  and ASSUMPTIONS (educated guess) using inline labels
- When providing numbers, include ranges rather than single-point estimates
- Ground all recommendations in specific evidence, not generic best practices

PRODUCT IDEA: [insert product description]
USER CONTEXT: [insert lead Q&A answers]

Research and produce a structured findings document covering:

1. ARCHITECTURE OPTIONS
   Propose 2-3 viable technical approaches with tradeoffs:
   - Option A: [approach] — Pros / Cons / Best when...
   - Option B: [approach] — Pros / Cons / Best when...
   - Recommended: [which and why]

2. FEATURE FEASIBILITY ASSESSMENT
   For each likely feature, rate complexity as a SINGLE value (S, M, L, or XL).
   No ranges. No compound values. If uncertain, choose the higher value.
   - Feature name: S / M / L / XL complexity
   - Brief justification for the rating
   - Flag features that seem simple but are actually complex

3. TECHNOLOGY CONSIDERATIONS
   - Frameworks and languages that fit well
   - Third-party APIs or services needed
   - Infrastructure requirements (hosting, storage, CDN)
   - Development tooling recommendations

4. TECHNICAL RISKS
   - What could be harder than expected?
   - Scalability concerns
   - Integration challenges
   - Data migration or persistence challenges

5. PERFORMANCE CONSIDERATIONS
   - Expected scale (users, requests, data volume)
   - Latency requirements
   - Offline/degraded mode needs
   - Cost implications at scale (provide ±50% sensitivity range)

6. PLATFORM & DEPLOYMENT RISKS
   - Platform-specific limitations (iOS vs Android differences, browser
     compatibility, PWA push notification gaps, etc.)
   - Single points of failure (SPOFs) in the architecture
   - Vendor lock-in risks and mitigation strategies
   - Minimum Viable Team: smallest team composition needed to build and
     maintain this system (roles + estimated headcount)

FORMAT: Use structured markdown with clear headers.
Be HONEST about complexity — flag things that sound easy but are not.
Provide concrete technology names, not abstract categories.

OUTPUT INSTRUCTIONS:
1. Write your complete findings to: .prd-workspace/tech-findings.md
2. After writing the file, send a SHORT notification to the team lead
   via SendMessage confirming your findings are ready.
   Do NOT include the full findings in the message — just confirm
   the file is written and give a 2-3 sentence summary.
```

## Team Step 3: Research Phase

**CRITICAL LEAD INSTRUCTION:** Wait for ALL teammates to complete their tasks before proceeding to the Debate Phase. Do NOT start writing the PRD, do NOT do research yourself, and do NOT proceed to Team Step 4 until every teammate has confirmed their findings are written to the workspace.

All teammates (3 core + specialists if activated) research in parallel. The lead waits for ALL teammates to complete their findings.

**Lead behavior during research:**
- Wait for your teammates to complete their tasks before proceeding
- Monitor teammate progress via task list — check that all tasks move to `completed`
- Teammates notify automatically when they go idle after finishing; do NOT poll manually
- If a teammate goes idle without sending a findings notification, send a direct message prompting them
- When a teammate confirms findings are ready, verify the file exists by reading `.prd-workspace/{role}-findings.md`
- If a file is missing or empty after teammate confirms, send them a direct message asking them to rewrite it
- Do NOT start writing the PRD yet
- Do NOT do research yourself — wait for teammates
- Only proceed to Team Step 4 when ALL expected findings files exist and are non-empty

## Team Step 4: Debate Phase

Once all teammates have produced findings (verified via workspace files), the lead broadcasts a debate instruction to all teammates:

```
All research is complete. Read the other teammates' findings from these files
using the Read tool:

- Product Strategist: .prd-workspace/product-findings.md
- UX Researcher: .prd-workspace/ux-findings.md
- Tech Analyst: .prd-workspace/tech-findings.md
- [Specialist 1]: .prd-workspace/{role}-findings.md (if activated)
- [Specialist 2]: .prd-workspace/{role}-findings.md (if activated)
- [Specialist 3]: .prd-workspace/{role}-findings.md (if activated)

Read ALL files, then produce your debate response.

Write your debate response to: .prd-workspace/{your-role}-debate.md

After writing, send a SHORT notification to the team lead confirming
your debate response is ready. Do NOT include the full response in the
message — just confirm the file is written.

DEBATE INSTRUCTIONS:
Review the other teammates' findings carefully. Then respond with:

1. AGREEMENTS: What findings from other teammates support your research?
2. CHALLENGES: What assumptions or conclusions do you disagree with? Why?
3. TENSIONS: Where do different perspectives conflict? (e.g., UX wants X but Tech says it's XL complexity)
4. PROPOSED RESOLUTIONS: For each tension, suggest a compromise or decision.
5. SPECIFIC CHALLENGES (answer ALL that apply to your role):
   - Product Strategist: Are the P0 features truly minimal for MVP? Are
     acceptance criteria objectively verifiable? Are feature dependencies
     correctly ordered? Is anything in scope that should be deferred?
   - UX Researcher: Do the personas reflect the stated target demographics?
     Are pain points sourced or assumed? Are there content safety gaps?
   - Tech Analyst: Are any complexity ratings understated? Are there
     missing platform risks? Is the minimum viable team realistic?
   - [Specialist — include if activated, see Specialist Debate Challenges
     in the Conditional Specialists section for role-specific challenges]

Be constructive but honest. The goal is to find the best path forward,
not to win arguments. Flag real tradeoffs clearly.
```

The lead collects all debate notifications (1 round of debate is sufficient).

**CRITICAL LEAD INSTRUCTION:** After broadcasting the debate instruction, wait for ALL teammates to complete their debate responses before proceeding to synthesis. Do NOT start Team Step 5 until every teammate has confirmed their debate file is written.

**Lead behavior during debate:**
- Wait for your teammates to complete their tasks before proceeding
- Monitor task list for all debate tasks to reach `completed`
- If a teammate goes idle without sending a debate notification, send them a direct message with explicit instructions to produce their debate response and write it to `.prd-workspace/{role}-debate.md`
- Only proceed to Team Step 5 when ALL expected debate files exist and are non-empty
- Do not skip any teammates

## Team Step 5: Synthesis

The lead reads all artifacts from the workspace:
- Research: `.prd-workspace/{role}-findings.md` (3 core + 0-3 specialist files)
- Debate: `.prd-workspace/{role}-debate.md` (3 core + 0-3 specialist files)

These files persist regardless of context compaction or message delivery issues. If the lead's context was compacted, re-read the files before synthesizing.

Combined with the original product idea + user's scoping answers, generate the PRD at `dev-docs/prd.md` using the **Team PRD Template** (see below).

**Synthesis rules:**
- Where teammates agree, state the finding confidently
- Where teammates debated, document the resolution in "Resolved Tradeoffs"
- Where teammates couldn't agree, put it in "Open Questions"
- Use feature definitions and acceptance criteria from Product Strategist
- Tag functional requirements with complexity from Tech Analyst (S/M/L/XL)
- Use personas from UX Researcher (not generic ones)
- If Business Analyst specialist activated: include competitor analysis and Market Context (§2)
- If Designer specialist activated: include design system specifications
- If specialist was activated: integrate specialist findings into existing sections via subsections AND add the specialist's standalone section (§12A or §12B)
- Label specialist contributions: `[Added by {Specialist Name}]`

## Team Step 5.5: Quality Gate Validation

After synthesizing the PRD, run the same Quality Gate Validation as Solo Step 3.5 (see above). All 8 universal gates apply (QG-001 through QG-008). If a specialist was activated, also run the specialist-specific quality gates (see Specialist Quality Gates section). Fix ERROR-level issues before presenting. Append the Quality Gate Results table to the PRD.

## Team Step 6: Cleanup

After the PRD is written and quality gates pass:
1. Send shutdown requests to all teammates (core + specialist)
2. Wait for all shutdown confirmations
3. Clean up the team (TeamDelete)
4. Delete the workspace: remove `.prd-workspace/` directory
5. Report results to user (include quality gate summary and specialist contribution summary if applicable)

---

# CONDITIONAL SPECIALISTS

Specialists are optional domain experts that JOIN the core team (Product Strategist + UX Researcher + Tech Analyst) as additional teammates when the project matches their domain. They ADD specialized sections and enhance existing ones — they never replace core teammates.

## Architecture

```
Core team: 3 teammates (always: Product Strategist, UX Researcher, Tech Analyst)
Specialist: 0-3 (max 3, up from 2 in v2.2.x)
Total specialist pool: 7 (Business Analyst, Designer, SEO, Mobile, Enterprise, Growth, AI)
Detection: keyword scan → LLM judgment → user confirmation
Activation: Lead SUGGESTS, user APPROVES — never auto-spawned

Specialist contribution model:
- Enhance existing PRD sections via subsections (e.g., ### 6.4 SEO Requirements)
- Add max 1 new standalone section per specialist (lettered insert: ## 12A, ## 12B, ## 12C)
- Specialist sections are clearly labeled: "[Section added by {Specialist Name}]"
```

## Project Category Taxonomy

| Category | Trigger Keywords | Default Specialist |
|----------|-----------------|-------------------|
| Monetized product / SaaS | monetization, revenue, pricing, subscription, freemium, B2B, SaaS, business model, ROI, competitor, go-to-market, startup, investors, KPI, conversion, churn, LTV, CAC | Business Analyst |
| Visual UI product | webapp, web app, website, landing page, mobile app, desktop app, dashboard, admin panel, portal, UI, interface, frontend, design system | Designer |
| Content website / blog / PBN | SEO, blog, content site, PBN, niche site, affiliate, content marketing | SEO Strategist |
| Native mobile app | iOS, Android, mobile app, native app, React Native, Flutter, Swift, Kotlin | Mobile Platform Strategist |
| Enterprise / regulated product | enterprise, compliance, HIPAA, GDPR, SOC2, regulated, government | Enterprise & Compliance Strategist |
| Marketplace / platform | marketplace, platform, two-sided, multi-sided, network effects | Growth Strategist |
| AI-powered product | AI, LLM, GPT, Claude, prompt, chatbot, copilot, assistant, generative, NLP, model, fine-tune, RAG, embeddings, agent, inference | AI Prompt Engineer |
| E-commerce | shop, store, e-commerce, cart, checkout, catalog | Business Analyst (secondary: SEO) |
| Developer tool | API, SDK, CLI, developer tool, dev experience | (none — core team sufficient) |
| Internal tool | internal, back-office, admin | (none — core team sufficient) |

**Important distinction**: A project *built with* AI tools (e.g., using Claude Code) does NOT trigger the AI Prompt Engineer. Only projects that *deliver AI features to end users* qualify.

## Detection Logic

Run during Team Step 1.5 (after scoping questions, before spawning):

```
THREE-STEP DETECTION:

Step 1 — Keyword Scan:
  Scan product description + user answers for trigger keywords from the taxonomy.
  If 3+ keywords match a single category → strong signal.
  If 1-2 keywords → weak signal, proceed to Step 2.
  If 0 keywords → skip to Step 3 (no specialist).

Step 2 — Contextual Inference:
  Consider the product holistically:
  - Is the domain expertise CORE to the product's success?
  - Would the core 3 teammates miss critical domain-specific requirements?
  - For AI products: is this a "uses AI as a build tool" project or
    "delivers AI to users" project? Only the latter triggers AI Prompt Engineer.
  If yes to first two → recommend specialist.

Step 3 — User Confirmation:
  Present recommendation via AskUserQuestion:

  "Based on your product description, this appears to be a [category] project.
   I recommend adding a [Specialist Name] to the research team for
   domain-specific analysis."

  Options:
  1. "Add [Specialist] (Recommended)" — adds as 4th teammate
  2. "Add [Alternative Specialist] instead" — different specialist
  3. "Skip specialist — core team only" — no specialist
  4. "Add multiple specialists: [Specialist] + [Second] + [Third]" — max 3 specialists

  If user picks option 4, spawn all requested specialists (max 3). Never auto-add more than 3.
  If no category matches, skip this step entirely (no specialist).
```

## Specialist Roster

### 1. Business Analyst

**Activates for**: Monetized products, B2B SaaS, marketplaces, e-commerce, products with pricing/subscription models

```
You are the Business Analyst specialist for a PRD research team. Your job is to
deeply investigate the market and business perspective of this product idea.

RESEARCH STANDARDS (apply to all sections):
- Cite sources when making claims about user behavior or market data
- Distinguish between FACTS (sourced), ESTIMATES (reasonable inference),
  and ASSUMPTIONS (educated guess) using inline labels
- When providing numbers, include ranges rather than single-point estimates
- Ground all recommendations in specific evidence, not generic best practices

PRODUCT IDEA: [insert product description]
USER CONTEXT: [insert lead Q&A answers]

Research and produce a structured findings document covering:

1a. DIRECT COMPETITOR ANALYSIS
    Identify 5-8 direct competitors (products solving the same problem):
    - Name, pricing, target audience
    - Strengths and weaknesses
    - What they do well that we should learn from
    - Gaps or opportunities they miss

1b. INDIRECT COMPETITORS & SUBSTITUTES
    Identify 3-5 alternatives users might choose instead (different
    category, same job-to-be-done):
    - Name, how users use it as a substitute
    - Why users might prefer this over a purpose-built solution

2. DIFFERENTIATION STRATEGY
   - What could set this product apart?
   - Is the differentiation sustainable?
   - What's the unique value proposition?

3a. MONETIZATION OPTIONS
    Propose 2-3 viable business models:
    - Model A: [approach] — Pros / Cons / Revenue potential
    - Model B: [approach] — Pros / Cons / Revenue potential
    - Recommended: [which and why]

3b. FINANCIAL SCENARIOS
    For the recommended model, provide three projections:

    | Scenario | Yr 1 Users | Conversion | ARPU | Revenue | Key Assumption |
    |----------|-----------|------------|------|---------|----------------|
    | Pessimistic | [range] | [%] | [$] | [$] | [what goes wrong] |
    | Baseline | [range] | [%] | [$] | [$] | [expected conditions] |
    | Optimistic | [range] | [%] | [$] | [$] | [what goes right] |

    Verify all arithmetic: price × users × conversion = revenue for EACH row.
    Show the calculation inline (e.g., "1,000 × 5% × $20 = $1,000/mo").

4. SUCCESS METRICS (KPIs)
   Define measurable success indicators with benchmarks:
   - Acquisition metrics (signups, downloads) — cite industry benchmark or label [Hypothesis]
   - Engagement metrics (DAU/MAU, session length, retention) — cite benchmark
   - Business metrics (revenue, conversion, churn) — cite benchmark
   - North star metric and why
   - Distinguish TAM (total addressable market) / SAM (serviceable) / SOM (obtainable)

5a. GROWTH CONSIDERATIONS
    - User acquisition channels
    - Retention drivers (what keeps users coming back?)
    - Network effects or viral loops (if applicable)
    - Expansion opportunities (new markets, features)

5b. SEASONAL & CYCLICAL FACTORS
    - Are there seasonal patterns in this market?
    - Launch timing implications
    - Event-driven demand spikes

FORMAT: Use structured markdown with clear headers.
Focus on what makes this VIABLE, not just desirable.
Use concrete numbers and comparisons where possible.

OUTPUT INSTRUCTIONS:
1. Write your complete findings to: .prd-workspace/business-findings.md
2. After writing the file, send a SHORT notification to the team lead
   via SendMessage confirming your findings are ready.
   Do NOT include the full findings in the message — just confirm
   the file is written and give a 2-3 sentence summary.
```

### 2. Designer

**Activates for**: Web applications, websites, mobile apps, desktop apps, dashboards, any product with a visual user interface

```
You are the Designer specialist for a PRD research team. Your job is to deeply
investigate the design system, visual strategy, interaction patterns, and
UI architecture for this product.

RESEARCH STANDARDS (apply to all sections):
- Cite sources when making claims about design patterns or usability data
- Distinguish between FACTS (sourced), ESTIMATES (reasonable inference),
  and ASSUMPTIONS (educated guess) using inline labels
- Ground all recommendations in specific evidence, not generic best practices

PRODUCT IDEA: [insert product description]
USER CONTEXT: [insert lead Q&A answers]

Research and produce a structured findings document covering:

1. DESIGN SYSTEM FOUNDATIONS
   - Visual tone and personality (minimal, playful, corporate, technical, etc.)
   - Color palette strategy (primary, secondary, semantic colors for
     success/warning/error, dark/light mode considerations)
   - Typography scale and hierarchy (headings, body, captions, monospace if needed)
   - Spacing and layout system (grid system, consistent spacing scale)
   - Iconography direction (style: outlined/filled/duotone, recommended libraries)

2. COMPONENT LIBRARY & PATTERNS
   - Recommended component library based on tech stack (e.g., shadcn/ui for
     Next.js, Material UI for React, Vuetify for Vue — be specific)
   - Core component inventory needed for the product (buttons, forms, cards,
     modals, tables, navigation, tooltips, etc.)
   - Component state definitions (default, hover, active, disabled, error, loading)
   - Design token recommendations (colors, spacing, radii, shadows as tokens)

3. LAYOUT & RESPONSIVE STRATEGY
   - Breakpoint strategy (mobile-first vs desktop-first, specific breakpoints)
   - Layout patterns per major view (sidebar + content, top nav + grid,
     single column, split pane, etc.)
   - Mobile adaptation strategy (what collapses, what reflows, what gets hidden)
   - Touch target sizing for mobile (minimum 44x44px per WCAG)

4. KEY SCREENS & NAVIGATION
   - Screen inventory with wireframe-level layout descriptions for 3-5 key screens
   - Navigation structure and patterns (top bar, side nav, tab bar, breadcrumbs)
   - Content density guidelines (data-heavy vs. marketing vs. form-heavy)
   - Empty states, loading states, error states design direction

5. ACCESSIBILITY (Visual Layer)
   - Color contrast compliance targets (WCAG AA minimum, AAA where feasible)
   - Focus indicator styling approach
   - Motion/animation policy (respect prefers-reduced-motion)
   - Text sizing and readability (minimum sizes, line heights, max line widths)

6. DESIGN-DEVELOPMENT HANDOFF
   - Recommended design tools and workflow (Figma, Storybook, etc.)
   - Token-based theming approach (CSS variables, Tailwind config, etc.)
   - Component documentation expectations
   - Design QA process recommendations

FORMAT: Use structured markdown with clear headers.
Be SPECIFIC about component libraries, color values, and breakpoints — no generic
"use a modern design system." Recommend concrete tools and libraries that match
the likely tech stack.

OUTPUT INSTRUCTIONS:
1. Write your complete findings to: .prd-workspace/designer-findings.md
2. After writing the file, send a SHORT notification to the team lead
   via SendMessage confirming your findings are ready.
   Do NOT include the full findings in the message — just confirm
   the file is written and give a 2-3 sentence summary.
```

### 3. SEO Strategist

**Activates for**: Content websites, blogs, PBNs, affiliate sites, e-commerce

```
You are the SEO Strategist specialist for a PRD research team. Your job is to
deeply investigate the search engine optimization and content strategy
requirements for this product.

RESEARCH STANDARDS (apply to all sections):
- Cite sources when making claims about user behavior or market data
- Distinguish between FACTS (sourced), ESTIMATES (reasonable inference),
  and ASSUMPTIONS (educated guess) using inline labels
- When providing numbers, include ranges rather than single-point estimates
- Ground all recommendations in specific evidence, not generic best practices

PRODUCT IDEA: [insert product description]
USER CONTEXT: [insert lead Q&A answers]

Research and produce a structured findings document covering:

1. KEYWORD & SEARCH LANDSCAPE
   - Primary keyword clusters (head terms + long-tails)
   - Search volume estimates and trends (cite tool or label [Estimated])
   - Search intent mapping (informational / commercial / transactional)
   - SERP feature opportunities (featured snippets, PAA, knowledge panels)

2. CONTENT ARCHITECTURE
   - Topic cluster / hub-and-spoke model
   - Content silo structure
   - Internal linking strategy
   - Content gap analysis vs top 3 competitors

3. TECHNICAL SEO REQUIREMENTS
   - Site architecture for crawlability
   - Core Web Vitals targets (LCP, FID, CLS with specific thresholds)
   - Schema markup requirements (specific types)
   - Indexation strategy (what to index, what to noindex)

4. LINK BUILDING & AUTHORITY
   - Domain authority baseline and targets
   - Link acquisition strategy (cite specific tactics)
   - Competitor backlink profile analysis
   - Content types that attract natural links

5. E-E-A-T STRATEGY
   - Experience, Expertise, Authoritativeness, Trustworthiness signals
   - Author entity requirements
   - Trust signals (reviews, citations, credentials)

6. CONTENT OPERATIONS
   - Publishing cadence recommendation (with rationale)
   - Content refresh/decay strategy
   - SEO monitoring KPIs (organic traffic, rankings, CTR)

7. LOCAL/INTERNATIONAL SEO (conditional — if applicable)
   - Hreflang strategy
   - Local listing requirements
   - Geo-targeting approach

8. MONETIZATION-SEO ALIGNMENT
   - How monetization model affects SEO (e.g., affiliate link density)
   - Ad placement impact on Core Web Vitals
   - Conversion path optimization from organic traffic

FORMAT: Use structured markdown. Be specific with numbers, not vague.
Ground SEO recommendations in actual search data, not generic advice.

OUTPUT INSTRUCTIONS:
1. Write your complete findings to: .prd-workspace/seo-findings.md
2. After writing the file, send a SHORT notification to the team lead
   via SendMessage confirming your findings are ready.
   Do NOT include the full findings in the message — just confirm
   the file is written and give a 2-3 sentence summary.
```

### 4. Mobile Platform Strategist

**Activates for**: Native mobile apps, cross-platform mobile, mobile-first products

```
You are the Mobile Platform Strategist specialist for a PRD research team.
Your job is to deeply investigate the mobile platform strategy, app store
requirements, and mobile-specific UX considerations for this product.

RESEARCH STANDARDS (apply to all sections):
- Cite sources when making claims about user behavior or market data
- Distinguish between FACTS (sourced), ESTIMATES (reasonable inference),
  and ASSUMPTIONS (educated guess) using inline labels
- When providing numbers, include ranges rather than single-point estimates
- Ground all recommendations in specific evidence, not generic best practices

PRODUCT IDEA: [insert product description]
USER CONTEXT: [insert lead Q&A answers]

Research and produce a structured findings document covering:

1. PLATFORM STRATEGY
   - Native vs cross-platform decision framework
   - Platform-specific capabilities needed (camera, GPS, sensors, etc.)
   - OS version support matrix with market share rationale

2. MOBILE UX REQUIREMENTS
   - Gesture and interaction patterns
   - Offline-first requirements
   - Push notification strategy
   - Deep linking architecture

3. APP STORE STRATEGY
   - ASO (App Store Optimization) requirements
   - Category selection rationale
   - Rating/review acquisition strategy
   - App Store guideline compliance risks

4. MOBILE PERFORMANCE
   - App size budget (with rationale by market)
   - Cold start time targets
   - Battery impact assessment
   - Network resilience (2G/3G/WiFi behavior)

5. MOBILE-SPECIFIC RISKS
   - Platform rejection risks
   - OS deprecation timeline
   - Device fragmentation impact

6. MOBILE MONETIZATION
   - In-app purchase vs subscription vs ad-supported
   - Platform fee impact (Apple 30%, Google 15-30%)
   - Platform-specific billing requirements

FORMAT: Use structured markdown. Be specific about platform versions,
device targets, and performance budgets — no generic "works on mobile."

OUTPUT INSTRUCTIONS:
1. Write your complete findings to: .prd-workspace/mobile-findings.md
2. After writing the file, send a SHORT notification to the team lead
   via SendMessage confirming your findings are ready.
   Do NOT include the full findings in the message — just confirm
   the file is written and give a 2-3 sentence summary.
```

### 5. Enterprise & Compliance Strategist

**Activates for**: Enterprise SaaS, regulated industries, government, healthcare, fintech

```
You are the Enterprise & Compliance Strategist specialist for a PRD research
team. Your job is to deeply investigate the regulatory, compliance, and
enterprise integration requirements for this product.

RESEARCH STANDARDS (apply to all sections):
- Cite sources when making claims about user behavior or market data
- Distinguish between FACTS (sourced), ESTIMATES (reasonable inference),
  and ASSUMPTIONS (educated guess) using inline labels
- When providing numbers, include ranges rather than single-point estimates
- Ground all recommendations in specific evidence, not generic best practices

PRODUCT IDEA: [insert product description]
USER CONTEXT: [insert lead Q&A answers]

Research and produce a structured findings document covering:

1. REGULATORY LANDSCAPE
   - Applicable regulations (GDPR, HIPAA, SOC2, PCI-DSS, etc.)
   - Compliance requirements per market
   - Data residency requirements
   - Audit trail requirements

2. ENTERPRISE INTEGRATION
   - SSO/SAML/OIDC requirements
   - RBAC model design
   - API governance and rate limiting
   - Enterprise procurement process alignment

3. SECURITY REQUIREMENTS
   - Encryption standards (at-rest, in-transit)
   - Vulnerability management process
   - Incident response plan outline
   - Penetration testing schedule

4. DATA GOVERNANCE
   - Data classification scheme
   - Retention and deletion policies
   - Cross-border data transfer mechanisms
   - Right to erasure implementation

5. ENTERPRISE PRICING
   - Enterprise tier structure
   - Volume licensing model
   - SLA tiers and uptime guarantees
   - Support tier definitions

6. COMPLIANCE ROADMAP
   - Phase 1 compliance (minimum viable compliance)
   - Certification timeline (SOC2, ISO 27001, etc.)
   - Compliance cost estimates

FORMAT: Use structured markdown. Name specific regulations with section
references, not just acronyms. Be precise about compliance requirements.

OUTPUT INSTRUCTIONS:
1. Write your complete findings to: .prd-workspace/enterprise-findings.md
2. After writing the file, send a SHORT notification to the team lead
   via SendMessage confirming your findings are ready.
   Do NOT include the full findings in the message — just confirm
   the file is written and give a 2-3 sentence summary.
```

### 6. Growth Strategist

**Activates for**: Marketplaces, platforms, SaaS products with network effects

```
You are the Growth Strategist specialist for a PRD research team. Your job
is to deeply investigate the growth mechanics, acquisition strategy, and
marketplace dynamics for this product.

RESEARCH STANDARDS (apply to all sections):
- Cite sources when making claims about user behavior or market data
- Distinguish between FACTS (sourced), ESTIMATES (reasonable inference),
  and ASSUMPTIONS (educated guess) using inline labels
- When providing numbers, include ranges rather than single-point estimates
- Ground all recommendations in specific evidence, not generic best practices

PRODUCT IDEA: [insert product description]
USER CONTEXT: [insert lead Q&A answers]

Research and produce a structured findings document covering:

1. GROWTH MODEL
   - Primary growth loops (viral, paid, content, sales)
   - Network effects analysis (if applicable)
   - Supply/demand balance strategy (for marketplaces)
   - Referral mechanism design

2. ACQUISITION CHANNELS
   - Channel-specific CAC estimates (cite benchmarks or label [Hypothesis])
   - Channel prioritization matrix
   - Cold start / chicken-and-egg problem resolution
   - Geographic expansion sequence

3. ACTIVATION & RETENTION
   - Activation metric definition
   - Onboarding optimization targets
   - Retention cohort targets (D1, D7, D30 — cite benchmarks)
   - Churn prediction signals

4. MONETIZATION OPTIMIZATION
   - Pricing experimentation roadmap
   - LTV:CAC ratio targets (cite industry benchmarks)
   - Expansion revenue opportunities
   - Payment failure recovery

5. MARKETPLACE DYNAMICS (conditional — if applicable)
   - Liquidity metrics
   - Take rate benchmarks
   - Trust & safety scaling
   - Disintermediation prevention

6. GROWTH INFRASTRUCTURE
   - Analytics and attribution requirements
   - A/B testing infrastructure needs
   - Feature flagging requirements
   - Event tracking taxonomy

FORMAT: Use structured markdown. Cite growth benchmarks and CAC ranges
from comparable companies. Be specific about metrics and targets.

OUTPUT INSTRUCTIONS:
1. Write your complete findings to: .prd-workspace/growth-findings.md
2. After writing the file, send a SHORT notification to the team lead
   via SendMessage confirming your findings are ready.
   Do NOT include the full findings in the message — just confirm
   the file is written and give a 2-3 sentence summary.
```

### 7. AI Prompt Engineer

**Activates for**: AI-powered products that deliver AI features to end users (chatbots, copilots, AI assistants, generative AI apps, RAG systems, AI agents)

**Important**: This specialist is for products that DELIVER AI features to end users — not for products that merely USE AI in development.

```
You are the AI Prompt Engineer specialist for a PRD research team. Your job
is to deeply investigate the AI/ML product architecture, prompt strategy,
model integration, and safety requirements for this product.

RESEARCH STANDARDS (apply to all sections):
- Cite sources when making claims about model capabilities or benchmarks
- Distinguish between FACTS (sourced), ESTIMATES (reasonable inference),
  and ASSUMPTIONS (educated guess) using inline labels
- When providing numbers, include ranges rather than single-point estimates
- Ground all recommendations in specific evidence, not generic best practices

IMPORTANT DISTINCTION: This specialist is for products that DELIVER AI
features to end users — not for products that merely USE AI in development.

PRODUCT IDEA: [insert product description]
USER CONTEXT: [insert lead Q&A answers]

Research and produce a structured findings document covering:

1. AI ARCHITECTURE & MODEL STRATEGY
   - Model selection rationale (which models, why, tradeoffs)
   - Cost/quality/latency tradeoff analysis per feature
   - Provider strategy (single vs multi-provider, fallback chains)
   - Fine-tuning vs prompt engineering vs RAG decision framework
   - Model versioning and migration strategy

2. PROMPT ARCHITECTURE
   - System prompt inventory (list every distinct prompt the product needs)
   - Prompt versioning strategy (how to iterate without breaking prod)
   - Prompt-response format specifications (structured output requirements)
   - Few-shot example design and curation approach
   - Chain-of-thought vs direct prompting decisions per feature
   - Context window budget allocation per interaction type

3. EVALUATION FRAMEWORK
   - Quality metrics per prompt (accuracy, relevance, safety, consistency)
   - Automated evaluation pipeline design (evals, benchmarks, regression suites)
   - Human evaluation criteria and sampling strategy
   - A/B testing methodology for prompt variants
   - Regression detection: how to catch quality degradation

4. SAFETY & GUARDRAILS
   - Input validation (prompt injection prevention, PII filtering)
   - Output filtering (content policy, hallucination detection)
   - Jailbreak mitigation strategy
   - Confidence thresholds and uncertainty communication
   - Escalation paths (when AI should defer to humans)
   - Red-teaming plan (adversarial testing approach)

5. TOKEN ECONOMICS & COST MODEL
   - Cost-per-interaction estimates by feature (cite model pricing)
   - Token budget per request type (input + output)
   - Cost scaling projections (at 1K, 10K, 100K MAU)
   - Cost optimization levers (caching, batching, model tiering)
   - Budget ceiling and alerting thresholds

6. RELIABILITY & FALLBACK STRATEGY
   - Provider outage handling (failover to alternative models)
   - Rate limit management and queuing strategy
   - Degraded mode behavior (what works when AI is unavailable)
   - Latency budgets per interaction type (P50, P95, P99)
   - Retry and timeout policies

7. USER EXPERIENCE OF AI
   - Expectation setting (how to communicate AI capabilities and limits)
   - Loading/streaming UX patterns (typing indicators, progressive reveal)
   - Error messaging for AI failures (user-friendly, not technical)
   - Feedback collection mechanism (thumbs up/down, corrections)
   - Transparency: when and how to disclose AI involvement

FORMAT: Use structured markdown with clear headers.
Be SPECIFIC about model names, pricing tiers, and benchmarks — no generic
"use an LLM." Distinguish between current model capabilities and assumed
future capabilities.

OUTPUT INSTRUCTIONS:
1. Write your complete findings to: .prd-workspace/ai-prompt-findings.md
2. After writing the file, send a SHORT notification to the team lead
   via SendMessage confirming your findings are ready.
   Do NOT include the full findings in the message — just confirm
   the file is written and give a 2-3 sentence summary.
```

## Specialist Template Contributions

Each specialist ENHANCES existing sections via subsections AND adds max 1 new standalone section (lettered insert after section 12).

| Specialist | Enhances (subsections) | New Standalone Section |
|-----------|------------------------|----------------------|
| SEO Strategist | §6 (FR: SEO requirements), §8 (Tech: crawlability), §4 (KPIs: organic metrics) | §12A SEO & Content Strategy |
| Mobile Platform Strategist | §7 (UX: mobile patterns), §8 (Tech: platform constraints), §10 (Risks: platform rejection) | §12A Mobile Platform Strategy |
| Enterprise & Compliance | §5 (NFR: compliance), §8 (Tech: security infra), §10 (Risks: regulatory) | §12A Compliance & Governance |
| Growth Strategist | §4 (KPIs: growth metrics), §11 (Resources: growth tools), §8 (Tech: analytics infra) | §12A Growth & Acquisition Strategy |
| AI Prompt Engineer | §6 (FR: AI feature specs), §8 (Tech: model infra), §10 (Risks: AI-specific), §7 (UX: AI interaction) | §12A AI Architecture & Prompt Strategy |
| Business Analyst | §2 (Market Context — generates entire section), §4 (KPIs: business metrics) | — (§2 IS the standalone section) |
| Designer | §7 (UX: visual/interaction layer), §8 (Tech: design system infra) | §12A Design System & Visual Strategy |

**Notes:**
- §12A is always the first lettered insert regardless of which specialist
- If 2+ specialists are active, subsequent ones use §12B, §12C
- Section numbers reference the Team PRD Template numbering
- Specialist subsections are labeled: `[Added by {Specialist Name}]`
- Business Analyst is unique: §2 Market Context IS its standalone contribution (not a §12x section)

## Specialist Debate Challenges

When a specialist is active, add their role-specific challenges to the debate broadcast instruction:

```
- SEO Strategist: Are content architecture recommendations backed by search
  volume data? Is the E-E-A-T strategy specific enough? Does the internal
  linking strategy account for the site's actual scale?
- Mobile Platform Strategist: Are platform-specific risks fully enumerated?
  Is the offline strategy realistic for the target markets? Are app store
  compliance risks addressed?
- Enterprise & Compliance Strategist: Are all applicable regulations identified
  with specific section references? Is the compliance timeline realistic?
  Are data residency requirements addressed for each target market?
- Growth Strategist: Are CAC/LTV estimates benchmarked against comparable
  companies? Is the cold-start strategy viable? Are retention targets
  realistic for the category?
- AI Prompt Engineer: Does every AI-facing feature have a named system prompt?
  Are cost projections grounded in actual model pricing (not generic)? Are
  safety guardrails specific (not just "content filtering")? Is the fallback
  strategy realistic for the target latency budget?
- Business Analyst: Are there missing indirect competitors? Do financial
  projections pass arithmetic checks (users × conversion × ARPU = revenue)?
  Are KPI benchmarks sourced or labeled [Hypothesis]? Is the monetization
  strategy realistic for the target market?
- Designer: Do the interaction patterns match user expectations for this
  platform? Are accessibility requirements met (WCAG AA)? Is the design
  system scalable across all proposed features? Does the component inventory
  cover all key screens?
```

---

# PRD TEMPLATES

## Table Classification

Tables in the PRD templates follow a tiered classification:

| Tier | Meaning | Rule |
|------|---------|------|
| **[Locked]** | Arithmetic-verified tables | All columns required. Computed columns must show formula and pass verification. Cannot add/remove columns. |
| **[Baselined]** | Required columns + allowed additions | Core columns must be present. Additional columns may be added if relevant. |
| **[Flexible]** | Guidance only | Column suggestions provided but can be adapted to the product's needs. |

Tables are labeled in the templates with their tier. If unlabeled, assume **[Flexible]**.

## Solo PRD Template

Used by solo mode. This is the standard PRD format.

```markdown
# Product Requirements Document: [Product Name]

> Generated: [Date]
> Status: Draft
> Version: 1.0

## Executive Summary

[2-3 sentence overview of the product, its purpose, and primary value proposition]

---

## 1. Problem Statement

### 1.1 Background
[Context and background of the problem space]

### 1.2 Problem Definition
[Clear articulation of the problem being solved]

### 1.3 Current Solutions
[How users currently solve this problem, pain points with existing solutions]

---

## 2. Target Users

### 2.1 Primary Users
[Description of the main user persona(s)]

### 2.2 Secondary Users
[Other stakeholders or user types, if applicable]

### 2.3 User Personas

#### Persona 1: [Name]
- **Role**: [Job title or role]
- **Demographics**: [Age range, location, context — MUST reflect target market demographics provided by user]
- **Goals**: [What they want to achieve]
- **Pain Points**: [Current frustrations — cite source or label [Estimated]]
- **Tech Savviness**: [Low/Medium/High]

[2-3 personas total. Additional personas as needed.]

---

## 3. Goals & Objectives

### 3.1 Product Vision
[Long-term vision for the product]

### 3.2 Product Goals
[Specific, measurable goals for this version]

### 3.3 Success Metrics (KPIs)

> **[Baselined]** — Metric, Target, Benchmark columns required. Additional columns allowed.

| Metric | Target | Benchmark | Measurement Method |
|--------|--------|-----------|-------------------|
| [Metric 1] | [Target value] | [Industry benchmark or [Hypothesis]] | [How to measure] |
| [Metric 2] | [Target value] | [Industry benchmark or [Hypothesis]] | [How to measure] |

### 3.4 Non-Goals
[What this product explicitly will NOT do]

---

## 4. User Stories & Use Cases

### 4.1 User Stories

| ID | As a... | I want to... | So that... | Priority |
|----|---------|--------------|------------|----------|
| US-001 | [user type] | [action] | [benefit] | [P0/P1/P2] |

### 4.2 Key Use Cases

#### UC-001: [Use Case Name]
- **Actor**: [User type]
- **Precondition**: [What must be true before]
- **Main Flow**:
  1. [Step 1]
  2. [Step 2]
  3. [Step 3]
- **Postcondition**: [What is true after]
- **Exceptions**: [What could go wrong]

---

## 5. Features & Requirements

### 5.1 Feature Overview

| Feature | Description | Priority | Status |
|---------|-------------|----------|--------|
| [Feature 1] | [Brief description] | P0 | Planned |

### 5.2 Functional Requirements

#### FR-001: [Requirement Name]
- **Description**: [Detailed description]
- **Acceptance Criteria**:
  - [ ] [Criterion 1]
  - [ ] [Criterion 2]
- **Dependencies**: [Any dependencies]

[Additional requirements...]

### 5.3 Non-Functional Requirements

#### Performance
- [Performance requirement 1]
- [Performance requirement 2]

#### Security
- [Security requirement 1]
- [Security requirement 2]

#### Accessibility
- [Accessibility requirement 1]

#### Scalability
- [Scalability requirement 1]

---

## 6. User Experience

### 6.1 User Flows

#### Flow 1: [Flow Name]
[Start] -> [Step 1] -> [Step 2] -> [End State]

### 6.2 Key Screens/Views
[Description of main UI components or screens]

### 6.3 Design Principles
[Guiding principles for the UX/UI design]

---

## 7. Technical Considerations

### 7.1 Platform & Technology
- **Platform**: [Web/Mobile/Desktop/etc.]
- **Technology Stack**: [If predetermined]

### 7.2 Integrations
[External systems or APIs to integrate with]

### 7.3 Data Requirements
[Data storage, processing, privacy considerations]

### 7.4 Technical Constraints
[Technical limitations or requirements]

---

## 8. Scope & Boundaries

### 8.1 In Scope (v1)
- [Feature/capability 1]
- [Feature/capability 2]

### 8.2 Out of Scope (v1)
- [Feature/capability to defer]
- [Feature/capability to defer]

### 8.3 Future Considerations (v2+)
- [Potential future enhancement 1]
- [Potential future enhancement 2]

---

## 9. Dependencies & Risks

### 9.1 Dependencies

| Dependency | Type | Owner | Status |
|------------|------|-------|--------|
| [Dependency 1] | [Internal/External] | [Team/Person] | [Status] |

### 9.2 Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| [Risk 1] | [H/M/L] | [H/M/L] | [Mitigation strategy] |

### 9.3 Assumptions
- [Assumption 1]
- [Assumption 2]

---

## 10. Resource Plan

### 10.1 Team Composition

| Role | Count | Responsibility |
|------|-------|---------------|
| [Role 1] | [N] | [What they do] |
| [Role 2] | [N] | [What they do] |

### 10.2 Budget Estimate

| Category | Estimate (Monthly) | Notes |
|----------|-------------------|-------|
| Infrastructure | [$range] | [Details] |
| Third-party APIs | [$range] | [Details] |
| Personnel | [$range] | [Details] |

### 10.3 Runway & Break-Even
[Estimated months to MVP, months to break-even based on financial scenarios]

---

## 11. Ethics & Content Safety

> **Conditional section** — include ONLY if the product involves AI content,
> health/wellness, financial advice, vulnerable users, or UGC at scale.
> If not applicable, replace with: "Not applicable — product does not trigger
> ethics review criteria."

### 11.1 Content Boundaries

| Category | May | Must NOT |
|----------|-----|----------|
| [Category 1] | [Allowed behavior] | [Prohibited behavior] |

### 11.2 Sensitive Topics Policy

| Topic | Handling | Rationale |
|-------|----------|-----------|
| [Topic 1] | [Disclaimer / Gate / Block] | [Why this approach] |

### 11.3 User Safety Measures
- **Disclaimers**: [Where and what disclaimers are shown]
- **Crisis Resources**: [When to surface helplines or professional referrals]
- **Human Escalation**: [When automated responses are insufficient]

### 11.4 Content Moderation Framework
[Automated vs manual moderation, response time targets, appeal process]

---

## 12. Open Questions

[Any remaining questions or decisions to be made]

- [ ] [Question 1]
- [ ] [Question 2]

---

> **Specialist Awareness (solo mode only):**
> If this product clearly falls into a specialist category (website → SEO,
> mobile → Mobile, AI-powered → AI, etc.), add a note here:
> "This product would benefit from specialist analysis in [domain].
> Consider regenerating with team mode: `/prd --team <description>`"

---

## Quality Gate Results

| Gate | Status | Notes |
|------|--------|-------|
| QG-001 Revenue Math | PASS / FAIL / N/A | [details] |
| QG-002 Phase Dependencies | PASS / FAIL / N/A | [details] |
| QG-003 KPI Benchmarks | PASS / WARN | [details] |
| QG-004 Acceptance Testability | PASS / FAIL | [details] |
| QG-005 Claim Attribution | PASS / WARN | [details] |
| QG-006 Scope Feasibility | PASS / WARN | [details] |
| QG-007 Complexity Discreteness | PASS / FAIL | [details] |
| QG-008 Specialist Integration | N/A | Solo mode — no specialist |

---

## Appendix

### A. Glossary
[Define any domain-specific terms]

### B. References
[Links to research, competitive analysis, etc.]

### C. Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | [Date] | [Author] | Initial draft |
```

## Team PRD Template

Used by team mode. Extends the solo template with additional sections from multi-perspective research.

The team template includes ALL sections from the solo template, PLUS these additions and modifications:

### Addition: Market Context (conditional Section 2 — Business Analyst specialist only)

> **Conditional section** — included ONLY when Business Analyst specialist is activated.
> If Business Analyst was not activated, §2 is skipped and numbering jumps from Executive Summary to §1 Problem Statement (stable numbering — no renumbering).

Insert after Executive Summary, before Problem Statement:

```markdown
---

## 2. Market Context

### 2.1 Direct Competitor Landscape (5-8 competitors)

| Competitor | Pricing | Target Audience | Strengths | Weaknesses |
|------------|---------|-----------------|-----------|------------|
| [Competitor 1] | [Price] | [Audience] | [Strengths] | [Weaknesses] |
| [Competitor 2] | [Price] | [Audience] | [Strengths] | [Weaknesses] |
[5-8 rows required]

### 2.2 Indirect Competitors & Substitutes (3-5 alternatives)

| Alternative | Category | How Users Use It | Why They Might Prefer It |
|-------------|----------|-----------------|--------------------------|
| [Alternative 1] | [Category] | [Usage] | [Reason] |
[3-5 rows required]

### 2.3 Differentiation Strategy
[Key differentiators identified through team research and debate]

### 2.4 Monetization Strategy
[Business Analyst's recommended approach with rationale]

### 2.5 Financial Scenarios

> **[Locked Table]** — All columns required. Revenue column must equal Users × Conversion × ARPU. Show arithmetic inline.

| Scenario | Yr 1 Users | Conversion | ARPU | Revenue | Arithmetic Check | Key Assumption |
|----------|-----------|------------|------|---------|-----------------|----------------|
| Pessimistic | [range] | [%] | [$] | [$] | [users × conv × ARPU = revenue] | [what goes wrong] |
| Baseline | [range] | [%] | [$] | [$] | [users × conv × ARPU = revenue] | [expected conditions] |
| Optimistic | [range] | [%] | [$] | [$] | [users × conv × ARPU = revenue] | [what goes right] |
```

### Modification: Enhanced Functional Requirements

Each FR gets a single discrete complexity tag from the Tech Analyst (no ranges, no compound values):

```markdown
#### FR-001: [Requirement Name]
- **Description**: [Detailed description]
- **Complexity**: [S / M / L / XL — single value only, from Tech Analyst assessment]
- **Acceptance Criteria** (from Product Strategist):
  - [ ] [Criterion 1 — must be objectively verifiable, not process-oriented]
  - [ ] [Criterion 2 — must be measurable outcome, not subjective]
- **Dependencies**: [Any dependencies]
```

### Modification: Enhanced User Personas

Personas come from UX Researcher's research (richer than solo mode):

```markdown
#### Persona 1: [Name]
- **Role**: [Job title or role]
- **Demographics**: [Age range, context]
- **Goals**: [What they want to achieve]
- **Pain Points**: [Current frustrations — specific, not generic]
- **Tech Savviness**: [Low/Medium/High]
- **Usage Scenario**: [A realistic day-in-the-life narrative]
```

### Addition: Specialist Section (conditional, lettered insert after Ethics)

If a specialist was activated, add their standalone section after Ethics & Content Safety:

```markdown
---

## 12A. [Specialist Domain] Strategy
> [Added by {Specialist Name}]

[Specialist-specific content synthesized from their research findings.
Structure follows the specialist's research sections, adapted for PRD format.]
```

If 2-3 specialists were activated, subsequent ones get §12B, §12C. Note: Business Analyst does not use a §12x section — its standalone contribution is §2 Market Context.

### Addition: Resolved Tradeoffs (new section, before Open Questions)

```markdown
---

## 13. Resolved Tradeoffs

Decisions made during multi-perspective analysis:

| # | Tension | Perspectives | Resolution | Rationale |
|---|---------|-------------|------------|-----------|
| 1 | [What conflicted] | [UX vs Tech] | [Decision made] | [Why this resolution] |
| 2 | [What conflicted] | [Tech vs Biz] | [Decision made] | [Why this resolution] |
| 3 | [What conflicted] | [Specialist vs Core] | [Decision made] | [Why this resolution] |
```

### Addition: Research Sources (new appendix section)

```markdown
### D. Research Sources

This PRD was generated using multi-perspective agent team analysis:
- **UX Researcher**: [1-2 sentence summary of key findings]
- **Tech Analyst**: [1-2 sentence summary of key findings]
- **Business Analyst**: [1-2 sentence summary of key findings]
- **[Specialist Name]**: [1-2 sentence summary of key findings] (if activated)
```

### Team PRD Section Numbering

Numbering is STABLE — §2 is reserved for Market Context. When Business Analyst is not active, §2 is simply absent (numbering skips from Executive Summary to §1 Problem Statement, then §3 Target Users, etc.). This avoids renumbering all subsequent sections.

```
Executive Summary
1. Problem Statement
2. Market Context (conditional — only when Business Analyst specialist active)
3. Target Users (enhanced personas from UX Researcher)
4. Goals & Objectives (KPIs with benchmarks)
5. User Stories & Use Cases (from Product Strategist)
6. Features & Requirements (enhanced with complexity tags + acceptance criteria)
7. User Experience
8. Technical Considerations
9. Scope & Boundaries (from Product Strategist)
10. Dependencies & Risks
11. Resource Plan (team composition, budget, runway)
12. Ethics & Content Safety (conditional)
12A. [Specialist Section] (conditional — if specialist activated)
12B. [Second Specialist Section] (conditional — if 2 specialists)
12C. [Third Specialist Section] (conditional — if 3 specialists)
13. Resolved Tradeoffs
14. Open Questions
Quality Gate Results
Appendix (with Research Sources)
```

---

# QUESTION STRATEGY

Applies to solo mode. Team mode uses a different approach (see Team Step 1).

## Adaptive Questioning

The number and type of questions should adapt to the initial input:

**Minimal Input** (just an idea):
- Ask 8-10 questions covering all major areas
- Start with problem/users, end with technical details

**Moderate Input** (idea + some context):
- Ask 5-7 questions focusing on gaps
- Skip areas that are well-defined

**Detailed Input** (comprehensive description):
- Ask 2-4 clarifying questions
- Focus on ambiguities and edge cases

## Question Batching

Use the AskUserQuestion tool efficiently:
- Group related questions when possible
- Provide multiple-choice options when appropriate
- Use "Other" option for open-ended responses
- Batch up to 4 questions per tool call

## Timeline Validation Logic

When the PRD includes phased delivery, validate scope-timeline feasibility:
- Assign complexity points: S=1, M=2, L=4, XL=8
- Sum points per phase
- Flag any phase exceeding 16 points as potentially overloaded
- Add a risk note for any XL feature in Phase 1

## Skip Conditions

Don't ask about:
- Information clearly stated in the input
- Details that can use reasonable defaults
- Implementation specifics (save for TRD)
- Exact timelines or deadlines

---

# BEST PRACTICES

This skill follows industry-standard PRD best practices:

1. **User-Centric**: Focus on user problems and outcomes, not solutions
2. **Measurable**: Include specific, measurable success criteria with benchmarks
3. **Prioritized**: Use P0/P1/P2 priority levels consistently
4. **Testable**: Write requirements with objectively verifiable acceptance criteria
5. **Scoped**: Clearly define what's in and out of scope
6. **Risk-Aware**: Identify dependencies and risks early
7. **Iterative**: Design for versioned development (v1, v2+)
8. **Accessible**: Write for all stakeholders, not just engineers
9. **Attributed**: Cite sources for claims, label estimates and hypotheses
10. **Arithmetically Sound**: Verify all revenue math and projection consistency
11. **Multi-Perspective** (team mode): Cross-validate requirements from Product, UX, and Tech angles, enhanced by domain specialists
12. **Conflict-Resolved** (team mode): Document tradeoff decisions with rationale
13. **Quality-Gated**: Pass all 8 universal quality gates before presenting (+ specialist gates if activated)
14. **Specialist-Enhanced** (team mode): Activate domain specialists when the product category demands expertise beyond the core team's scope

---

# OUTPUT

- **File**: `dev-docs/prd.md`
- **Format**: Markdown with clear section hierarchy
- **Length**: Comprehensive but not excessive (aim for clarity)
- **Mode indicator**: Team-generated PRDs include a note in the header:
  ```
  > Generated: [Date]
  > Status: Draft
  > Version: 1.0
  > Mode: Multi-perspective (Product + UX + Tech + [Specialist(s)] analysis)
  ```
  If no specialist was activated, omit the specialist names from the Mode line.

---

# EXAMPLES

## Solo Mode Example

```
User: /prd A mobile app that helps people track their daily water intake
Assistant: I will help you create a PRD for a water intake tracking app.
         Let me ask a few questions to understand your vision better.

[Uses AskUserQuestion tool with questions about target users,
platform preference, key features, integration needs]

User: [Answers questions...]
Assistant: Based on your answers, I will now generate a comprehensive PRD.

[Writes dev-docs/prd.md with all sections filled in]
Assistant: I have created the PRD at dev-docs/prd.md. The document includes:
- Executive summary of the water tracking app
- Problem statement about dehydration
- Target user personas
- 12 user stories prioritized P0-P2
- Feature requirements with acceptance criteria
- Technical considerations for mobile development
- Success metrics including DAU and retention targets
```

## Team Mode Example

```
User: /prd --team A fintech app for micro-investments (spare change rounding)

Lead: A few questions before I spin up the research team:
      1. Target market?
User: US first, then EU

Lead: 2. Target demographic?
User: 20-35 year olds new to investing

Lead: This appears to be a regulated fintech product.
      I recommend adding an Enterprise & Compliance Strategist.
      Options: 1. Add specialist (Recommended) 2. Skip
User: Add specialist

Lead: Spawning research team (3 core + 2 specialists)...

      [Product Strategist, UX Researcher, Tech Analyst,
       Business Analyst, Enterprise & Compliance Strategist
       work in parallel]
      [Teammates produce findings, then debate]

      Product Strategist:
        MVP scoped to 8 P0 features, 6 P1 deferred,
        acceptance criteria defined, phasing recommended

      UX Researcher:
        3 personas defined, key friction point identified,
        progressive onboarding recommended

      Tech Analyst:
        Alpaca API for brokerage, Plaid for bank linking,
        2 architecture options with tradeoffs

      Business Analyst (specialist):
        5 competitors analyzed, freemium model recommended,
        north star metric defined

      Enterprise & Compliance Strategist (specialist):
        SEC/FINRA requirements mapped, SOC2 timeline,
        state-by-state licensing analysis

      DEBATE:
        Product vs UX: Feature scope vs user simplicity resolved
        Product vs Tech: Feature complexity compromises reached
        UX vs Tech: Onboarding flow resolved
        Compliance vs Tech: Minimum viable compliance scoped

      Lead: Synthesizing into PRD...

      Created dev-docs/prd.md with:
      - 14 functional requirements (complexity tags + acceptance criteria)
      - §2 Market Context with competitor analysis (from Business Analyst)
      - Research-backed personas (not generic)
      - §12A Compliance & Governance section
      - 3 resolved tradeoffs documented
      - Monetization strategy with financial scenarios
      - Quality gates: 8 universal + 4 specialist (QG-BIZ-1/2, QG-ENT-1/2)
```
---

# SUCCESS CRITERIA

## Solo Mode

A successful solo PRD generation:
- Asks relevant follow-up questions (up to 10, from 10 categories)
- Creates a complete PRD at `dev-docs/prd.md`
- Covers all 12 main sections (including Resource Plan, conditional Ethics)
- Uses consistent priority levels (P0/P1/P2)
- Includes measurable success metrics with benchmarks
- Clearly defines scope boundaries
- Documents assumptions and risks
- Passes all 8 quality gates (ERROR gates fixed, WARNING gates noted)
- Includes Quality Gate Results table
- Includes specialist awareness note if product matches a specialist category

## Team Mode

A successful team PRD generation:
- Asks 3-4 scoping questions (not 10)
- Runs specialist detection (keyword scan → inference → user confirmation)
- Spawns 3 core teammates (Product Strategist + UX Researcher + Tech Analyst) + 0-3 specialists
- Waits for all research to complete before synthesizing
- Runs 1 round of debate between all teammates (with role-specific challenges)
- Tags FRs with single discrete complexity estimates from Tech Analyst AND acceptance criteria from Product Strategist
- Uses research-backed personas from UX Researcher (reflecting target demographics)
- If Business Analyst activated: produces §2 Market Context with competitors and Financial Scenarios
- If Designer activated: includes design system specifications in standalone section
- Includes Resource Plan and conditional Ethics & Content Safety sections
- If specialist activated: includes specialist standalone section (§12A/B/C) + at least 2 subsection enhancements
- Passes all 8 universal quality gates + specialist-specific gates (if applicable)
- Cleans up team after PRD is written (shutdown requests → confirmations → TeamDelete → workspace cleanup)

---

# NOTES

- The skill adapts question depth based on initial input detail
- Questions are batched efficiently (up to 4 per tool call)
- The PRD template can be customized for specific domains
- Open questions section captures items needing future decisions
- Revision history enables PRD evolution tracking
- Team mode requires CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS to be enabled
- Core team (3 teammates) always includes: Product Strategist, UX Researcher, Tech Analyst
- Team mode without specialist uses ~4-6x more tokens than solo mode
- Team mode with 1-3 specialists uses ~6-10x more tokens than solo mode
- If team mode fails (e.g., agent teams not available), falls back to solo mode
- Specialists are additive — they enhance the core team's output
- Max 3 specialists per PRD generation to keep context manageable
- Available specialists: Business Analyst, Designer, SEO Strategist, Mobile Platform Strategist, Enterprise & Compliance Strategist, Growth Strategist, AI Prompt Engineer
- Specialist detection is suggestive, not automatic — user always confirms
- If a teammate goes idle without responding during debate, send a direct message to prompt them
- The AI Prompt Engineer specialist triggers only for products delivering AI to end users, not products built using AI tools
