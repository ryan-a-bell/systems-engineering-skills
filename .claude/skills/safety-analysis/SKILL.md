---
name: safety-analysis
description: Perform system safety analysis: hazard analysis (PHA/SSHA) and safety-case (GSN) construction. Use for hazard identification, preliminary or subsystem hazard analysis, or building a goal-structured safety case.
---

# Safety Analysis

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

Safety engineering: from hazards to an argued safety case.

## Modes

| Mode | What it does |
|------|--------------|
| `hazard` | Preliminary/subsystem hazard analysis (PHA/SSHA). |
| `safety-case` | Build a goal-structured (GSN) safety case. |

## Inputs

- system description
- hazard list
- safety requirements

## Outputs

- hazard analysis
- safety case (GSN)

## Quality gates

- Hazards traced to causes and controls
- Safety claims supported by evidence

## Notes

- **v2 provenance:** v2 SAF-1..SAF-2
- Each mode's full prompt/schema pair can live under this folder as it matures
  (e.g. `modes/<mode>.md`, `schemas/`, `examples/`) — progressive disclosure keeps
  `SKILL.md` lean while the detail loads on demand.
