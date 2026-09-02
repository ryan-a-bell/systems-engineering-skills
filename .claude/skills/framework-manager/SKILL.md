---
name: framework-manager
description: Create, select, and validate systems-engineering architecture/process frameworks (DoDAF, UAF, MODAF, TOGAF, or custom) defined as declarative manifests. Use when the user wants to define a new framework, choose which framework to operate in, or check whether an artifact set conforms to a framework's required viewpoints and gates.
---

# Framework Manager

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

Treat a framework as data: a manifest naming its viewpoints, required artifact types, phase gates, and traceability rules. Operating 'within' a framework then means validating the shared model against that manifest.

## Modes

| Mode | What it does |
|------|--------------|
| `create` | Author a new framework manifest (viewpoints, artifact types, gates, rules). |
| `select` | Choose an existing framework and load its manifest for the session. |
| `validate-conformance` | Check an artifact/model set against the selected framework's required views and completeness rules. |

## Inputs

- framework manifest (for select/validate)
- system model / artifact set
- target standard (DoDAF/UAF/custom)

## Outputs

- framework manifest
- conformance report
- gap list

## Quality gates

- Manifest is machine-readable and versioned
- Required viewpoints enumerated
- Conformance report cites the rule for every gap

## Wiring

- **Reads:** `frameworks/*.yaml` manifests (each validated against `frameworks/_schema.yaml`).
- **Writes:** `se-project.yaml` → `framework` and `diagram.default_notation` (taken from
  the manifest's `notation_defaults`).
- `create` authors a new `frameworks/<id>.yaml`; `select` loads one into state;
  `validate-conformance` compares the digital-thread model against the manifest's
  `required` viewpoints and reports gaps.
- Switching frameworks re-points state at a different manifest — the model is **not**
  rebuilt, only re-projected by `diagram-generation`.

## Notes

- **v2 provenance:** NEW in v3 (fills the framework gap)
- Each mode's full prompt/schema pair can live under this folder as it matures
  (e.g. `modes/<mode>.md`, `schemas/`, `examples/`) — progressive disclosure keeps
  `SKILL.md` lean while the detail loads on demand.
