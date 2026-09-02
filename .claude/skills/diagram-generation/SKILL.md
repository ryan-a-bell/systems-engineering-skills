---
name: diagram-generation
description: Generate diagrams from the shared architecture model in any supported notation. Use whenever a diagram is requested - context, structure (BDD/IBD/component/class), behavior (sequence/activity/state), requirements, C4, deployment, or trace maps - rendered to Mermaid, PlantUML, SysML v1, SysML v2, Excalidraw, or HTML. Notation and intent are parameters, not separate skills.
---

# Diagram Generation

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

One skill over a shared IR, replacing v2's 34 notation-times-type skills. Pick an INTENT (what to show) and a NOTATION (how to render); a capability matrix handles notations that cannot express a given intent, with graceful fallback.

## Parameters

| Axis | Values |
|------|--------|
| `intent` | context | structure | behavior | requirements | c4 | deployment | trace-map |
| `notation` | mermaid | plantuml | sysmlv1 | sysmlv2 | excalidraw | html |

## Inputs

- architecture/behavior model (IR)
- intent
- notation
- optional style

## Outputs

- diagram source (in chosen notation)
- diagram metadata

## Quality gates

- Intent expressible in notation (or degrades explicitly)
- Consistent naming with model
- Syntax validates (via diagram-toolkit)

## Wiring

- **Reads:** the shared model (IR) from the digital thread (`se-project.yaml`); the
  active framework manifest in `frameworks/` (to map a requested view onto its
  viewpoints); and, via `diagram-toolkit`, the capability matrix in
  `registry/diagram-backends.yaml`.
- **Parameters:** `intent` (context | structure | behavior | requirements | c4 |
  deployment | trace-map) and `notation` (defaults to `diagram.default_notation`).
  The active framework supplies the viewpoint vocabulary — e.g. selecting the `c4`
  framework yields Context/Container/Component views.
- If the chosen notation cannot express the intent, degrade per the registry
  `fallback` rule and state that explicitly.

## Notes

- **v2 provenance:** v2 PUML-*, SYSML1-*, SYSML2-*, MERM-*, EXCL-* (34 -> 1)
- Each mode's full prompt/schema pair can live under this folder as it matures
  (e.g. `modes/<mode>.md`, `schemas/`, `examples/`) — progressive disclosure keeps
  `SKILL.md` lean while the detail loads on demand.
