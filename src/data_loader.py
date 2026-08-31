"""
ScoutBench Data Loader Module
Handles loading, caching, and cohort filtering for multi-season European league datasets
across 6 specialized positional cohorts.
"""

from typing import Optional, List
from pathlib import Path
import pandas as pd
from src.config import DEFAULT_MIN_MINUTES
from src.normalization import normalize_player_dataframe

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
PROCESSED_DATA_PATH = DATA_DIR / "processed" / "master_players.csv"


def load_master_dataset(filepath: Optional[Path] = None, min_minutes: int = DEFAULT_MIN_MINUTES) -> pd.DataFrame:
    """
    Loads the master player dataset from disk and filters by minimum minutes played.
    """
    path = filepath or PROCESSED_DATA_PATH
    if not path.exists():
        raise FileNotFoundError(f"Master dataset not found at {path}. Run dataset generator first.")
        
    df = pd.read_csv(path)
    df = normalize_player_dataframe(df, min_minutes=min_minutes)
    
    # Map raw position codes to granular position cohorts if not present
    if "position_group" not in df.columns:
        df["position_group"] = df["position"].apply(lambda p: _map_to_cohort(str(p)))
        
    return df


def _map_to_cohort(pos_str: str) -> str:
    """
    Maps fine-grained position strings to 6 standard positional cohorts matching pro scouting standards:
    - Goalkeeper (GK)
    - Centreback (CB)
    - Fullback / Wingback (FB / WB / LB / RB)
    - Central / Defensive Midfielder (CM / DM)
    - Winger / Attacking Mid (W / AM / RW / LW)
    - Centre-Forward / Striker (ST / CF / FW)
    """
    p = pos_str.upper().strip()
    if "GK" in p:
        return "Goalkeeper"
    elif "CB" in p:
        return "Centreback"
    elif "FB" in p or "WB" in p or "LB" in p or "RB" in p:
        return "Fullback / Wingback"
    elif "DM" in p or "CM" in p or p == "MF":
        return "Central / Defensive Midfielder"
    elif "AM" in p or "RW" in p or "LW" in p or "W" in p:
        return "Winger / Attacking Mid"
    elif "ST" in p or "CF" in p or "FW" in p:
        return "Centre-Forward / Striker"
    elif "DF" in p:
        return "Centreback"
    return "Central / Defensive Midfielder"


def get_player_profile(df: pd.DataFrame, player_name: str, season: Optional[str] = None) -> Optional[pd.Series]:
    """Finds a specific player record by exact name or substring match."""
    filtered = df[df["player"].str.lower() == player_name.lower()]
    if filtered.empty:
        filtered = df[df["player"].str.contains(player_name, case=False, na=False)]
    if season and "season" in df.columns:
        filtered = filtered[filtered["season"] == season]
    if filtered.empty:
        return None
    return filtered.iloc[0]


def get_cohort_peers(df: pd.DataFrame, position_group: str, league: Optional[str] = None, season: Optional[str] = None) -> pd.DataFrame:
    """Returns all player records belonging to the same positional cohort and season."""
    cohort = df[df["position_group"] == position_group].copy()
    if season and "season" in cohort.columns:
        cohort = cohort[cohort["season"] == season]
    if league and league != "All Leagues" and "league" in cohort.columns:
        cohort = cohort[cohort["league"] == league]
    return cohort
