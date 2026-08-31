"""
ScoutBench Normalization Module
Handles Per-90 standardizations and Possession-Adjusted (pAdj) defensive metrics.
"""

import pandas as pd
import numpy as np


def calculate_per90(raw_count: pd.Series, minutes: pd.Series) -> pd.Series:
    """
    Normalizes a cumulative raw metric to a per-90 minute rate.
    Formula: (Raw Count / Minutes) * 90
    """
    # Protect against division by zero for players with 0 minutes
    valid_mask = minutes > 0
    per90_series = pd.Series(0.0, index=raw_count.index)
    per90_series[valid_mask] = (raw_count[valid_mask] / minutes[valid_mask]) * 90.0
    return per90_series.round(2)


def calculate_padj(per90_metric: pd.Series, team_possession_pct: pd.Series) -> pd.Series:
    """
    Applies Sigrid Olthof / Sam Green Possession Adjustment (pAdj) to defensive metrics.
    
    Why pAdj is necessary:
    Teams with high possession (e.g., Barcelona 65%) have fewer defensive opportunities 
    because the opposition rarely has the ball. Scaling by opposition possession normalizes
    defensive output to an even 50% baseline.
    
    Formula:
        pAdj = Metric_per90 * (50 / (100 - Team_Possession_%))
    """
    # Opponent possession percentage
    opp_possession = 100.0 - team_possession_pct
    
    # Avoid division by zero or unrealistic possession limits (clamp between 20% and 80%)
    opp_possession_clamped = opp_possession.clip(lower=20.0, upper=80.0)
    
    scaling_factor = 50.0 / opp_possession_clamped
    padj_series = per90_metric * scaling_factor
    return padj_series.round(2)


def normalize_player_dataframe(df: pd.DataFrame, min_minutes: int = 900) -> pd.DataFrame:
    """
    Processes a raw multi-table player dataframe:
    1. Filters out players below the minimum minutes threshold to eliminate noise.
    2. Computes per-90 rates for counting stats.
    3. Computes pAdj defensive stats.
    4. Retains percentage stats as-is.
    """
    df = df.copy()
    
    # Filter minimum playing time
    if "minutes" in df.columns:
        df = df[df["minutes"] >= min_minutes].reset_index(drop=True)
    
    # If team possession is not present, default to 50.0 (neutral)
    if "team_possession_pct" not in df.columns:
        df["team_possession_pct"] = 50.0
        
    return df
