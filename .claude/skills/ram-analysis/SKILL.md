---
name: ram-analysis
description: Reliability, availability, and maintainability analysis: reliability allocation/block modeling, FMEA/FMECA, fault-tree analysis, availability allocation, maintainability task analysis, and spares/LOR provisioning. Use for RAM modeling, FMEA, fault trees, or spares provisioning.
---

# Ram Analysis

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

The RAM/ilities capability; calls the compute library for reliability math.

## Modes

| Mode | What it does |
|------|--------------|
| `reliability-alloc` | Reliability allocation and block modeling. |
| `fmea` | FMEA/FMECA. |
| `fault-tree` | Fault-tree analysis. |
| `availability` | Availability allocation modeling. |
| `maintainability` | Maintainability task analysis. |
| `spares` | Level-of-repair / spares provisioning. |

## Inputs

- architecture model
- failure data
- usage profile

## Outputs

- reliability model
- fmea table
- fault tree
- availability model
- spares plan

## Quality gates

- Allocations sum correctly
- Failure modes traced to effects
- Provisioning meets targets

## Notes

- **v2 provenance:** v2 RAM-1..RAM-6 (math via lib/)
- Each mode's full prompt/schema pair can live under this folder as it matures
  (e.g. `modes/<mode>.md`, `schemas/`, `examples/`) — progressive disclosure keeps
  `SKILL.md` lean while the detail loads on demand.
