"""
ScoutBench Metrics & Analytics Engine
Computes positional percentile ranks, continuous tactical spectrums,
universal behavioral indexes, and pro-tier scouting intelligence dossiers.
"""

from typing import Dict, List, Tuple, Any, Optional
import pandas as pd
import numpy as np
from scipy.stats import percentileofscore
from src.config import METRIC_LABELS, TACTICAL_SPECTRUM_CONFIG, BEHAVIORAL_INDEX_CONFIG


def compute_player_percentiles(
    player_row: pd.Series,
    peer_df: pd.DataFrame,
    metrics: List[str]
) -> Dict[str, float]:
    """
    Calculates the percentile ranking (0.0 to 100.0) for each specified metric 
    of a target player relative to their positional cohort.
    """
    percentiles: Dict[str, float] = {}
    
    for metric in metrics:
        if metric in peer_df.columns and pd.notna(player_row.get(metric)):
            cohort_values = peer_df[metric].dropna().values
            player_val = player_row[metric]
            
            if len(cohort_values) > 0:
                pct = percentileofscore(cohort_values, player_val, kind="weak")
                percentiles[metric] = round(float(pct), 1)
            else:
                percentiles[metric] = 50.0
        else:
            percentiles[metric] = 50.0
            
    return percentiles


def compute_tactical_spectrum(
    percentiles: Dict[str, float],
    position_group: str
) -> Dict[str, Any]:
    """
    Computes a continuous 4-axis Tactical Spectrum (0-100) based on weighted 
    positional attribute percentiles (FM / Pro analytics matrix style).
    Returns continuous axis scores and dynamically derives primary & secondary archetypes.
    """
    pos_config = TACTICAL_SPECTRUM_CONFIG.get(
        position_group, 
        TACTICAL_SPECTRUM_CONFIG["Central / Defensive Midfielder"]
    )
    
    axes_results = []
    
    for axis_name, axis_info in pos_config.items():
        weights = axis_info["weights"]
        total_weight = sum(weights.values())
        
        weighted_score = 0.0
        for metric, w in weights.items():
            pct = percentiles.get(metric, 50.0)
            weighted_score += (w * pct)
            
        final_score = round(weighted_score / total_weight, 1) if total_weight > 0 else 50.0
        final_score = max(0.0, min(100.0, final_score))
        
        axes_results.append({
            "name": axis_name,
            "score": final_score,
            "archetype": axis_info["archetype"],
            "description": axis_info["description"]
        })
        
    # Sort axes to identify dominant primary archetype and secondary stylistic tendency
    sorted_axes = sorted(axes_results, key=lambda x: x["score"], reverse=True)
    primary = sorted_axes[0]["archetype"] if sorted_axes else "All-Round Performer"
    secondary = sorted_axes[1]["archetype"] if len(sorted_axes) > 1 else None
    
    return {
        "axes": axes_results,
        "primary_archetype": primary,
        "secondary_archetype": secondary,
        "dominant_axis": sorted_axes[0]["name"] if sorted_axes else ""
    }


def compute_behavioral_indexes(
    percentiles: Dict[str, float],
    position_group: str
) -> Dict[str, Dict[str, Any]]:
    """
    Computes 4 Universal Behavioral & Work-Rate Indexes (0.0 to 100.0):
    - High-Press & Work-Rate Index (HPWI)
    - Verticality & Directness Index (VDI)
    - Press-Resistance & Retention Index (PRBI)
    - Offensive Threat & Opportunity Index (OOTI)
    """
    indexes: Dict[str, Dict[str, Any]] = {}
    
    for idx_name, idx_info in BEHAVIORAL_INDEX_CONFIG.items():
        weights = idx_info["weights"]
        total_weight = sum(weights.values())
        
        weighted_score = 0.0
        for metric, w in weights.items():
            pct = percentiles.get(metric, 50.0)
            weighted_score += (w * pct)
            
        final_score = round(weighted_score / total_weight, 1) if total_weight > 0 else 50.0
        final_score = max(0.0, min(100.0, final_score))
        
        indexes[idx_name] = {
            "score": final_score,
            "description": idx_info["description"]
        }
        
    return indexes


def classify_tactical_archetype(
    percentiles: Dict[str, float],
    position_group: str
) -> str:
    """
    Derives the dominant primary tactical archetype from the continuous tactical spectrum.
    Maintains backwards-compatibility.
    """
    spectrum = compute_tactical_spectrum(percentiles, position_group)
    return spectrum["primary_archetype"]


def extract_strengths_and_vulnerabilities(
    percentiles: Dict[str, float],
    high_threshold: float = 80.0,
    low_threshold: float = 35.0
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Identifies top statistical strengths (>= high_threshold) and vulnerabilities (<= low_threshold).
    """
    strengths = []
    vulnerabilities = []
    
    for metric, pct in percentiles.items():
        label = METRIC_LABELS.get(metric, metric)
        if pct >= high_threshold:
            strengths.append({"metric": metric, "label": label, "percentile": pct})
        elif pct <= low_threshold:
            vulnerabilities.append({"metric": metric, "label": label, "percentile": pct})
            
    strengths = sorted(strengths, key=lambda x: x["percentile"], reverse=True)
    vulnerabilities = sorted(vulnerabilities, key=lambda x: x["percentile"])
    
    return strengths, vulnerabilities


def generate_scouting_intelligence(
    player_row: pd.Series,
    percentiles: Dict[str, float],
    spectrum: Dict[str, Any],
    behavioral_indexes: Dict[str, Dict[str, Any]],
    position_group: str
) -> Dict[str, Any]:
    """
    Synthesizes deep tactical intelligence notes, identifying off-the-ball behavior,
    system translatability, and core tactical tendencies without superficial summaries.
    """
    hpwi = behavioral_indexes.get("High-Press & Work-Rate", {}).get("score", 50.0)
    vdi = behavioral_indexes.get("Verticality & Directness", {}).get("score", 50.0)
    prbi = behavioral_indexes.get("Press-Resistance & Retention", {}).get("score", 50.0)
    ooti = behavioral_indexes.get("Offensive Threat & Opportunity", {}).get("score", 50.0)
    
    system_notes = []
    
    # 1. Pressing & Work-Rate Tactical Behavior
    if hpwi >= 75.0:
        system_notes.append({
            "badge": "ELITE COUNTER-PRESSER",
            "tone": "positive",
            "text": f"Registers an elite High-Press & Work-Rate index ({hpwi:.0f}/100). Highly proactive in front-foot counter-pressing traps, high regains, and defensive transitions. Optimal fit for aggressive high-pressing systems."
        })
    elif hpwi <= 35.0:
        system_notes.append({
            "badge": "PASSIVE OFF-THE-BALL",
            "tone": "warning",
            "text": f"Low defensive work-rate output ({hpwi:.0f}/100). Functions primarily as a luxury option or resting outlet in transitions; requires structured defensive cover in high-intensity pressing setups."
        })
        
    # 2. Progression & Directness Profile
    if vdi >= 75.0:
        system_notes.append({
            "badge": "HIGH-VERTICALITY OUTLET",
            "tone": "positive",
            "text": f"Direct space-eater ({vdi:.0f}/100 Verticality Index). Aggressively propels possession forward through line-breaking passes or direct vertical carries into territory."
        })
    elif vdi <= 35.0:
        system_notes.append({
            "badge": "LATERAL RECYCLER",
            "tone": "neutral",
            "text": f"Conservative progression profile ({vdi:.0f}/100 Verticality). Prioritizes safe sideways/backwards circulation over high-risk vertical line-breaks."
        })
        
    # 3. Press-Resistance & Ball Retention Under Pressure
    if prbi >= 75.0:
        system_notes.append({
            "badge": "PRESS-RESISTANT ANCHOR",
            "tone": "positive",
            "text": f"Exceptional security under pressure ({prbi:.0f}/100 Press-Resistance). Excels at absorbing physical pressure, evading tackles, and maintaining possession in tight central corridors."
        })
    elif prbi <= 35.0:
        system_notes.append({
            "badge": "TURNOVER RISK UNDER PRESSURE",
            "tone": "warning",
            "text": f"Vulnerable when pressed aggressively ({prbi:.0f}/100 Press-Resistance). Lower ball retention efficiency in congested zones."
        })

    # 4. Attacking Threat
    if ooti >= 75.0:
        system_notes.append({
            "badge": "PRIMARY OFFENSIVE CATALYST",
            "tone": "positive",
            "text": f"High individual offensive production ({ooti:.0f}/100 Threat Index). Major source of direct expected goals (npxG) and chance creation (xAG)."
        })
        
    strengths, vulnerabilities = extract_strengths_and_vulnerabilities(percentiles)
    
    return {
        "primary_archetype": spectrum["primary_archetype"],
        "secondary_archetype": spectrum["secondary_archetype"],
        "dominant_axis": spectrum["dominant_axis"],
        "strengths": strengths,
        "vulnerabilities": vulnerabilities,
        "system_notes": system_notes
    }


def compute_cohort_benchmark(
    df: pd.DataFrame,
    position_group: str,
    season: str,
    benchmark_type: str,
    domestic_league: Optional[str] = None
) -> pd.Series:
    """
    Computes a synthetic cohort benchmark profile by calculating the arithmetic mean
    for all numerical metrics across a filtered peer group.
    
    Supported benchmark types:
    - 'top5_positional': Top 5 European Positional Average (same position_group & season across all 5 leagues)
    - 'domestic_positional': Domestic League Positional Average (same position_group, season & domestic_league)
    - 'u21_european': Under-21 European Positional Average (age <= 21, same position_group & season across all leagues)
    - 'u21_domestic': Under-21 Domestic League Average (age <= 21, same position_group, season & domestic_league)
    """
    if df is None or df.empty:
        raise ValueError("Input DataFrame is empty or None.")
    
    valid_benchmark_types = {
        "top5_positional",
        "domestic_positional",
        "u21_european",
        "u21_domestic"
    }
    
    if benchmark_type not in valid_benchmark_types:
        raise ValueError(
            f"Unsupported benchmark_type '{benchmark_type}'. "
            f"Supported types are: {', '.join(sorted(valid_benchmark_types))}"
        )
    
    # Base filter by season and position group
    mask = (df["season"] == season) & (df["position_group"] == position_group)
    
    if benchmark_type == "top5_positional":
        label = f"Top 5 European {position_group} Average"
        league_val = "Top 5 European Leagues"
    elif benchmark_type == "domestic_positional":
        if not domestic_league:
            raise ValueError("domestic_league must be specified for 'domestic_positional' benchmark.")
        mask = mask & (df["league"] == domestic_league)
        label = f"{domestic_league} {position_group} Average"
        league_val = domestic_league
    elif benchmark_type == "u21_european":
        mask = mask & (df["age"] <= 21)
        label = f"U-21 European {position_group} Average"
        league_val = "Top 5 European Leagues (U-21)"
    elif benchmark_type == "u21_domestic":
        if not domestic_league:
            raise ValueError("domestic_league must be specified for 'u21_domestic' benchmark.")
        mask = mask & (df["league"] == domestic_league) & (df["age"] <= 21)
        label = f"U-21 {domestic_league} {position_group} Average"
        league_val = f"{domestic_league} (U-21)"
    
    filtered_df = df[mask]
    if filtered_df.empty:
        raise ValueError(
            f"No player records found for benchmark '{benchmark_type}' "
            f"(position_group='{position_group}', season='{season}', domestic_league='{domestic_league}')."
        )
    
    # Compute arithmetic mean for all numeric columns
    numeric_means = filtered_df.mean(numeric_only=True)
    
    # Synthesize virtual benchmark profile Series
    benchmark_profile = numeric_means.copy()
    benchmark_profile["player"] = label
    benchmark_profile["team"] = "Cohort Benchmark"
    benchmark_profile["league"] = league_val
    benchmark_profile["position_group"] = position_group
    benchmark_profile["position"] = position_group
    benchmark_profile["season"] = season
    benchmark_profile["sample_size"] = int(len(filtered_df))
    benchmark_profile["preferred_foot"] = "N/A"
    benchmark_profile["nationality"] = "Benchmark / Mixed"
    benchmark_profile["primary_position"] = position_group
    benchmark_profile["secondary_position"] = "None"
    benchmark_profile["wage_tier"] = "Benchmark Average"
    
    if "age" in numeric_means:
        benchmark_profile["age"] = round(float(numeric_means["age"]), 1)
    if "minutes" in numeric_means:
        benchmark_profile["minutes"] = int(round(numeric_means["minutes"]))
    if "contract_expiry" in numeric_means:
        benchmark_profile["contract_expiry"] = int(round(numeric_means["contract_expiry"]))
    if "market_value_eur" in numeric_means:
        benchmark_profile["market_value_eur"] = float(numeric_means["market_value_eur"])
        
    return benchmark_profile


def compute_comparison_deltas(
    base_row: pd.Series,
    base_percentiles: Dict[str, float],
    compared_rows: List[pd.Series],
    compared_percentiles: List[Dict[str, float]],
    metrics: List[str]
) -> pd.DataFrame:
    """
    Computes statistical deltas (raw per-90 difference and percentile difference)
    between a base target player and 1 to 3 compared player/benchmark profiles.
    
    For each compared profile i:
      delta_val = compared_val - base_val
      delta_pct = compared_pct - base_pct
      
    Returns a structured DataFrame suitable for tabular side-by-side rendering.
    """
    rows = []
    
    for metric in metrics:
        metric_label = METRIC_LABELS.get(metric, metric)
        
        # Base values
        base_val_raw = base_row.get(metric, np.nan) if base_row is not None else np.nan
        base_val = float(base_val_raw) if pd.notna(base_val_raw) else 0.0
        base_pct = float(base_percentiles.get(metric, 50.0))
        
        row_dict: Dict[str, Any] = {
            "metric": metric,
            "metric_label": metric_label,
            "base_val": round(base_val, 2),
            "base_pct": round(base_pct, 1),
        }
        
        # Add compared profiles
        for idx, (comp_row, comp_pcts) in enumerate(zip(compared_rows, compared_percentiles)):
            slot_num = idx + 1
            comp_name = comp_row.get("player", f"Profile {slot_num}") if comp_row is not None else f"Profile {slot_num}"
            
            comp_val_raw = comp_row.get(metric, np.nan) if comp_row is not None else np.nan
            comp_val = float(comp_val_raw) if pd.notna(comp_val_raw) else 0.0
            comp_pct = float(comp_pcts.get(metric, 50.0))
            
            delta_val = comp_val - base_val
            delta_pct = comp_pct - base_pct
            
            # Keyed by slot
            row_dict[f"comp_{slot_num}_name"] = comp_name
            row_dict[f"comp_{slot_num}_val"] = round(comp_val, 2)
            row_dict[f"comp_{slot_num}_pct"] = round(comp_pct, 1)
            row_dict[f"comp_{slot_num}_delta_val"] = round(delta_val, 2)
            row_dict[f"comp_{slot_num}_delta_pct"] = round(delta_pct, 1)
            
        rows.append(row_dict)
        
    return pd.DataFrame(rows)

