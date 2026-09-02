---
name: project-management
description: SE project management: WBS/schedule building, cost estimation, and measurement-program definition. Use for work breakdown and schedule, cost estimates, or defining SE measures and metrics.
---

# Project Management

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

Program controls for the SE effort; calls the compute library for EVM/cost math.

## Modes

| Mode | What it does |
|------|--------------|
| `wbs-schedule` | Build WBS and schedule. |
| `cost-estimate` | Build the cost estimate. |
| `measurement` | Define the measurement program (metrics/EVM). |

## Inputs

- scope / deliverables
- resource data
- cost basis

## Outputs

- wbs + schedule
- cost estimate
- measurement plan

## Quality gates

- WBS is complete and decomposed
- Estimates have a basis
- Metrics are actionable

## Notes

- **v2 provenance:** v2 PM-1..PM-3 (math via lib/)
- Each mode's full prompt/schema pair can live under this folder as it matures
  (e.g. `modes/<mode>.md`, `schemas/`, `examples/`) — progressive disclosure keeps
  `SKILL.md` lean while the detail loads on demand.
