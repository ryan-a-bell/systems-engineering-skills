---
name: requirements-engineering
description: Elicit, write, normalize, structure, allocate, and trace requirements to INCOSE quality standards. Use for requirement generation from descriptions, the 20-questions elicitation game, quality/ambiguity checks, requirement structuring and allocation, traceability building, or change-impact analysis.
---

# Requirements Engineering

## Session context (read first)

Before acting, read `se-project.yaml` at the project root for the active
**framework**, **lifecycle**, **phase**, and **diagram.default_notation**, plus the
current shared **model (IR) + trace links**. Operate within that context and write
any artifacts you produce back into the digital thread (`se-project.yaml`). If it is
missing, ask the user to run `/framework-manager select <framework>` (or offer to
create one from `se-project.example.yaml`) before proceeding.

If a `framework` or `lifecycle` is set, also read its manifest (`frameworks/<framework>.yaml` / `lifecycles/<lifecycle>.yaml`) for the viewpoints/phases and their descriptions **before** producing framework-specific artifacts — see the repo `CLAUDE.md` for the full sequence.

**Layer:** core

## Purpose

The full requirements capability. Each mode is one contract; they share the requirement artifact schema.

## Modes

| Mode | What it does |
|------|--------------|
| `elicit` | Build elicitation context and draft requirements from stakeholder inputs. |
| `twenty-questions` | Interactive 20-questions requirements elicitor across 4 rounds / 7 dimensions. |
| `normalize` | Check and rewrite requirements for INCOSE quality (necessary, singular, verifiable...). |
| `structure-allocate` | Structure the requirement hierarchy and allocate to elements. |
| `trace` | Build requirement-to-model / requirement-to-test trace links. |
| `change-impact` | Assess baseline change impact across requirements. |

## Inputs

- stakeholder notes
- system description
- requirements set / baseline

## Outputs

- requirements set
- quality report
- trace links
- change-impact report

## Quality gates

- Every requirement is singular, verifiable, unambiguous
- Traceable to a source
- Allocation complete

## Notes

- **v2 provenance:** v2 RE-1..RE-6
- Each mode's full prompt/schema pair can live under this folder as it matures
  (e.g. `modes/<mode>.md`, `schemas/`, `examples/`) — progressive disclosure keeps
  `SKILL.md` lean while the detail loads on demand.
