# Compute library (not skills)

Deterministic functions imported by the capability skills — **not** agent skills,
so they have no `SKILL.md` and never appear under `/`. Skills reach them through
[`../registry/compute.yaml`](../registry/compute.yaml), never by hard-coded path,
so a built-in module can be swapped for an external calc skill or MCP tool without
editing the skill.

| Module | Capability id | Used by |
|--------|---------------|---------|
| `reliability.py` | `reliability` | ram-analysis |
| `evm.py` | `evm` | project-management |
| `swap_budget.py` | `swap_budget` | project-management, mbse-modeling |
| `monte_carlo.py` | `monte_carlo` | risk-management, trade-study |

`requirements.txt` lists their Python dependencies. Ported from an earlier v2
iteration of this framework.
