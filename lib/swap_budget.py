"""SWaP-C Budget Roll-Up and Margin Calculations.

Computes Size/Weight/Power/Cost budgets from component-level data,
calculates margins against allocations, and identifies critical contributors.

Reference: NASA SE Handbook, MIL-STD-881F, ECSS-E-HB-10-02A
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple


# Default growth factors by data maturity (NASA SE Handbook typical)
DEFAULT_GROWTH_FACTORS = {
    "measured": 0.03,
    "vendor_spec": 0.05,
    "estimated": 0.15,
    "TBD": 0.30,
}

# RAG margin thresholds
RAG_GREEN_THRESHOLD = 20.0    # >= 20% margin
RAG_YELLOW_THRESHOLD = 10.0   # >= 10% margin
CONCENTRATION_THRESHOLD = 25.0  # flag if single component > 25%


@dataclass
class Component:
    """A system component with SWaP-C attributes."""
    id: str
    name: str
    subsystem: str = ""
    weight_kg: float = 0.0
    volume_cm3: float = 0.0
    power_W: float = 0.0
    cost_USD: float = 0.0
    maturity: str = "estimated"
    confidence: str = "medium"


@dataclass
class Allocations:
    """System-level budget allocations."""
    weight_kg: Optional[float] = None
    volume_cm3: Optional[float] = None
    power_W: Optional[float] = None
    cost_USD: Optional[float] = None


@dataclass
class DimensionBudget:
    """Budget analysis for a single dimension (weight, power, etc.)."""
    total: float
    allocation: Optional[float]
    margin_absolute: Optional[float]
    margin_pct: Optional[float]
    status: Optional[str]
    unit: str
    top_contributors: List[Dict]
    by_subsystem: List[Dict]


@dataclass
class BudgetResult:
    """Complete SWaP-C budget analysis result."""
    weight: Optional[DimensionBudget] = None
    power: Optional[DimensionBudget] = None
    cost: Optional[DimensionBudget] = None
    volume: Optional[DimensionBudget] = None
    growth_analysis: Dict = field(default_factory=dict)
    data_quality: Dict = field(default_factory=dict)
    warnings: List[str] = field(default_factory=list)
    computation_steps: List[Dict] = field(default_factory=list)


def classify_margin(margin_pct: float) -> str:
    """Classify margin as RAG status."""
    if margin_pct < 0:
        return "RED_OVERBUDGET"
    elif margin_pct < RAG_YELLOW_THRESHOLD:
        return "RED"
    elif margin_pct < RAG_GREEN_THRESHOLD:
        return "YELLOW"
    else:
        return "GREEN"


def compute_dimension_budget(
    components: List[Component],
    dimension: str,
    allocation: Optional[float],
    unit: str,
    step_counter: List[int],
    steps: List[Dict],
) -> Tuple[Optional[DimensionBudget], List[str]]:
    """Compute budget for a single dimension.

    Args:
        components: List of system components.
        dimension: Attribute name (weight_kg, power_W, etc.).
        allocation: Budget allocation for this dimension.
        unit: Unit string for output.
        step_counter: Mutable counter for computation trace steps.
        steps: Mutable list of computation trace steps.

    Returns:
        Tuple of (DimensionBudget, list of warnings).
    """
    warnings = []
    values = [(c, getattr(c, dimension, 0.0)) for c in components]

    # Filter for consumers only (positive values) for budget dimensions
    # Exception: power sources may be negative
    consumer_values = [(c, v) for c, v in values if v > 0]
    if not consumer_values and dimension != "power_W":
        return None, []

    total = sum(v for _, v in consumer_values)

    # Record summation step
    step_counter[0] += 1
    addends = " + ".join(f"{v}" for _, v in consumer_values)
    steps.append({
        "step": step_counter[0],
        "operation": f"{dimension}_sum",
        "expression": addends,
        "result": round(total, 2),
        "unit": unit,
    })

    # Margin calculation
    margin_abs = None
    margin_pct = None
    status = None
    if allocation is not None and allocation > 0:
        margin_abs = round(allocation - total, 2)
        margin_pct = round((allocation - total) / allocation * 100, 1)
        status = classify_margin(margin_pct)

        step_counter[0] += 1
        steps.append({
            "step": step_counter[0],
            "operation": f"{dimension}_margin_pct",
            "expression": f"({allocation} - {round(total, 2)}) / {allocation} * 100",
            "result": margin_pct,
            "unit": "%",
        })

        if status in ("RED", "RED_OVERBUDGET"):
            warnings.append(
                f"{dimension} margin is {status} ({margin_pct}%)"
            )

    # Pareto analysis
    top_contributors = []
    if total > 0:
        sorted_components = sorted(
            consumer_values, key=lambda x: x[1], reverse=True
        )
        cumulative = 0.0
        for c, v in sorted_components[:5]:
            pct = round(v / total * 100, 1)
            cumulative += pct
            top_contributors.append({
                "component_id": c.id,
                "name": c.name,
                "value": v,
                "contribution_pct": pct,
            })
            if pct > CONCENTRATION_THRESHOLD:
                warnings.append(
                    f"{c.name} ({c.id}) exceeds {CONCENTRATION_THRESHOLD}% "
                    f"concentration for {dimension} ({pct}%)"
                )

    # Subsystem breakdown
    subsystem_totals: Dict[str, float] = {}
    for c, v in consumer_values:
        sub = c.subsystem or "Unassigned"
        subsystem_totals[sub] = subsystem_totals.get(sub, 0.0) + v

    by_subsystem = sorted(
        [
            {
                "subsystem": sub,
                "total": round(val, 2),
                "contribution_pct": round(val / total * 100, 1) if total > 0 else 0,
            }
            for sub, val in subsystem_totals.items()
        ],
        key=lambda x: x["total"],
        reverse=True,
    )

    budget = DimensionBudget(
        total=round(total, 2),
        allocation=allocation,
        margin_absolute=margin_abs,
        margin_pct=margin_pct,
        status=status,
        unit=unit,
        top_contributors=top_contributors,
        by_subsystem=by_subsystem,
    )

    return budget, warnings


def compute_budget_rollup(
    components: List[Component],
    allocations: Allocations,
    growth_factors: Optional[Dict[str, float]] = None,
) -> BudgetResult:
    """Compute full SWaP-C budget rollup with margins and Pareto analysis.

    Args:
        components: List of system components with SWaP-C attributes.
        allocations: System-level budget allocations.
        growth_factors: Growth factors by maturity level. Defaults to NASA typical.

    Returns:
        BudgetResult with complete analysis and computation trace.
    """
    if not components:
        raise ValueError("At least one component is required")

    gf = growth_factors or DEFAULT_GROWTH_FACTORS
    steps: List[Dict] = []
    step_counter = [0]
    all_warnings: List[str] = []

    # Compute each dimension
    dimensions = [
        ("weight_kg", allocations.weight_kg, "kg"),
        ("power_W", allocations.power_W, "W"),
        ("cost_USD", allocations.cost_USD, "USD"),
        ("volume_cm3", allocations.volume_cm3, "cm3"),
    ]

    results = {}
    for dim, alloc, unit in dimensions:
        budget, warnings = compute_dimension_budget(
            components, dim, alloc, unit, step_counter, steps
        )
        results[dim] = budget
        all_warnings.extend(warnings)

    # Data quality assessment
    maturity_counts: Dict[str, int] = {}
    for c in components:
        mat = c.maturity or "estimated"
        maturity_counts[mat] = maturity_counts.get(mat, 0) + 1

    estimated_or_tbd = maturity_counts.get("estimated", 0) + maturity_counts.get("TBD", 0)
    estimated_pct = round(estimated_or_tbd / len(components) * 100, 1)

    if estimated_pct > 50:
        all_warnings.append(
            f"{estimated_pct}% of components are estimated/TBD - "
            "recommend firming up data"
        )

    # Growth analysis
    growth_analysis = {}
    for dim, alloc, unit in dimensions:
        if results.get(dim) is None:
            continue
        grown_values = []
        for c in components:
            val = getattr(c, dim, 0.0)
            if val > 0:
                factor = gf.get(c.maturity, gf.get("estimated", 0.15))
                grown_values.append(val * (1 + factor))
        if grown_values:
            total_grown = round(sum(grown_values), 2)
            grown_margin_pct = None
            grown_status = None
            if alloc and alloc > 0:
                grown_margin_pct = round((alloc - total_grown) / alloc * 100, 1)
                grown_status = classify_margin(grown_margin_pct)
            growth_analysis[dim] = {
                "total_grown": total_grown,
                "margin_grown_pct": grown_margin_pct,
                "status_grown": grown_status,
            }

    return BudgetResult(
        weight=results.get("weight_kg"),
        power=results.get("power_W"),
        cost=results.get("cost_USD"),
        volume=results.get("volume_cm3"),
        growth_analysis=growth_analysis,
        data_quality={
            "total_components": len(components),
            "by_maturity": maturity_counts,
            "estimated_or_tbd_pct": estimated_pct,
        },
        warnings=all_warnings,
        computation_steps=steps,
    )
