---
name: mbse-modeling
description: Build and manage model-based systems engineering artifacts: modeling scope/viewpoint planning, architecture and behavior/function models, requirements-model linking and coverage auditing, model QA, reporting, and parametric/simulation orchestration. Use for MBSE model creation, checking, or reporting.
---

# Mbse Modeling

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

The MBSE workbench. Produces and audits the architecture model that diagram-generation later renders.

## Modes

| Mode | What it does |
|------|--------------|
| `scope-viewpoint` | Plan modeling scope and viewpoints. |
| `architecture` | Generate the architecture (structure) model. |
| `behavior` | Generate behavior/function models. |
| `req-link-coverage` | Link requirements to model and audit coverage. |
| `qa` | Model QA and consistency checking. |
| `reporting` | Generate model reports/artifacts. |
| `parametric` | Orchestrate parametric analysis / simulation. |

## Inputs

- modeling plan
- requirements set
- architecture/behavior model

## Outputs

- architecture model
- behavior model
- model quality report

## Quality gates

- Model consistent and well-formed
- Requirements coverage audited
- Viewpoints satisfied

## Notes

- **v2 provenance:** v2 MBSE-1..MBSE-7
- Each mode's full prompt/schema pair can live under this folder as it matures
  (e.g. `modes/<mode>.md`, `schemas/`, `examples/`) — progressive disclosure keeps
  `SKILL.md` lean while the detail loads on demand.
