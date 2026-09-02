---
name: mission-analysis
description: Analyze mission and operational needs: generate a ConOps, define measures of effectiveness/performance (MOE/MOP), and identify capability gaps. Use for concept-of-operations drafting, MOE/MOP definition, or capability gap analysis.
---

# Mission Analysis

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

Front-of-lifecycle mission framing that feeds requirements and architecture.

## Modes

| Mode | What it does |
|------|--------------|
| `conops` | Generate a concept of operations from mission intent. |
| `moe-mop` | Define measures of effectiveness and performance. |
| `capability-gap` | Identify capability gaps against needs. |

## Inputs

- mission statement
- stakeholder needs
- operational context

## Outputs

- conops
- moe/mop set
- capability gap analysis

## Quality gates

- MOEs tie to mission outcomes
- MOPs are measurable
- Gaps trace to needs

## Notes

- **v2 provenance:** v2 MA-1..MA-3
- Each mode's full prompt/schema pair can live under this folder as it matures
  (e.g. `modes/<mode>.md`, `schemas/`, `examples/`) — progressive disclosure keeps
  `SKILL.md` lean while the detail loads on demand.
