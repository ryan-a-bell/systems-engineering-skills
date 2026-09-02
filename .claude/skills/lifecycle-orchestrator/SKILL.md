---
name: lifecycle-orchestrator
description: Guide a stateful walkthrough of a system lifecycle (vee, spiral, agile-hybrid, waterfall, incremental, sustainment) after a framework is selected, tracking phases, gates, and which artifacts are done vs pending. Use when the user asks to step through a lifecycle, run a phase gate, or see where they are in the process.
---

# Lifecycle Orchestrator

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

A guided, resumable process engine. Holds session state (current phase, gate status, produced artifacts) and hands off to the right capability skill at each step.

## Modes

| Mode | What it does |
|------|--------------|
| `select-model` | Pick the lifecycle model (vee, spiral, agile-hybrid, waterfall, incremental, sustainment). |
| `advance-phase` | Move to the next phase and surface the artifacts/skills it expects. |
| `gate-review` | Run a phase-gate check against entry/exit criteria. |
| `status` | Report current phase, completed vs pending artifacts, and open gates. |

## Inputs

- selected framework
- session state / digital thread
- lifecycle model choice

## Outputs

- updated session state
- phase plan
- gate-review result

## Quality gates

- State is persisted and resumable
- Each phase lists expected artifacts
- Gate criteria evaluated explicitly

## Wiring

- **Reads:** `se-project.yaml` (`framework`, current `phase`) and the lifecycle model
  definitions.
- **Writes:** `se-project.yaml` → `lifecycle`, `phase`, and `gates` status.
- Holds the resumable walkthrough state and hands each phase's work to the appropriate
  capability skill (via `skill-router`).

## Notes

- **v2 provenance:** v2 lifecycle_orchestrators/ (as data-driven state, not templates)
- Each mode's full prompt/schema pair can live under this folder as it matures
  (e.g. `modes/<mode>.md`, `schemas/`, `examples/`) — progressive disclosure keeps
  `SKILL.md` lean while the detail loads on demand.
