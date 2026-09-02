"""Reliability, Maintainability, and Availability Calculations.

Implements series, parallel, k-of-n, and standby reliability models.
Computes MTBF, MTTR, availability, and sparing requirements.

References:
    MIL-HDBK-338B: Electronic Reliability Design Handbook
    IEC 61078: Reliability Block Diagrams
    MIL-STD-721C: Reliability & Maintainability Terms
"""

import math
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple


@dataclass
class ComponentRMA:
    """Component reliability, maintainability, and availability data."""
    id: str
    name: str
    mtbf_hr: float
    mttr_hr: float = 0.0
    mpmt_hr: float = 0.0   # Mean Preventive Maintenance Time
    mldt_hr: float = 0.0   # Mean Logistics Delay Time
    madt_hr: float = 0.0   # Mean Administrative Delay Time


@dataclass
class AvailabilityResult:
    """Availability calculation result for a single item."""
    id: str
    name: str
    mtbf_hr: float
    mttr_hr: float
    mdt_hr: float
    Ai: float       # Inherent availability
    Aa: Optional[float] = None  # Achieved availability
    Ao: Optional[float] = None  # Operational availability
    Ai_nines: float = 0.0
    Ao_nines: float = 0.0
    lambda_per_hr: float = 0.0


def failure_rate_to_mtbf(lambda_per_hr: float) -> float:
    """Convert failure rate to MTBF. MTBF = 1 / lambda."""
    if lambda_per_hr <= 0:
        raise ValueError("Failure rate must be positive")
    return 1.0 / lambda_per_hr


def mtbf_to_failure_rate(mtbf_hr: float) -> float:
    """Convert MTBF to failure rate. lambda = 1 / MTBF."""
    if mtbf_hr <= 0:
        raise ValueError("MTBF must be positive")
    return 1.0 / mtbf_hr


def inherent_availability(mtbf: float, mttr: float) -> float:
    """Compute inherent availability: Ai = MTBF / (MTBF + MTTR).

    Assumes only corrective maintenance, no logistics delays.
    """
    if mtbf <= 0:
        raise ValueError("MTBF must be positive")
    if mttr < 0:
        raise ValueError("MTTR must be non-negative")
    return mtbf / (mtbf + mttr)


def operational_availability(mtbf: float, mdt: float) -> float:
    """Compute operational availability: Ao = MTBF / (MTBF + MDT).

    MDT = MTTR + MLDT + MADT (Mean Downtime includes all delays).
    """
    if mtbf <= 0:
        raise ValueError("MTBF must be positive")
    if mdt < 0:
        raise ValueError("MDT must be non-negative")
    return mtbf / (mtbf + mdt)


def availability_to_nines(availability: float) -> float:
    """Convert availability to 'nines' notation: nines = -log10(1 - A).

    Example: A = 0.999 -> 3.0 nines, A = 0.99999 -> 5.0 nines.
    """
    if availability <= 0 or availability >= 1:
        if availability == 1.0:
            return float("inf")
        raise ValueError("Availability must be between 0 and 1")
    return -math.log10(1.0 - availability)


def series_availability(availabilities: List[float]) -> float:
    """Compute series system availability: A_series = PRODUCT(A[i]).

    All components must work for the system to work.
    """
    if not availabilities:
        raise ValueError("At least one availability value required")
    result = 1.0
    for a in availabilities:
        if not 0 <= a <= 1:
            raise ValueError(f"Availability must be between 0 and 1, got {a}")
        result *= a
    return result


def parallel_availability(availabilities: List[float]) -> float:
    """Compute parallel system availability: A_parallel = 1 - PRODUCT(1 - A[i]).

    System works if any one component works (active redundancy).
    """
    if not availabilities:
        raise ValueError("At least one availability value required")
    result = 1.0
    for a in availabilities:
        if not 0 <= a <= 1:
            raise ValueError(f"Availability must be between 0 and 1, got {a}")
        result *= (1.0 - a)
    return 1.0 - result


def k_of_n_availability(k: int, n: int, component_availability: float) -> float:
    """Compute k-of-n system availability for identical components.

    A = SUM(C(n,j) * A^j * (1-A)^(n-j)) for j = k to n.

    Args:
        k: Minimum number of working components required.
        n: Total number of components.
        component_availability: Availability of each identical component.

    Returns:
        System availability.
    """
    if k < 1 or k > n:
        raise ValueError(f"k must be between 1 and n, got k={k}, n={n}")
    if not 0 <= component_availability <= 1:
        raise ValueError("Component availability must be between 0 and 1")

    a = component_availability
    result = 0.0
    for j in range(k, n + 1):
        binom_coeff = math.comb(n, j)
        result += binom_coeff * (a ** j) * ((1 - a) ** (n - j))
    return result


def series_reliability(failure_rates: List[float], time: float) -> float:
    """Compute series system reliability: R(t) = PRODUCT(exp(-lambda_i * t)).

    Equivalent to R(t) = exp(-SUM(lambda_i) * t) for exponential distribution.
    """
    if time < 0:
        raise ValueError("Time must be non-negative")
    total_lambda = sum(failure_rates)
    return math.exp(-total_lambda * time)


def parallel_reliability(failure_rates: List[float], time: float) -> float:
    """Compute parallel system reliability: R(t) = 1 - PRODUCT(1 - exp(-lambda_i * t))."""
    if time < 0:
        raise ValueError("Time must be non-negative")
    unreliability_product = 1.0
    for lam in failure_rates:
        unreliability_product *= (1.0 - math.exp(-lam * time))
    return 1.0 - unreliability_product


def weighted_mttr(
    failure_rates: List[float], repair_times: List[float]
) -> float:
    """Compute system MTTR weighted by failure rates.

    MTTR_sys = SUM(lambda_i * MTTR_i) / SUM(lambda_i)
    """
    if len(failure_rates) != len(repair_times):
        raise ValueError("failure_rates and repair_times must have same length")
    total_lambda = sum(failure_rates)
    if total_lambda == 0:
        raise ValueError("Total failure rate must be positive")
    weighted_sum = sum(
        lam * mttr for lam, mttr in zip(failure_rates, repair_times)
    )
    return weighted_sum / total_lambda


def poisson_spares(
    demand_rate: float, lead_time: float, confidence: float
) -> int:
    """Compute spare quantity for given confidence level using Poisson distribution.

    Finds minimum n such that P(demand <= n) >= confidence.

    Args:
        demand_rate: Expected demands per unit time (failures/year).
        lead_time: Replenishment lead time in same units.
        confidence: Desired fill rate (e.g., 0.95 for 95%).

    Returns:
        Minimum number of spares.
    """
    if demand_rate < 0:
        raise ValueError("Demand rate must be non-negative")
    if lead_time < 0:
        raise ValueError("Lead time must be non-negative")
    if not 0 < confidence < 1:
        raise ValueError("Confidence must be between 0 and 1")

    expected_demand = demand_rate * lead_time
    if expected_demand == 0:
        return 0

    # Compute cumulative Poisson probability
    cumulative = 0.0
    n = 0
    while cumulative < confidence:
        # P(X = n) = e^(-mu) * mu^n / n!
        prob = math.exp(-expected_demand) * (expected_demand ** n) / math.factorial(n)
        cumulative += prob
        if cumulative >= confidence:
            return n
        n += 1
    return n


def compute_component_availability(component: ComponentRMA) -> AvailabilityResult:
    """Compute all availability types for a single component."""
    mtbf = component.mtbf_hr
    mttr = component.mttr_hr
    mdt = mttr + component.mldt_hr + component.madt_hr

    ai = inherent_availability(mtbf, mttr)
    ao = operational_availability(mtbf, mdt) if mdt > mttr else ai

    return AvailabilityResult(
        id=component.id,
        name=component.name,
        mtbf_hr=mtbf,
        mttr_hr=mttr,
        mdt_hr=mdt,
        Ai=ai,
        Ao=ao,
        Ai_nines=availability_to_nines(ai),
        Ao_nines=availability_to_nines(ao),
        lambda_per_hr=1.0 / mtbf,
    )
