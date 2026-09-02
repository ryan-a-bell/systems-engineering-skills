"""Earned Value Management Metrics and Forecasting.

Computes all standard EVM indices, variance analyses, and completion
forecasts per ANSI/EIA-748 and PMI Practice Standard.

References:
    ANSI/EIA-748: Earned Value Management Systems
    PMI Practice Standard for Earned Value Management
    GAO Cost Estimating Guide (GAO-20-195G)
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple


@dataclass
class EVMInput:
    """Core EVM data elements."""
    BAC: float   # Budget at Completion
    PV: float    # Planned Value (cumulative to date)
    EV: float    # Earned Value (cumulative to date)
    AC: float    # Actual Cost (cumulative to date)
    project_name: str = ""
    reporting_date: str = ""


@dataclass
class EVMMetrics:
    """Complete EVM metric set."""
    # Input summary
    BAC: float
    PV: float
    EV: float
    AC: float
    percent_complete: float
    percent_spent: float

    # Variances
    CV: float       # Cost Variance
    CV_pct: float   # Cost Variance %
    SV: float       # Schedule Variance
    SV_pct: float   # Schedule Variance %

    # Performance Indices
    CPI: float      # Cost Performance Index
    SPI: float      # Schedule Performance Index

    # Forecasts
    EAC_cpi: float          # Estimate at Completion (CPI method)
    EAC_composite: float    # EAC (CPI * SPI method)
    EAC_optimistic: float   # EAC (remaining at planned rate)
    ETC_cpi: float          # Estimate to Complete
    VAC_cpi: float          # Variance at Completion
    TCPI_bac: Optional[float]  # To-Complete PI (to meet BAC)

    # Status
    cost_status: str        # GREEN, YELLOW, RED
    schedule_status: str
    overall_status: str

    # Computation trace
    steps: List[Dict] = field(default_factory=list)


def classify_status(index: float) -> str:
    """Classify CPI or SPI as traffic-light status."""
    if index >= 0.95:
        return "GREEN"
    elif index >= 0.90:
        return "YELLOW"
    else:
        return "RED"


def compute_evm_metrics(data: EVMInput) -> EVMMetrics:
    """Compute all standard EVM metrics with full computation trace.

    Args:
        data: EVMInput with BAC, PV, EV, AC.

    Returns:
        EVMMetrics with all indices, forecasts, status, and trace.

    Raises:
        ValueError: If input data is invalid.
    """
    bac, pv, ev, ac = data.BAC, data.PV, data.EV, data.AC
    steps: List[Dict] = []
    step_num = 0

    # Validation
    if bac <= 0:
        raise ValueError("BAC must be positive")
    if pv <= 0:
        raise ValueError("PV must be positive")
    if ev < 0:
        raise ValueError("EV must be non-negative")
    if ac <= 0:
        raise ValueError("AC must be positive")

    # Percent complete and spent
    step_num += 1
    pct_complete = round(ev / bac * 100, 1)
    steps.append({"step": step_num, "operation": "percent_complete",
                   "expression": f"{ev} / {bac} * 100", "result": pct_complete, "unit": "%"})

    step_num += 1
    pct_spent = round(ac / bac * 100, 1)
    steps.append({"step": step_num, "operation": "percent_spent",
                   "expression": f"{ac} / {bac} * 100", "result": pct_spent, "unit": "%"})

    # Variances
    step_num += 1
    cv = round(ev - ac, 2)
    steps.append({"step": step_num, "operation": "CV",
                   "expression": f"{ev} - {ac}", "result": cv, "unit": "USD"})

    step_num += 1
    cv_pct = round(cv / ev * 100, 1) if ev > 0 else 0
    steps.append({"step": step_num, "operation": "CV_pct",
                   "expression": f"{cv} / {ev} * 100", "result": cv_pct, "unit": "%"})

    step_num += 1
    sv = round(ev - pv, 2)
    steps.append({"step": step_num, "operation": "SV",
                   "expression": f"{ev} - {pv}", "result": sv, "unit": "USD"})

    step_num += 1
    sv_pct = round(sv / pv * 100, 1) if pv > 0 else 0
    steps.append({"step": step_num, "operation": "SV_pct",
                   "expression": f"{sv} / {pv} * 100", "result": sv_pct, "unit": "%"})

    # Performance Indices
    step_num += 1
    cpi = round(ev / ac, 3) if ac > 0 else 0
    steps.append({"step": step_num, "operation": "CPI",
                   "expression": f"{ev} / {ac}", "result": cpi, "unit": ""})

    step_num += 1
    spi = round(ev / pv, 3) if pv > 0 else 0
    steps.append({"step": step_num, "operation": "SPI",
                   "expression": f"{ev} / {pv}", "result": spi, "unit": ""})

    # Estimates at Completion
    step_num += 1
    eac_cpi = round(bac / cpi) if cpi > 0 else float("inf")
    steps.append({"step": step_num, "operation": "EAC_cpi",
                   "expression": f"{bac} / {cpi}", "result": eac_cpi, "unit": "USD"})

    step_num += 1
    cpi_spi = cpi * spi
    eac_composite = round(ac + (bac - ev) / cpi_spi) if cpi_spi > 0 else float("inf")
    steps.append({"step": step_num, "operation": "EAC_composite",
                   "expression": f"{ac} + ({bac} - {ev}) / ({cpi} * {spi})",
                   "result": eac_composite, "unit": "USD"})

    step_num += 1
    eac_optimistic = round(ac + (bac - ev))
    steps.append({"step": step_num, "operation": "EAC_optimistic",
                   "expression": f"{ac} + ({bac} - {ev})", "result": eac_optimistic, "unit": "USD"})

    # Remaining metrics
    step_num += 1
    etc_cpi = round(eac_cpi - ac)
    steps.append({"step": step_num, "operation": "ETC_cpi",
                   "expression": f"{eac_cpi} - {ac}", "result": etc_cpi, "unit": "USD"})

    step_num += 1
    vac_cpi = round(bac - eac_cpi)
    steps.append({"step": step_num, "operation": "VAC_cpi",
                   "expression": f"{bac} - {eac_cpi}", "result": vac_cpi, "unit": "USD"})

    step_num += 1
    tcpi_bac = None
    bac_minus_ac = bac - ac
    if bac_minus_ac > 0:
        tcpi_bac = round((bac - ev) / bac_minus_ac, 3)
        steps.append({"step": step_num, "operation": "TCPI_bac",
                       "expression": f"({bac} - {ev}) / ({bac} - {ac})",
                       "result": tcpi_bac, "unit": ""})
    else:
        steps.append({"step": step_num, "operation": "TCPI_bac",
                       "expression": f"({bac} - {ev}) / ({bac} - {ac})",
                       "result": "undefined (BAC = AC)", "unit": ""})

    # Status classification
    cost_status = classify_status(cpi)
    schedule_status = classify_status(spi)
    # Overall is worst of cost and schedule
    status_order = {"RED": 0, "YELLOW": 1, "GREEN": 2}
    overall_status = cost_status if status_order.get(cost_status, 2) <= status_order.get(schedule_status, 2) else schedule_status

    return EVMMetrics(
        BAC=bac, PV=pv, EV=ev, AC=ac,
        percent_complete=pct_complete, percent_spent=pct_spent,
        CV=cv, CV_pct=cv_pct, SV=sv, SV_pct=sv_pct,
        CPI=cpi, SPI=spi,
        EAC_cpi=eac_cpi, EAC_composite=eac_composite, EAC_optimistic=eac_optimistic,
        ETC_cpi=etc_cpi, VAC_cpi=vac_cpi, TCPI_bac=tcpi_bac,
        cost_status=cost_status, schedule_status=schedule_status,
        overall_status=overall_status, steps=steps,
    )


def earned_schedule(
    pv_curve: List[Tuple[float, float]],
    current_ev: float,
    actual_time: float,
    planned_duration: float,
) -> Dict:
    """Compute Earned Schedule metrics.

    Args:
        pv_curve: List of (time_months, cumulative_pv) tuples.
        current_ev: Current earned value.
        actual_time: Actual elapsed time in months.
        planned_duration: Total planned project duration in months.

    Returns:
        Dict with ES, SV_t, SPI_t, EAC_t.
    """
    if not pv_curve:
        raise ValueError("PV curve must have at least one data point")

    # Find ES by interpolating where PV = current_ev
    es = 0.0
    for i in range(len(pv_curve) - 1):
        t1, pv1 = pv_curve[i]
        t2, pv2 = pv_curve[i + 1]
        if pv1 <= current_ev <= pv2:
            # Linear interpolation
            fraction = (current_ev - pv1) / (pv2 - pv1) if pv2 != pv1 else 0
            es = t1 + fraction * (t2 - t1)
            break
    else:
        # EV is beyond the last PV point or before the first
        if current_ev >= pv_curve[-1][1]:
            es = pv_curve[-1][0]
        else:
            es = pv_curve[0][0]

    sv_t = round(es - actual_time, 1)
    spi_t = round(es / actual_time, 3) if actual_time > 0 else 0
    eac_t = round(actual_time + (planned_duration - es) / spi_t, 1) if spi_t > 0 else float("inf")

    return {
        "ES_months": round(es, 1),
        "AT_months": actual_time,
        "SV_t_months": sv_t,
        "SPI_t": spi_t,
        "EAC_t_months": eac_t,
        "schedule_overrun_months": round(eac_t - planned_duration, 1),
    }


def tcpi_feasibility(tcpi: float) -> str:
    """Assess TCPI recovery feasibility."""
    if tcpi <= 1.0:
        return "feasible"
    elif tcpi <= 1.10:
        return "achievable"
    elif tcpi <= 1.20:
        return "difficult"
    else:
        return "very_difficult"
