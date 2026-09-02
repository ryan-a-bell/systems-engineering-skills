---
name: risk-management
description: Manage program and technical risk: set up the risk program, identify and populate a risk register, score and analyze coupling, build mitigation/contingency plans, and monitor and report trends. Use for risk identification, scoring, mitigation planning, or risk reporting.
---

# Risk Management

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

Closed-loop risk process over a shared register.

## Modes

| Mode | What it does |
|------|--------------|
| `setup` | Set up the risk program and scales. |
| `identify` | Identify risks and populate the register. |
| `score-couple` | Score risks and analyze coupling. |
| `mitigate` | Build mitigation/contingency plans. |
| `monitor` | Monitor trends, report, and escalate. |

## Inputs

- risk program config
- risk register
- project context

## Outputs

- risk register
- risk analysis report
- mitigation plan
- status report

## Quality gates

- Consistent scoring scale
- Each risk has an owner and handling
- Trends tracked over time

## Notes

- **v2 provenance:** v2 RISK-1..RISK-5
- Each mode's full prompt/schema pair can live under this folder as it matures
  (e.g. `modes/<mode>.md`, `schemas/`, `examples/`) — progressive disclosure keeps
  `SKILL.md` lean while the detail loads on demand.
