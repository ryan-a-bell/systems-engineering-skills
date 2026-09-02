---
name: human-system-integration
description: Human-system integration: operator task analysis, human error-mode assessment, and UI/interface requirements. Use for task analysis, human-error analysis, or deriving human-machine interface requirements.
---

# Human System Integration

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

The human in the loop: tasks, errors, and interface needs.

## Modes

| Mode | What it does |
|------|--------------|
| `task-analysis` | Analyze operator tasks. |
| `error-mode` | Assess human error modes. |
| `ui-requirements` | Derive UI/interface requirements. |

## Inputs

- operational scenarios
- operator roles
- interface concepts

## Outputs

- task analysis
- error-mode assessment
- ui requirements

## Quality gates

- Tasks tie to operational threads
- Error modes have mitigations
- UI requirements verifiable

## Notes

- **v2 provenance:** v2 HSI-1..HSI-3
- Each mode's full prompt/schema pair can live under this folder as it matures
  (e.g. `modes/<mode>.md`, `schemas/`, `examples/`) — progressive disclosure keeps
  `SKILL.md` lean while the detail loads on demand.
