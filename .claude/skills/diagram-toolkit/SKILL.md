---
name: diagram-toolkit
description: Validate, convert, and orchestrate diagrams: syntax validation with line-level errors, cross-notation conversion, and architecture-to-diagram-set orchestration with render-and-verify. Use to check diagram syntax, convert between notations, or auto-generate a coordinated diagram package.
---

# Diagram Toolkit

## Session context (read first)

Before acting, read `se-project.yaml` at the project root for the active
**framework**, **lifecycle**, **phase**, and **diagram.default_notation**, plus the
current shared **model (IR) + trace links**. Operate within that context and write
any artifacts you produce back into the digital thread (`se-project.yaml`). If it is
missing, ask the user to run `/framework-manager select <framework>` (or offer to
create one from `se-project.example.yaml`) before proceeding.

If a `framework` or `lifecycle` is set, also read its manifest (`frameworks/<framework>.yaml` / `lifecycles/<lifecycle>.yaml`) for the viewpoints/phases and their descriptions **before** producing framework-specific artifacts — see the repo `CLAUDE.md` for the full sequence.

**Layer:** diagramming

## Purpose

The cross-cutting diagram services. Orchestrate mode drives diagram-generation across intents and then renders and visually verifies the output.

## Modes

| Mode | What it does |
|------|--------------|
| `validate` | Syntax validation with precise line-level errors and optional auto-fix. |
| `convert` | Convert a diagram between notations. |
| `orchestrate` | Select intents for a model, generate the set, render, and verify. |

## Inputs

- diagram source or architecture model
- target notation (convert)

## Outputs

- validation result
- converted diagram
- diagram package + index

## Quality gates

- Errors cite line numbers
- Conversion preserves semantics
- Rendered output checked for overlaps/clipping

## Wiring

- **Reads:** `registry/diagram-backends.yaml` to select a backend per (intent × notation)
  — the built-in `diagram-generation`, an external skill such as `drawio-skill`, or an
  MCP tool. All backends consume the same shared model, so they are interchangeable.
- `orchestrate` picks the intents for a model, generates the set, renders, and visually
  verifies (overlaps, clipping, stacked edges); `validate` checks syntax with line-level
  errors; `convert` maps a diagram between notations.

## Notes

- **v2 provenance:** v2 DIAG-X1..DIAG-X3 (adds render-and-verify)
- Each mode's full prompt/schema pair can live under this folder as it matures
  (e.g. `modes/<mode>.md`, `schemas/`, `examples/`) — progressive disclosure keeps
  `SKILL.md` lean while the detail loads on demand.
