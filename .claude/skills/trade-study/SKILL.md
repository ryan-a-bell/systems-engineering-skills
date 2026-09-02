---
name: trade-study
description: Run a decision/trade study: frame the decision and objectives, weight criteria, generate and screen alternatives, run the decision matrix, and produce a recommendation and decision record. Use for trade studies, criteria weighting, alternative analysis, or decision documentation.
---

# Trade Study

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

Structured decision analysis with an auditable record.

## Modes

| Mode | What it does |
|------|--------------|
| `frame` | Frame the decision and objectives. |
| `weight-criteria` | Facilitate criteria weighting. |
| `generate-screen` | Generate and screen alternatives. |
| `decision-matrix` | Run the weighted decision matrix. |
| `record` | Produce the recommendation / decision record. |

## Inputs

- decision statement
- criteria
- alternatives

## Outputs

- decision matrix
- decision record
- trade study report

## Quality gates

- Criteria are independent and weighted
- Alternatives comparable
- Recommendation traces to scores

## Notes

- **v2 provenance:** v2 TS-1..TS-5
- Each mode's full prompt/schema pair can live under this folder as it matures
  (e.g. `modes/<mode>.md`, `schemas/`, `examples/`) — progressive disclosure keeps
  `SKILL.md` lean while the detail loads on demand.
