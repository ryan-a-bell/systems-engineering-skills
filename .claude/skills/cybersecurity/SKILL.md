---
name: cybersecurity
description: Model system cybersecurity: STRIDE threat modeling and security-controls allocation. Use for threat model construction or allocating and tracing security controls to the architecture.
---

# Cybersecurity

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

Security engineering integrated with the architecture model.

## Modes

| Mode | What it does |
|------|--------------|
| `threat-model` | Build a STRIDE threat model. |
| `controls-allocation` | Allocate and trace security controls. |

## Inputs

- architecture model
- assets / data flows
- control catalog

## Outputs

- threat model
- controls allocation matrix

## Quality gates

- Threats cover STRIDE categories
- Controls trace to threats and assets

## Notes

- **v2 provenance:** v2 CYB-1..CYB-2
- Each mode's full prompt/schema pair can live under this folder as it matures
  (e.g. `modes/<mode>.md`, `schemas/`, `examples/`) — progressive disclosure keeps
  `SKILL.md` lean while the detail loads on demand.
