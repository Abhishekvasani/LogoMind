---
doc_id: LOG-STRAT-001
title: LOGOS Strategy Engine (Brand DNA Builder) v1.0
version: 1.0
status: Approved
governance_level: L2 — Engine Specification
engine_blueprint: CTO Decision #003 (every engine follows the same structure)
last_reviewed: 2026-07-17
related:
  - LOG-DISC-001 Discovery Engine (upstream)
  - RS-LIC-BS-001..005 Brand Strategy Series (knowledge sources)
  - LOG-CREATE-001 Create Engine (downstream consumer)
conformance: "This engine conforms to LM-STD-001 through LM-STD-006 and the Engine Blueprint Standard."
---

# LOG-STRAT-001 — Strategy Engine (Brand DNA Builder)

> *The Strategy Engine is the moment LogoMind stops understanding the client and starts defining the brand. It takes the Discovery output and synthesises it into Brand DNA — the strategic foundation every downstream engine reasons over.*

---

## 1. Mission

Transform the Discovery output (raw understanding of the client, their audience, their category) into a **Brand DNA profile** — a complete, coherent, defensible strategic foundation that every downstream engine (Insight, Create, Judge) reasons over.

The Strategy Engine does not generate creative ideas. It produces the strategic clarity those ideas must serve.

---

## 2. Purpose in the Pipeline

```
LOGOS Discover  →  LOGOS Strategy  →  LOGOS Insight  →  LOGOS Create  →  LOGOS Judge
(raw brief)         (Brand DNA)        (research)        (concepts)       (evaluation)
                       ▲
                       │
              THE STRATEGY ENGINE
              outputs the foundation
              everything else reasons over
```

Every downstream engine depends on the Strategy Engine's output. A weak Brand DNA produces weak research, weak concepts, and weak evaluation. The Strategy Engine is the second most important engine in the system (after Discovery) — because everything downstream inherits its quality.

---

## 3. Inputs

### Required Data (from Discovery Engine output)
- Discovery Summary (the refined brief, post-Discovery-Engine processing)
- Brand Confidence Score (must be ≥ 70% to proceed)
- Stated purpose (RS-LIC-PH-002) — discovered or refined during Discovery
- Identified audience configuration (RS-LIC-BS-003)

### Optional Data
- Existing brand assets (if rebrand)
- Stated positioning aspirations
- Competitor information gathered during Discovery
- Founder stories / origin narratives

### Knowledge Sources (LMKC volumes consulted)
- **RS-LIC-BS-001** Brand Positioning — provides the Positioning Statement template and Audit
- **RS-LIC-BS-002** Brand Differentiation — provides the Three Tests and Five Dimensions
- **RS-LIC-BS-003** Target Audience — provides the Configuration framework
- **RS-LIC-BS-004** Brand Personality — provides the "describe as a person" method
- **RS-LIC-BS-005** Brand Archetypes — provides the Archetype Audit and Twelve Archetypes vocabulary

The Strategy Engine *applies* the Brand Strategy Series — it does not redefine it (CTO Decision: Standards are Inherited, Not Repeated).

---

## 4. Reasoning Steps

```
Step 1: SYNTHESISE PURPOSE
   → Confirm or refine the purpose from Discovery output
   → Apply the Purpose-Discovery Sequence (RS-LIC-PH-002 §4)
   → Test: Is this purpose discovered (authentic) or asserted (aspirational)?

Step 2: CRAFT POSITIONING STATEMENT
   → Use the Positioning Statement template (RS-LIC-BS-001 §4)
   → "For [audience] who [need], [brand] is the [category] that [distinctive
      point], unlike [alternative], because [reason to believe]."
   → Test: Does the statement pass the sacrifice test? (If competitors could
      say the same, it's table-stakes, not positioning.)

Step 3: LOCATE DIFFERENTIATION
   → Apply the Three Tests (RS-LIC-BS-002): Valued, Defensible, Aligned
   → Apply the Five Dimensions: Product, Behaviour, Audience Focus, Voice, Identity
   → Identify where real differentiation actually lives (rarely product alone)
   → Test: Could competitors copy this within 12-24 months?

Step 4: SHARPEN AUDIENCE CONFIGURATION
   → Translate demographics into Configuration (RS-LIC-BS-003):
     concerns, contexts, vocabularies, behaviours
   → Test: Could this describe millions of completely different people?
     (If yes, it's a bucket, not a configuration.)

Step 5: DEFINE PERSONALITY AS CHARACTER
   → Apply "describe as a person" (RS-LIC-BS-004)
   → Coherence test: Do the traits hang together as a believable person?
   → Specificity test: Could this describe any other brand?

Step 6: IDENTIFY ARCHETYPE (if authentically present)
   → Apply the Archetype Audit (RS-LIC-BS-005)
   → Map to Twelve Archetypes vocabulary — discovery, not assignment
   → Test: Is this identification authentic, or imposed? Is there a clean
      archetype at all? (Honest "no clean archetype" is a valid finding.)

Step 7: SYNTHESISE BRAND DNA
   → Combine all six elements into a single Brand DNA profile
   → Coherence check: Do all six reinforce each other? Or do any contradict?
   → Output the Brand DNA document
```

---

## 5. Decision Rules

| Rule | Condition | Action |
|------|-----------|--------|
| **DR-1** | Brand Confidence Score < 70% | Return to Discovery Engine — strategic work is premature |
| **DR-2** | Positioning fails the sacrifice test | Push back: surface the lack of distinctiveness rather than proceed with false positioning |
| **DR-3** | Differentiation fails the Defensible test | Flag as temporary advantage; recommend locating defensible differentiation before proceeding |
| **DR-4** | Personality fails the coherence test | Push back: surface the incoherence; do not output an incoherent character |
| **DR-5** | No authentic archetype identified | Accept "no clean archetype" as a finding; do not impose one |
| **DR-6** | Any element contradicts another (e.g., personality contradicts positioning) | Surface the contradiction; recommend resolution before Brand DNA is finalised |

The Strategy Engine does NOT silently resolve contradictions. It surfaces them. Silent resolution produces incoherent Brand DNA; honest surfacing produces strategic clarity (see §10 Failure Cases).

---

## 6. Confidence Calculation

Each Brand DNA element carries a confidence score (per LM-STD-003):

| Element | Confidence Inputs |
|---------|-------------------|
| Purpose | Strength of behavioural evidence; specificity of articulation |
| Positioning | Defensibility (competitor analysis); audience-valued evidence |
| Differentiation | Survives all Three Tests; dimension identified |
| Audience Configuration | Specificity (configuration vs. bucket); investigation vs. assumption |
| Personality | Coherence; authenticity match |
| Archetype | Authenticity of embodiment; exclusivity (clean vs. mixed) |

**Overall Brand DNA Confidence** = weighted average, with positioning and differentiation weighted highest (they determine defensibility).

If overall confidence < C3 (Moderate), the Strategy Engine flags the Brand DNA as *provisional* and recommends returning to Discovery for additional information.

---

## 7. Outputs

### Primary Output: Brand DNA Document

A single structured document containing:

```yaml
brand_dna:
  purpose: <one-sentence statement, traced to behaviour>
  positioning_statement: <full template-completed statement>
  differentiation:
    primary: <where real differentiation lives + Three Tests evidence>
    secondary: <supporting differentiators>
    defensibility: <C-level + reasoning>
  audience:
    primary: <configuration: concerns, contexts, vocabularies, behaviours>
    secondary: <adjacent audiences, if any>
  personality: <character description, not adjective list>
  archetype:
    primary: <if authentically identified, with evidence>
    secondary: <if a genuine blend>
    finding: <clean / mixed / none>
  emotional_goal: <what the audience should feel>
  differentiators_to_avoid: <claimed but unsupported differentiators>
  contradictions_flagged: <any unresolved incoherence>

metadata:
  confidence: <C-level + reasoning>
  source: <Discovery Engine output + LMKC consultation>
  version: 1.0
```

### Secondary Outputs
- **Strategic Confidence Report** — which elements are well-supported vs. provisional
- **Discovery Recommendations** — if confidence is low, what additional Discovery questions would strengthen the Brand DNA

---

## 8. Quality Checks

Before Brand DNA is finalised:

| Check | Question | Pass Criterion |
|-------|----------|----------------|
| **Sacrifice Test** | Does the positioning require forfeiting other slots? | Yes — real positioning requires sacrifice |
| **Three Tests** | Does differentiation pass Valued, Defensible, Aligned? | All three |
| **Configuration Test** | Is audience a configuration, not a bucket? | Yes — specific concerns/contexts/vocabularies |
| **Character Test** | Is personality a coherent person, not an adjective list? | Yes — believable, specific, distinctive |
| **Authenticity Test** | Does each element match observable brand behaviour? | Yes — no aspirational gaps |
| **Coherence Test** | Do all six elements reinforce each other? | Yes — no contradictions |
| **Archetype Honesty** | If no clean archetype, is that honestly stated? | Yes — no imposition |

Brand DNA that fails any check is returned for refinement — not released with gaps.

---

## 9. Failure Cases

| Failure | What Happens | Prevention |
|---------|--------------|------------|
| **Asserted Brand DNA** | The Strategy Engine outputs what the client claims rather than what investigation supports | Apply Authenticity Test to every element; surface gaps honestly |
| **Incoherent Brand DNA** | Elements contradict (e.g., "premium" positioning with "accessible" personality) | Coherence Test; surface contradictions; do not silently resolve |
| **Imposed Archetype** | Archetype assigned without behavioural authenticity | Honest "no clean archetype" is valid; never impose |
| **Bucket Audience** | Demographics without configuration | Configuration Test; reject vague audience definitions |
| **False Positioning** | Positioning that competitors could claim identically | Sacrifice Test; push back on table-stakes |
| **Skipping Discovery** | Strategy Engine runs on raw brief without Discovery processing | DR-1: Brand Confidence Score < 70% returns to Discovery |

---

## 10. Learning Opportunities

The Strategy Engine produces data that improves LMKC over time (with human approval per FD-007):

- **Patterns of positioning failure** — which positioning errors recur across projects?
- **Differentiation dimensions by category** — where does defensible differentiation typically live in different industries?
- **Archetype frequency** — which archetypes are common, which are rare, which are over-claimed?
- **Audience configuration patterns** — what configurations recur across categories?

These observations become *Proposed Knowledge Entries* — never auto-promoted to LMKC without human review.

---

## 11. Future Versions

| Version | Planned Enhancement |
|---------|---------------------|
| v1.1 | Adaptive positioning templates by category (B2B, consumer, service, luxury) |
| v1.2 | Archetype blend mapping — richer support for multi-archetype brands |
| v1.3 | Differentiation erosion tracking — flag when previously-defensible differentiation is declining |
| v2.0 | Direct integration with Discovery Workshop — real-time Brand DNA construction as discovery proceeds |

---

## Relationship to Other Engines

| Engine | Relationship |
|--------|-------------|
| **LOGOS Discover** (upstream) | Provides the raw inputs; Strategy Engine cannot proceed without Discovery output |
| **LOGOS Insight** (downstream) | Consumes Brand DNA to focus research on the right positioning, audience, and competitors |
| **LOGOS Create** (downstream) | Consumes Brand DNA to generate concepts that serve the strategic foundation |
| **LOGOS Judge** (downstream) | Evaluates concepts *against* Brand DNA — does each concept serve the strategy? |

The Strategy Engine is the **strategic pivot** of the entire pipeline — the moment raw understanding becomes structured strategy. Everything downstream depends on its quality.
