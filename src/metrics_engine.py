"""
ScoutBench Metrics & Archetype Engine
Computes positional percentile ranks (using scipy) and classifies tactical player archetypes across 6 specialized roles.
"""

from typing import Dict, List, Tuple
import pandas as pd
import numpy as np
from scipy.stats import percentileofscore
from src.config import METRIC_LABELS


def compute_player_percentiles(
    player_row: pd.Series,
    peer_df: pd.DataFrame,
    metrics: List[str]
) -> Dict[str, float]:
    """
    Calculates the percentile ranking (0 to 100) for each specified metric 
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


def extract_strengths_and_vulnerabilities(
    percentiles: Dict[str, float],
    high_threshold: float = 80.0,
    low_threshold: float = 35.0
) -> Tuple[List[Dict[str, any]], List[Dict[str, any]]]:
    """
    Identifies a player's top traits:
    - Strengths: Metrics with percentiles >= high_threshold
    - Vulnerabilities: Metrics with percentiles <= low_threshold
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


def classify_tactical_archetype(
    percentiles: Dict[str, float],
    position_group: str
) -> str:
    """
    Algorithmic badge assignment across 6 granular positional roles.
    """
    p = percentiles
    
    if position_group == "Goalkeeper":
        if p.get("def_actions_outside_pen_per90", 0) >= 75 and p.get("passes_completed_long_pct", 0) >= 70:
            return "Proactive Sweeper-Keeper"
        elif p.get("psxg_net_per90", 0) >= 80 or p.get("save_pct", 0) >= 80:
            return "Elite Shot-Stopper"
        elif p.get("pass_completion_pct", 0) >= 80:
            return "Ball-Playing Keeper"
        return "Modern Goalkeeper"

    elif position_group == "Centreback":
        if p.get("progressive_passes_per90", 0) >= 75 and p.get("pass_completion_pct", 0) >= 75:
            return "Ball-Playing High-Line CB"
        elif p.get("aerial_win_pct", 0) >= 75 and p.get("blocks_per90", 0) >= 70:
            return "Dominant Box Stopper"
        elif p.get("progressive_carries_per90", 0) >= 70:
            return "Ball-Carrying Defender"
        return "Complete Centreback"

    elif position_group == "Fullback / Wingback":
        if p.get("progressive_passes_per90", 0) >= 75 and p.get("pass_completion_pct", 0) >= 75:
            return "Inverted Playmaking Fullback"
        elif p.get("take_ons_attempted_per90", 0) >= 75 and p.get("progressive_carries_per90", 0) >= 75:
            return "Attacking Overlapping Wingback"
        elif p.get("padj_tackles_per90", 0) >= 75:
            return "Defensive Fullback"
        return "Modern Dual-Flank Fullback"

    elif position_group == "Central / Defensive Midfielder":
        if p.get("pass_completion_pct", 0) >= 80 and p.get("progressive_passes_per90", 0) >= 75:
            return "Deep Tempo Dictator"
        elif p.get("xAG_per90", 0) >= 75 or p.get("sca_per90", 0) >= 80:
            return "Half-Space Creator"
        elif p.get("ball_recoveries_per90", 0) >= 70 and p.get("progressive_carries_per90", 0) >= 65:
            return "Box-to-Box Engine"
        elif p.get("padj_tackles_per90", 0) >= 75 and p.get("padj_interceptions_per90", 0) >= 75:
            return "Defensive Ball-Winner"
        return "Complete Central Midfielder"

    elif position_group == "Winger / Attacking Mid":
        if p.get("take_ons_attempted_per90", 0) >= 80 and p.get("take_on_success_pct", 0) >= 60:
            return "1v1 Isolation Winger"
        elif p.get("npxG_per90", 0) >= 75 and p.get("touches_att_pen_per90", 0) >= 70:
            return "Inverted Goalscorer"
        elif p.get("xAG_per90", 0) >= 75 or p.get("sca_per90", 0) >= 75:
            return "Wide Playmaker"
        return "Direct Attacking Winger"

    elif position_group == "Centre-Forward / Striker":
        if p.get("npxG_per90", 0) >= 80 and p.get("shots_on_target_pct", 0) >= 75:
            return "Elite Box Poacher"
        elif p.get("xAG_per90", 0) >= 70 and p.get("key_passes_per90", 0) >= 70:
            return "False Nine / Creative CF"
        elif p.get("aerial_win_pct", 0) >= 75 and p.get("touches_att_pen_per90", 0) >= 70:
            return "Target Forward"
        return "Complete Centre-Forward"

    return "All-Round Performer"
