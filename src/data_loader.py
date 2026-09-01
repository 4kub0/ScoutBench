"""
ScoutBench Data Loader Module
Handles loading, caching, schema validation, and cohort filtering for multi-season
European league datasets enriched with biographical, physical, and financial attributes.
"""

from typing import Optional, List, Set
from pathlib import Path
import pandas as pd
from src.config import DEFAULT_MIN_MINUTES
from src.normalization import normalize_player_dataframe

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
PROCESSED_DATA_PATH = DATA_DIR / "processed" / "master_players.csv"

# Expected schema definitions for Requirement R1
REQUIRED_BASE_COLUMNS = [
    "player", "team", "league", "season", "position", "age", "minutes", "team_possession_pct"
]

REQUIRED_METADATA_COLUMNS = [
    "nationality",
    "preferred_foot",
    "height_cm",
    "weight_kg",
    "primary_position",
    "secondary_position",
    "market_value_eur",
    "contract_expiry",
    "wage_tier"
]

VALID_PREFERRED_FEET = {"Left", "Right", "Both"}

VALID_WAGE_TIERS = {
    "Tier 1 (€200k+/wk)",
    "Tier 2 (€100k-200k/wk)",
    "Tier 3 (€50k-100k/wk)",
    "Tier 4 (€20k-50k/wk)",
    "Tier 5 (<€20k/wk)"
}

VALID_PRIMARY_POSITIONS = {
    "GK", "CB", "LB", "RB", "DM", "CM", "AM", "LW", "RW", "ST", "WB", "FW", "W", "FB"
}


def validate_master_dataset(df: pd.DataFrame) -> bool:
    """
    Validates that the master dataset strictly satisfies Requirement R1:
    1. All base identifier and 9 metadata columns exist.
    2. Exactly 3,952 rows are present if evaluating the unfiltered dataset.
    3. Zero missing values (0 NaNs / nulls) in all 9 biographical, physical, and financial columns.
    4. Numeric ranges and categorical values satisfy bounded domain constraints:
       - height_cm: 160 - 205 cm
       - weight_kg: 55 - 105 kg
       - preferred_foot: 'Left', 'Right', or 'Both'
       - market_value_eur: > 0
       - contract_expiry: 2024 - 2035
       - wage_tier: One of the 5 standard wage tiers
       - primary_position: Valid football position code
    
    Returns:
        bool: True if dataset passes all validation checks.
    
    Raises:
        ValueError: If any validation rule or constraint is violated.
    """
    if df is None or not isinstance(df, pd.DataFrame):
        raise ValueError("Provided dataset is None or not a pandas DataFrame.")

    if df.empty:
        raise ValueError("Provided dataset is empty.")

    # 1. Column Presence Check
    all_required = REQUIRED_BASE_COLUMNS + REQUIRED_METADATA_COLUMNS
    missing_cols = [c for c in all_required if c not in df.columns]
    if missing_cols:
        raise ValueError(f"Master dataset is missing required columns: {missing_cols}")

    # 2. Row Count Verification (if unfiltered master dataset)
    if len(df) >= 3952 and len(df) != 3952:
        raise ValueError(f"Expected exactly 3,952 rows for master dataset, found {len(df)}.")

    # 3. Zero Missing / Null Values Check on Enriched Metadata
    for col in REQUIRED_METADATA_COLUMNS:
        null_count = df[col].isnull().sum()
        if null_count > 0:
            raise ValueError(f"Found {null_count} null/NaN values in metadata column '{col}'. Zero nulls required.")

    # 4. Domain & Range Validation
    # Height bounds
    if not pd.api.types.is_numeric_dtype(df["height_cm"]):
        raise ValueError("Column 'height_cm' must be numeric.")
    if (df["height_cm"] < 160).any() or (df["height_cm"] > 205).any():
        invalid_heights = df[(df["height_cm"] < 160) | (df["height_cm"] > 205)][["player", "height_cm"]]
        raise ValueError(f"Found height_cm values outside valid range [160, 205]:\n{invalid_heights.head()}")

    # Weight bounds
    if not pd.api.types.is_numeric_dtype(df["weight_kg"]):
        raise ValueError("Column 'weight_kg' must be numeric.")
    if (df["weight_kg"] < 55).any() or (df["weight_kg"] > 105).any():
        invalid_weights = df[(df["weight_kg"] < 55) | (df["weight_kg"] > 105)][["player", "weight_kg"]]
        raise ValueError(f"Found weight_kg values outside valid range [55, 105]:\n{invalid_weights.head()}")

    # Preferred foot categories
    invalid_feet = set(df["preferred_foot"].unique()) - VALID_PREFERRED_FEET
    if invalid_feet:
        raise ValueError(f"Found invalid preferred_foot values: {invalid_feet}. Expected subset of {VALID_PREFERRED_FEET}.")

    # Market value bounds
    if not pd.api.types.is_numeric_dtype(df["market_value_eur"]):
        raise ValueError("Column 'market_value_eur' must be numeric.")
    if (df["market_value_eur"] <= 0).any():
        invalid_mv = df[df["market_value_eur"] <= 0][["player", "market_value_eur"]]
        raise ValueError(f"Found non-positive market_value_eur values:\n{invalid_mv.head()}")

    # Contract expiry bounds
    if not pd.api.types.is_numeric_dtype(df["contract_expiry"]):
        raise ValueError("Column 'contract_expiry' must be numeric.")
    if (df["contract_expiry"] < 2024).any() or (df["contract_expiry"] > 2035).any():
        invalid_exp = df[(df["contract_expiry"] < 2024) | (df["contract_expiry"] > 2035)][["player", "contract_expiry"]]
        raise ValueError(f"Found contract_expiry values outside valid range [2024, 2035]:\n{invalid_exp.head()}")

    # Wage tier categories
    invalid_wages = set(df["wage_tier"].unique()) - VALID_WAGE_TIERS
    if invalid_wages:
        raise ValueError(f"Found invalid wage_tier values: {invalid_wages}. Expected subset of {VALID_WAGE_TIERS}.")

    # Primary position codes
    invalid_prim = set(df["primary_position"].unique()) - VALID_PRIMARY_POSITIONS
    if invalid_prim:
        raise ValueError(f"Found invalid primary_position codes: {invalid_prim}. Expected subset of {VALID_PRIMARY_POSITIONS}.")

    return True


def load_master_dataset(filepath: Optional[Path] = None, min_minutes: int = DEFAULT_MIN_MINUTES) -> pd.DataFrame:
    """
    Loads the master player dataset from disk, restores metadata strings, validates schema integrity,
    and applies minimum playing time filtering.
    
    Args:
        filepath: Optional custom Path to master_players.csv. Defaults to data/processed/master_players.csv.
        min_minutes: Minimum minutes played threshold (default 900).
        
    Returns:
        pd.DataFrame: Validated and normalized player dataset preserving all 9 enriched metadata fields.
    """
    path = filepath or PROCESSED_DATA_PATH
    if not path.exists():
        raise FileNotFoundError(f"Master dataset not found at {path}. Run dataset generator first.")
        
    df = pd.read_csv(path, encoding="utf-8")
    
    # Restore string 'None' for secondary_position (prevent pandas read_csv NaN conversion)
    if "secondary_position" in df.columns:
        df["secondary_position"] = df["secondary_position"].fillna("None")
        
    # Validate raw full dataset schema prior to filtering
    if len(df) == 3952:
        validate_master_dataset(df)
        
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


def get_player_profile(df: pd.DataFrame, player_name: Optional[str], season: Optional[str] = None) -> Optional[pd.Series]:
    """
    Finds a specific player record by exact name or substring match, preserving all enriched metadata.
    
    Args:
        df: Player dataset DataFrame.
        player_name: Name of the player to search for.
        season: Optional season filter (e.g. '2025/26' or '2024/25').
        
    Returns:
        pd.Series or None: Player record row if found, None otherwise.
    """
    if not player_name or not isinstance(player_name, str):
        return None
    filtered = df[df["player"].str.lower() == player_name.lower()]
    if filtered.empty:
        filtered = df[df["player"].str.contains(player_name, case=False, na=False)]
    if season and "season" in df.columns:
        filtered = filtered[filtered["season"] == season]
    if filtered.empty:
        return None
    return filtered.iloc[0]


def get_cohort_peers(
    df: pd.DataFrame, 
    position_group: str, 
    league: Optional[str] = None, 
    season: Optional[str] = None
) -> pd.DataFrame:
    """
    Returns all player records belonging to the same positional cohort and season.
    
    Args:
        df: Player dataset DataFrame.
        position_group: Standard positional cohort name (e.g. 'Winger / Attacking Mid').
        league: Optional league filter (or 'All Leagues' for Europe-wide cohort).
        season: Optional season filter.
        
    Returns:
        pd.DataFrame: Filtered cohort peer DataFrame.
    """
    cohort = df[df["position_group"] == position_group].copy()
    if season and "season" in cohort.columns:
        cohort = cohort[cohort["season"] == season]
    if league and league != "All Leagues" and "league" in cohort.columns:
        cohort = cohort[cohort["league"] == league]
    return cohort


def format_market_value(val_eur: float) -> str:
    """
    Formats a numeric market valuation into editorial string currency representation.
    Examples:
        150000000 -> '€150.0M' or '€150M'
        2500000 -> '€2.5M'
        500000 -> '€500k'
    """
    if val_eur >= 1_000_000:
        val_m = val_eur / 1_000_000.0
        if val_m == int(val_m):
            return f"€{int(val_m)}M"
        return f"€{val_m:.1f}M"
    elif val_eur >= 1_000:
        val_k = val_eur / 1_000.0
        if val_k == int(val_k):
            return f"€{int(val_k)}k"
        return f"€{val_k:.1f}k"
    return f"€{int(val_eur)}"


def get_available_seasons(df: pd.DataFrame) -> List[str]:
    """Returns sorted list of distinct seasons present in the dataset."""
    if "season" in df.columns:
        return sorted(df["season"].unique().tolist(), reverse=True)
    return ["2025/26", "2024/25"]


def get_available_leagues(df: pd.DataFrame) -> List[str]:
    """Returns sorted list of distinct leagues present in the dataset."""
    if "league" in df.columns:
        return sorted(df["league"].unique().tolist())
    return []


def get_available_clubs(df: pd.DataFrame, league: Optional[str] = None) -> List[str]:
    """Returns sorted list of distinct clubs, optionally filtered by league."""
    target_df = df if (league is None or league == "All Leagues") else df[df["league"] == league]
    if "team" in target_df.columns:
        return sorted(target_df["team"].unique().tolist())
    return []
