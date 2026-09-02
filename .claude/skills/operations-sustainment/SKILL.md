---
name: operations-sustainment
description: Support operations and sustainment: transition-readiness review, sustainment plan building, and obsolescence/end-of-life planning. Use for transition readiness, sustainment planning, or obsolescence and EOL management.
---

# Operations Sustainment

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

Back-of-lifecycle operations and support.

## Modes

| Mode | What it does |
|------|--------------|
| `transition-readiness` | Review transition/deployment readiness. |
| `sustainment-plan` | Build the sustainment plan. |
| `obsolescence` | Plan obsolescence / end-of-life. |

## Inputs

- system baseline
- operations context
- supply/BOM data

## Outputs

- transition readiness report
- sustainment plan
- obsolescence plan

## Quality gates

- Readiness criteria explicit
- Sustainment resources identified
- EOL risks mitigated

## Notes

- **v2 provenance:** v2 OPS-1..OPS-3
- Each mode's full prompt/schema pair can live under this folder as it matures
  (e.g. `modes/<mode>.md`, `schemas/`, `examples/`) — progressive disclosure keeps
  `SKILL.md` lean while the detail loads on demand.
