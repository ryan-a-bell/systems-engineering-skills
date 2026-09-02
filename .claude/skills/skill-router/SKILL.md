---
name: skill-router
description: Route a user intent or artifact to the correct SE capability skill and mode. Use when it is unclear which skill applies, or to triage an incoming request or artifact across the taxonomy.
---

# Skill Router

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

The dispatcher for the taxonomy. Maps free-form intent or an artifact type to one capability skill plus the mode within it.

## Modes

| Mode | What it does |
|------|--------------|
| `route-intent` | Map a natural-language request to a skill + mode. |
| `triage-artifact` | Classify an incoming artifact and suggest the next skill/mode. |

## Inputs

- user intent or artifact
- skills registry

## Outputs

- chosen skill + mode
- rationale

## Quality gates

- Single unambiguous target returned
- Falls back to a clarifying question when confidence is low

## Wiring

- **Reads:** `se-project.yaml` (active context) and each skill's `description`
  frontmatter.
- Dispatches an intent to exactly one capability skill + mode; falls back to a
  clarifying question when confidence is low.

## Notes

- **v2 provenance:** v2 META-1
- Each mode's full prompt/schema pair can live under this folder as it matures
  (e.g. `modes/<mode>.md`, `schemas/`, `examples/`) — progressive disclosure keeps
  `SKILL.md` lean while the detail loads on demand.
