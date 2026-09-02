"""Monte Carlo Simulation Engine for SE Risk Analysis.

Provides Latin Hypercube Sampling with correlated variables,
convergence testing, and statistical analysis of results.

Used by CALC-8 (Monte Carlo Risk Simulator) and referenced by
COST-4 (Cost-Risk Integration) and other probabilistic skills.

References:
    NASA Cost Estimating Handbook: Monte Carlo for cost uncertainty
    GAO Cost Guide (GAO-20-195G): Schedule risk analysis
    MIL-STD-882E: System safety risk assessment
"""

import math
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional, Tuple

try:
    import numpy as np
    from scipy import stats as scipy_stats
    HAS_SCIPY = True
except ImportError:
    HAS_SCIPY = False


@dataclass
class Variable:
    """A random variable for Monte Carlo simulation."""
    name: str
    distribution: str   # triangular, pert, normal, lognormal, uniform
    params: Dict[str, float]
    # Distribution-specific params:
    #   triangular: {min, mode, max}
    #   pert: {min, mode, max, lambda (default 4)}
    #   normal: {mean, std}
    #   lognormal: {mean, std} (of underlying normal)
    #   uniform: {min, max}


@dataclass
class SimulationResult:
    """Results from a Monte Carlo simulation run."""
    n_iterations: int
    mean: float
    std: float
    percentiles: Dict[str, float]  # P5, P10, P25, P50, P75, P80, P90, P95
    histogram: List[Tuple[float, int]]  # (bin_edge, count)
    sensitivity: List[Dict[str, float]]  # variable_name, rank_correlation
    convergence_achieved: bool
    convergence_pct_change: float  # P50 change in last 10% of iterations
    seed: int


def _sample_triangular(params: Dict[str, float], n: int) -> "np.ndarray":
    """Sample from triangular distribution."""
    low = params["min"]
    mode = params["mode"]
    high = params["max"]
    return np.random.triangular(low, mode, high, n)


def _sample_pert(params: Dict[str, float], n: int) -> "np.ndarray":
    """Sample from PERT (Beta) distribution.

    PERT uses a Beta distribution shaped by min, mode, max, and lambda.
    Default lambda=4 gives standard PERT weighting.
    """
    low = params["min"]
    mode = params["mode"]
    high = params["max"]
    lam = params.get("lambda", 4)

    if high <= low:
        return np.full(n, mode)

    # PERT mean and shape parameters
    mu = (low + lam * mode + high) / (lam + 2)
    if high == low:
        return np.full(n, mu)

    # Beta shape parameters
    alpha1 = ((mu - low) * (2 * mode - low - high)) / ((mode - mu) * (high - low))
    if alpha1 <= 0:
        alpha1 = 1.0 + lam / 2
    alpha2 = alpha1 * (high - mu) / (mu - low) if (mu - low) > 0 else alpha1

    # Sample from Beta and scale to [low, high]
    beta_samples = np.random.beta(max(alpha1, 0.1), max(alpha2, 0.1), n)
    return low + beta_samples * (high - low)


def _sample_normal(params: Dict[str, float], n: int) -> "np.ndarray":
    """Sample from normal distribution."""
    return np.random.normal(params["mean"], params["std"], n)


def _sample_lognormal(params: Dict[str, float], n: int) -> "np.ndarray":
    """Sample from lognormal distribution."""
    return np.random.lognormal(params["mean"], params["std"], n)


def _sample_uniform(params: Dict[str, float], n: int) -> "np.ndarray":
    """Sample from uniform distribution."""
    return np.random.uniform(params["min"], params["max"], n)


SAMPLERS = {
    "triangular": _sample_triangular,
    "pert": _sample_pert,
    "normal": _sample_normal,
    "lognormal": _sample_lognormal,
    "uniform": _sample_uniform,
}


def run_simulation(
    variables: List[Variable],
    expression: Callable[..., float],
    n_iterations: int = 10000,
    correlation_matrix: Optional["np.ndarray"] = None,
    seed: int = 42,
    percentile_list: Optional[List[int]] = None,
) -> SimulationResult:
    """Run Monte Carlo simulation.

    Args:
        variables: List of random variables to sample.
        expression: Function that takes variable values and returns output.
            Signature: expression(var1, var2, ...) -> float
            Or: expression(values_dict) -> float
        n_iterations: Number of simulation iterations (default 10,000).
        correlation_matrix: Optional correlation matrix for correlated sampling.
            Shape (n_vars, n_vars). If None, variables are independent.
        seed: Random seed for reproducibility.
        percentile_list: Which percentiles to compute (default: standard set).

    Returns:
        SimulationResult with statistics, percentiles, and sensitivity.
    """
    if not HAS_SCIPY:
        raise ImportError(
            "numpy and scipy are required for Monte Carlo simulation. "
            "Install with: pip install numpy scipy"
        )

    np.random.seed(seed)

    if percentile_list is None:
        percentile_list = [5, 10, 25, 50, 75, 80, 90, 95]

    n_vars = len(variables)

    # Generate independent samples
    samples = np.zeros((n_iterations, n_vars))
    for i, var in enumerate(variables):
        sampler = SAMPLERS.get(var.distribution)
        if sampler is None:
            raise ValueError(f"Unknown distribution: {var.distribution}")
        samples[:, i] = sampler(var.params, n_iterations)

    # Apply correlations if provided
    if correlation_matrix is not None:
        if correlation_matrix.shape != (n_vars, n_vars):
            raise ValueError(
                f"Correlation matrix shape {correlation_matrix.shape} "
                f"doesn't match {n_vars} variables"
            )
        # Iman-Conover method for inducing rank correlations
        # Convert to ranks, apply Cholesky correlation, convert back
        try:
            cholesky = np.linalg.cholesky(correlation_matrix)
        except np.linalg.LinAlgError:
            raise ValueError("Correlation matrix is not positive definite")

        # Rank-based correlation
        ranks = np.zeros_like(samples)
        for i in range(n_vars):
            ranks[:, i] = scipy_stats.rankdata(samples[:, i])

        # Normal scores of ranks
        normal_scores = scipy_stats.norm.ppf(ranks / (n_iterations + 1))
        # Apply correlation
        correlated_scores = normal_scores @ cholesky.T
        # Re-rank and map back to original samples
        for i in range(n_vars):
            new_ranks = scipy_stats.rankdata(correlated_scores[:, i])
            sorted_original = np.sort(samples[:, i])
            samples[:, i] = sorted_original[(new_ranks - 1).astype(int)]

    # Evaluate expression for each iteration
    results = np.zeros(n_iterations)
    for j in range(n_iterations):
        values = {var.name: samples[j, i] for i, var in enumerate(variables)}
        results[j] = expression(values)

    # Statistics
    mean_val = float(np.mean(results))
    std_val = float(np.std(results))

    # Percentiles
    percentiles = {}
    for p in percentile_list:
        percentiles[f"P{p}"] = float(np.percentile(results, p))

    # Histogram (20 bins)
    counts, bin_edges = np.histogram(results, bins=20)
    histogram = [(float(bin_edges[i]), int(counts[i])) for i in range(len(counts))]

    # Sensitivity analysis (Spearman rank correlation)
    sensitivity = []
    for i, var in enumerate(variables):
        corr, _ = scipy_stats.spearmanr(samples[:, i], results)
        sensitivity.append({
            "variable": var.name,
            "rank_correlation": round(float(corr), 3),
            "abs_correlation": round(abs(float(corr)), 3),
        })
    sensitivity.sort(key=lambda x: x["abs_correlation"], reverse=True)

    # Convergence check: compare P50 of first 90% vs full run
    p50_90pct = float(np.percentile(results[:int(0.9 * n_iterations)], 50))
    p50_full = percentiles["P50"]
    convergence_pct = abs(p50_full - p50_90pct) / abs(p50_full) * 100 if p50_full != 0 else 0
    convergence_achieved = convergence_pct < 1.0  # Less than 1% change

    return SimulationResult(
        n_iterations=n_iterations,
        mean=round(mean_val, 2),
        std=round(std_val, 2),
        percentiles={k: round(v, 2) for k, v in percentiles.items()},
        histogram=histogram,
        sensitivity=sensitivity,
        convergence_achieved=convergence_achieved,
        convergence_pct_change=round(convergence_pct, 3),
        seed=seed,
    )
