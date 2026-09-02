---
name: verification-validation
description: Plan and design V&V: build a V&V strategy, map verification methods and design tests, sequence integration/system tests, build validation/UAT scenarios, and package evidence. Use for verification planning, test design, integration sequencing, or evidence assembly.
---

# Verification Validation

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

Right side of the Vee. Turns requirements into a defensible evidence chain.

## Modes

| Mode | What it does |
|------|--------------|
| `strategy` | Build the V&V strategy and plan. |
| `verify-map` | Map verification methods and design test cases. |
| `integration-sequence` | Sequence integration and system tests. |
| `validation-uat` | Build validation / user-acceptance scenarios. |
| `evidence` | Package evidence and reporting. |

## Inputs

- requirements baseline
- architecture model
- test results

## Outputs

- v&v plan
- verification matrix
- test cases
- evidence index

## Quality gates

- Every requirement has a verification method
- Traceable evidence
- Integration order respects dependencies

## Notes

- **v2 provenance:** v2 VV-1..VV-5
- Each mode's full prompt/schema pair can live under this folder as it matures
  (e.g. `modes/<mode>.md`, `schemas/`, `examples/`) — progressive disclosure keeps
  `SKILL.md` lean while the detail loads on demand.
