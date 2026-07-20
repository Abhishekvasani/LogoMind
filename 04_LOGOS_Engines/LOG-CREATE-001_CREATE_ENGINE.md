---
doc_id: LOG-CREATE-001
title: LOGOS Create Engine (Concept Families) v1.0
version: 1.0
status: Approved
governance_level: L2 — Engine Specification
engine_blueprint: CTO Decision #003
last_reviewed: 2026-07-17
related:
  - LOG-STRAT-001 Strategy Engine (upstream — provides Brand DNA)
  - LOG-INSIGHT-001 Insight Engine (upstream — provides research context)
  - LOG-JUDGE-001 Judge Engine (downstream — evaluates Create output)
  - RS-LIC-PH-005 Originality (knowledge source)
conformance: "This engine conforms to LM-STD-001 through LM-STD-006 and the Engine Blueprint Standard."
---

# LOG-CREATE-001 — Create Engine (Concept Families)

> *The Create Engine is where strategy becomes creative direction. It does not generate logos — it generates **Concept Families**: strategic territories the designer chooses between before any sketching begins. This is LogoMind's signature feature.*

---

## 1. Mission

Transform Brand DNA + Insight context into **3–5 Concept Families** — strategic creative directions, each with its own theme, candidate symbols, visual language, and rationale. The designer then chooses a territory to develop, rather than choosing between isolated ideas.

---

## 2. Purpose in the Pipeline

```
LOGOS Strategy  →  LOGOS Insight  →  LOGOS Create  →  LOGOS Judge
(Brand DNA)         (research)         (Concept        (evaluation)
                                       Families)
                                          ▲
                                          │
                                 THE CREATE ENGINE
                                 outputs strategic
                                 creative territories
```

The Create Engine occupies the creative pivot of the pipeline — the moment strategy becomes creative direction. Its output is not finished concepts; it is *directions* that frame the designer's sketching work.

---

## 3. The Signature Principle: Concept Families, Not Isolated Ideas

> Most AI tools generate isolated logo ideas: "here are 20 logos."
>
> LogoMind generates **Concept Families**: "here are 4 strategic directions. Choose one and I'll develop it further."

This mirrors how experienced branding agencies work — they explore *territories* before refining concepts. A Concept Family is a strategic territory with multiple supporting ideas, not a single idea.

### Example: Eco-Friendly Tech Company

Instead of:
```
Concept 1: leaf icon
Concept 2: circuit icon
Concept 3: tree icon
...
```

The Create Engine produces:
```
Family A — Nature
   Theme: organic growth
   Symbols: leaf, seed, growth rings, branching systems
   Visual language: organic curves, natural asymmetry

Family B — Technology
   Theme: connected systems
   Symbols: circuits, networks, data flow, nodes
   Visual language: precise geometry, structured grids

Family C — Fusion
   Theme: nature + technology integrated
   Symbols: leaf + circuit, tree + hexagon, seed + pixel
   Visual language: hybrid forms, tension between organic and geometric

Family D — Abstract
   Theme: balance, flow, renewal
   Symbols: spiral, cycle, equilibrium, pulse
   Visual language: pure abstraction, no literal referent
```

The designer chooses a *direction* — not just an *idea*.

---

## 4. Inputs

### Required Data
- Brand DNA (from Strategy Engine) — purpose, positioning, differentiation, audience, personality, archetype
- Insight context (from Insight Engine) — industry clichés, competitor visual language, category opportunities

### Optional Data
- Client symbol preferences (from Discovery)
- Symbols to avoid (from Discovery)
- Cultural/regional considerations

### Knowledge Sources
- **RS-LIC-PH-001 Meaning** — concepts must express the brand's meaning
- **RS-LIC-PH-002 Purpose** — concepts must serve the brand's purpose
- **RS-LIC-PH-005 Originality** — provides the Combination Method for generating original concepts
- **LMKC Symbol Intelligence** (future volume) — the library of symbols, meanings, cultural considerations
- **LMKC Industry Intelligence** (future volume) — category-specific symbol conventions and clichés

---

## 5. Reasoning Steps

```
Step 1: EXTRACT MEANING ANCHORS
   → From Brand DNA, identify the 2-3 core meanings the identity must express
   → Example: "trust" + "precision" + "innovation"
   → These become the creative targets every Concept Family must serve

Step 2: GENERATE SYMBOL CANDIDATES (per meaning anchor)
   → For each meaning, generate symbol candidates from multiple domains:
     ├── Direct symbols (literal — usually to be avoided or used carefully)
     ├── Abstract symbols (geometric, conceptual)
     ├── Natural forms (organic, biological)
     ├── Scientific/mathematical concepts
     ├── Architectural forms
     ├── Cultural/historical references
     └── Negative-space opportunities
   → Apply the Cross-Pollination Principle (RS-LIC-PH-005 §4):
     reach past the obvious domain into adjacent ones

Step 3: APPLY THE COMBINATION METHOD
   → Use structured combination (RS-LIC-PH-005) to generate original directions
   → Pair symbols from different domains
   → Test each combination against the 5 Originality Tests:
     Meaning, Distinctiveness, Clarity, Inevitability, Non-Arbitrary
   → Discard combinations that fail any test

Step 4: ELIMINATE CLICHÉS
   → Consult Insight Engine's cliché list for the category
   → Remove or actively avoid exhausted symbols
   → Flag: "This symbol is overused in this industry. Consider alternatives."

Step 5: GENERATE HIDDEN METAPHOR CANDIDATES
   → For each meaning anchor, ask: "What represents [meaning]
     without literally showing [meaning]?"
   → Example: "trust" → bridge, keystone, anchor, orbit, pulse
     (none literally show "trust" — all carry it metaphorically)

Step 6: CLUSTER INTO CONCEPT FAMILIES
   → Group surviving symbols/metaphors by thematic affinity
   → Aim for 3-5 distinct families, each with a clear theme
   → Ensure families are genuinely distinct (not variations of one idea)
   → Each family should offer a different strategic angle on the meaning

Step 7: DEVELOP EACH FAMILY
   → For each Concept Family, specify:
     ├── Theme (one phrase capturing the family's strategic angle)
     ├── Core symbols (3-7 symbols that belong to this territory)
     ├── Visual language (forms, geometry, treatment hints)
     ├── Why it works (trace to Brand DNA — which meaning does it serve?)
     ├── Potential pitfalls (what could go wrong in execution?)
     └── Originality assessment (how distinctive for this purpose?)

Step 8: SCORE AND RANK FAMILIES
   → Apply a preliminary Creative Council assessment (9 minds, LOG-CC-001)
   → Rank families by strategic fit + originality + clarity
   → Surface the strongest 2-3 families prominently; include 1-2 alternatives

Step 9: PREPARE FOR JUDGE ENGINE
   → Package the Concept Families for the Judge Engine's full evaluation
   → Include the reasoning trail: why each family was generated, what it
     serves, what risks it carries
```

---

## 6. Decision Rules

| Rule | Condition | Action |
|------|-----------|--------|
| **DR-1** | Brand DNA confidence < C3 | Return to Strategy Engine — creative work is premature |
| **DR-2** | Fewer than 3 viable Concept Families | Surface the creative constraint; consult broader symbol domains |
| **DR-3** | All families rely on category clichés | Flag: the category may be visually exhausted; recommend abstraction or category-breaking approach |
| **DR-4** | A family fails the Meaning Test | Discard — originality without meaning is novelty, not originality |
| **DR-5** | Client-requested symbol is a cliché | Apply Creative Director Mode: respectfully challenge the request (see §9) |
| **DR-6** | A combination is novel but arbitrary | Discard — the Non-Arbitrary Test catches forced combinations |

---

## 7. Confidence Calculation

Each Concept Family carries a confidence score:

| Factor | Weight |
|--------|--------|
| Meaning alignment (does it serve Brand DNA?) | 30% |
| Distinctiveness (is it unusual for this category?) | 25% |
| Clarity (will a cold viewer read it?) | 20% |
| Executable (can it actually be drawn effectively?) | 15% |
| Original (combinatorial, not novel-for-novelty) | 10% |

Families scoring < C3 are flagged as *exploratory* — interesting but risky. Families scoring C4+ are *recommended*. The designer always makes the final choice.

---

## 8. Outputs

### Primary Output: Concept Families Document

```yaml
concept_families:
  project: <project name>
  brand_dna_reference: <link to Brand DNA document>

  family_A:
    theme: "<one-phrase strategic angle>"
    core_meaning_served: "<which Brand DNA meaning>"
    symbols:
      - name: <symbol>
        meaning: <what it carries>
        originality: <C-level + reasoning>
        abstraction_level: <literal / abstract / metaphorical>
        risk_level: <low / medium / high>
        possible_combinations: <with what other symbols?>
    visual_language:
      forms: <geometry, curves, angles>
      treatment: <minimal, detailed, textured>
      composition: <symmetric, asymmetric, dynamic>
    why_it_works: "<reasoning trace to Brand DNA>"
    pitfalls: "<what could go wrong>"
    creative_council_assessment: <9-mind summary>
    confidence: <C-level>
    recommendation_strength: <recommended / alternative / exploratory>

  family_B: { ... }
  family_C: { ... }

cliches_avoided:
  - <symbol>: <why avoided for this category>

client_request_notes:
  - <any client-requested symbols and how they were handled>

metadata:
  total_families: <count>
  recommended: <strongest family IDs>
  source: <Brand DNA + Insight + LMKC>
```

### Secondary Outputs
- **Cliché Avoidance Report** — what symbols were considered and rejected, with reasons
- **Client Request Handling** — how client symbol preferences were respected or respectfully challenged

---

## 9. Creative Director Mode

The Create Engine implements **Creative Director Mode** (per the Founder's Charter, FD-010, and AI Design Principle 4):

When a client requests a symbol that is overused or strategically weak, the Create Engine does not silently comply. It respectfully challenges:

> *"The client requested a lion, but the industry already overuses lions. Consider expressing leadership through a crown-inspired geometry, a bold monogram, or a rising-horizon abstract form. Each carries the same meaning (leadership) with greater originality."*

This is one of LogoMind's signature behaviours — challenging weak client requests to serve the client better. The challenge is always respectful and always offers alternatives.

---

## 10. Quality Checks

| Check | Question | Pass Criterion |
|-------|----------|----------------|
| **Family Count** | Are there 3–5 genuinely distinct families? | Yes — fewer suggests creative constraint; more suggests dilution |
| **Meaning Test** | Does each family serve a Brand DNA meaning? | Yes — traceable to purpose/positioning |
| **Cliché Avoidance** | Have category clichés been identified and avoided? | Yes — cliché list consulted |
| **Originality Tests** | Does each family pass the 5 Originality Tests? | Yes — Meaning, Distinctiveness, Clarity, Inevitability, Non-Arbitrary |
| **Strategic Diversity** | Do the families offer genuinely different strategic angles? | Yes — not variations of one idea |
| **Reasoning Trail** | Can each family's inclusion be defended? | Yes — traceable to Brand DNA + LMKC |

---

## 11. Failure Cases

| Failure | What Happens | Prevention |
|---------|--------------|------------|
| **Isolated Ideas** | Engine outputs flat list of ideas instead of Concept Families | Enforce the Family structure (theme + supporting symbols + visual language) |
| **Cliché Compliance** | Engine includes overused symbols without challenge | Cliché list consultation; Creative Director Mode |
| **Novelty Chase** | Engine produces novel-but-meaningless combinations | Apply Meaning Test and Non-Arbitrary Test; discard failures |
| **Single-Family Bias** | All "families" are variations of one idea | Strategic Diversity check; ensure genuinely different angles |
| **Client Sycophancy** | Engine includes weak client-requested symbols without challenge | Creative Director Mode; always offer better alternatives |
| **Skipping Originality Tests** | Combinations presented without testing | All 5 Originality Tests must pass before inclusion |

---

## 12. Learning Opportunities

- **Category cliché maps** — which symbols are overused in which industries? (Builds LMKC Symbol Intelligence)
- **Combinatorial patterns** — which symbol combinations produce strong concepts across projects?
- **Family diversity patterns** — how many genuinely distinct families typically emerge per category?
- **Creative Director challenge effectiveness** — which client challenges produce better outcomes?

---

## 13. Future Versions

| Version | Enhancement |
|--------|-------------|
| v1.1 | Symbol Intelligence volume integration — richer symbol library |
| v1.2 | Cultural adaptation — adjust families for regional audiences |
| v1.3 | Motion identity families — extend Concept Families to animated contexts |
| v2.0 | Co-creative mode — designer sketches; engine develops the sketch's family |

---

## Relationship to Other Engines

| Engine | Relationship |
|--------|-------------|
| **LOGOS Strategy** (upstream) | Provides Brand DNA — the creative target |
| **LOGOS Insight** (upstream) | Provides cliché awareness and competitor context |
| **LOGOS Judge** (downstream) | Evaluates the Concept Families — which survives scrutiny? |
| **LOGOS Coach** (downstream) | Helps the designer sketch within the chosen family |
| **Creative Council** (LOG-CC-001) | Provides the 9-mind assessment during Step 8 |

---

## The "Why?" Loop

For every recommended Concept Family, the Create Engine applies the "Why?" Loop:

- Why this family?
- Why not another?
- Is it overused in this category?
- Can it be made more abstract?
- Can it tell two stories at once?
- Can it be simplified?
- Will it still work at favicon size?
- Would a design jury find it distinctive?

Only families that survive the "Why?" Loop are included in the output.
