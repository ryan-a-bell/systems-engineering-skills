# Systems Engineering Skills — working guidance

This repo is an agent framework for systems engineering. Active state lives in
`se-project.yaml`; the framework and lifecycle **definitions** live on disk under
`frameworks/` and `lifecycles/`. `se-project.yaml` only holds *pointers* (which
framework, which lifecycle) — the detail is read on demand.

## Always: load the active framework before framework-specific work

Before producing any framework-specific artifact — a diagram, viewpoint, model, or
conformance check — follow this sequence:

1. **Read `se-project.yaml`** at the project root. Note `framework`, `lifecycle`,
   `phase`, and `diagram.default_notation`.
2. **If `framework` is set, read its manifest `frameworks/<framework>.yaml`** to load
   that framework's viewpoints — their ids, names, descriptions, and the diagram
   `intent` each maps to — *before* you generate anything. Match the user's request to
   the correct viewpoint(s).
3. **If `lifecycle` is set, read `lifecycles/<lifecycle>.yaml`** to see the current
   `phase`'s expected artifacts and its gate.
4. **Then act**, using the framework's viewpoint vocabulary and the default notation
   (unless the user names a notation).

If `se-project.yaml` is missing or `framework` is `null`, ask the user to run
`/framework-manager select <framework>` first (or offer to create one from
`se-project.example.yaml`).

### Worked example — "make an OV diagram" under DoDAF

1. Read `se-project.yaml` → `framework: dodaf`.
2. Read `frameworks/dodaf.yaml` → the Operational View viewpoints are **OV-1** (concept
   graphic, intent `context`), **OV-2** (resource flow, intent `behavior`), **OV-5b**
   (activity model, intent `behavior`).
3. Map "an OV diagram" to those. Produce **OV-1** by default (the high-level concept
   graphic), or ask which OV product if the intent is ambiguous.
4. Render it in the default notation from state (or the one the user asked for), from
   the shared model in the digital thread.

The same pattern holds for UAF (operational/resources/… viewpoints) and C4
(Context/Container/Component) — the framework file is always the source of which
viewpoints exist and what each means.

## Reference

- Frameworks: `frameworks/*.yaml` (conform to `frameworks/_schema.yaml`).
- Lifecycles: `lifecycles/*.yaml` (conform to `lifecycles/_schema.yaml`).
- Extension points: `registry/compute.yaml`, `registry/diagram-backends.yaml`.
- Skills read state first — see each skill's "Session context (read first)" section.
