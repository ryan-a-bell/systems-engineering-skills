---
name: config-management
description: Perform configuration management: CM planning and CI identification/baselines, change control with cross-artifact impact, status accounting and baseline comparison, audit support (FCA/PCA), and release readiness and notes. Use for CM planning, change control, baselines, audits, or releases.
---

# Config Management

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

Configuration control across the digital thread.

## Modes

| Mode | What it does |
|------|--------------|
| `plan-ci` | CM plan, CI identification, baseline definition. |
| `change-control` | Change control with cross-artifact impact. |
| `status-accounting` | Status accounting and baseline comparison. |
| `audit` | Audit support: FCA/PCA closure tracking. |
| `release` | Release readiness and release notes. |

## Inputs

- artifact set
- baselines
- change requests

## Outputs

- cm plan
- ci list
- baseline snapshot
- change-impact report
- release notes

## Quality gates

- CIs uniquely identified
- Baselines immutable
- Changes traced end to end

## Notes

- **v2 provenance:** v2 CM-1..CM-5
- Each mode's full prompt/schema pair can live under this folder as it matures
  (e.g. `modes/<mode>.md`, `schemas/`, `examples/`) — progressive disclosure keeps
  `SKILL.md` lean while the detail loads on demand.
