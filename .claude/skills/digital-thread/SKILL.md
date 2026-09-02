---
name: digital-thread
description: Maintain the shared semantic model (IR) and traceability links connecting requirements, functions, components, and verification across all skills. Use when the user wants to record, query, or visualize trace links, or check coverage and change-impact across artifacts.
---

# Digital Thread

## Session context (read first)

Before acting, read `se-project.yaml` at the project root for the active
**framework**, **lifecycle**, **phase**, and **diagram.default_notation**, plus the
current shared **model (IR) + trace links**. Operate within that context and write
any artifacts you produce back into the digital thread (`se-project.yaml`). If it is
missing, ask the user to run `/framework-manager select <framework>` (or offer to
create one from `se-project.example.yaml`) before proceeding.

If a `framework` or `lifecycle` is set, also read its manifest (`frameworks/<framework>.yaml` / `lifecycles/<lifecycle>.yaml`) for the viewpoints/phases and their descriptions **before** producing framework-specific artifacts — see the repo `CLAUDE.md` for the full sequence.

**Layer:** meta

## Purpose

The single source of truth every other skill reads and writes. Owns trace edges so coverage and impact are computed centrally, not re-derived per skill.

## Modes

| Mode | What it does |
|------|--------------|
| `record-links` | Add/update trace edges between model elements. |
| `query-trace` | Retrieve trace chains for an element. |
| `coverage` | Report requirement/verification coverage gaps. |
| `impact` | Compute change-impact across the thread. |

## Inputs

- model elements
- existing trace links
- changed element (for impact)

## Outputs

- updated trace graph
- coverage report
- impact set

## Quality gates

- Links are typed and bidirectional
- Orphans/gaps flagged
- Impact set is complete and minimal

## Wiring

- **Owns:** the `model` (elements/relations) and `trace.links` sections of `se-project.yaml`.
- Every capability skill writes its artifacts and trace edges here; `diagram-generation`
  reads the model from here to render views.
- `coverage` and `impact` are computed centrally over the trace graph, so no skill
  re-derives traceability on its own.

## Notes

- **v2 provenance:** v2 RE-4 trace logic, promoted to a shared service
- Each mode's full prompt/schema pair can live under this folder as it matures
  (e.g. `modes/<mode>.md`, `schemas/`, `examples/`) — progressive disclosure keeps
  `SKILL.md` lean while the detail loads on demand.
