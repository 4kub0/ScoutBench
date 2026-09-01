"""
ScoutBench Data Loader & Metadata Pipeline Unit Tests
Comprehensive tests for:
- Master dataset loading and schema integrity
- Zero-null validation across all 3,952 player-season records
- Range and domain validation for all 9 biographical, physical, and financial attributes
- Temporal consistency between 2024/25 and 2025/26
- Player search and cohort peer filtering
"""

import unittest
import pandas as pd
import numpy as np
from pathlib import Path
from src.data_loader import (
    load_master_dataset,
    validate_master_dataset,
    get_player_profile,
    get_cohort_peers,
    format_market_value,
    get_available_seasons,
    get_available_leagues,
    get_available_clubs,
    REQUIRED_METADATA_COLUMNS,
    REQUIRED_BASE_COLUMNS,
    VALID_PREFERRED_FEET,
    VALID_WAGE_TIERS,
    VALID_PRIMARY_POSITIONS,
    PROCESSED_DATA_PATH
)


class TestDataLoaderAndMetadataPipeline(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Load the raw unfiltered dataset and default filtered dataset
        cls.raw_df = pd.read_csv(PROCESSED_DATA_PATH, encoding="utf-8")
        if "secondary_position" in cls.raw_df.columns:
            cls.raw_df["secondary_position"] = cls.raw_df["secondary_position"].fillna("None")
        cls.df = load_master_dataset(min_minutes=0)
        cls.filtered_df = load_master_dataset(min_minutes=900)

    def test_dataset_dimensions_and_seasons(self):
        """Verify exactly 3,952 rows across dual seasons (1,976 each)."""
        self.assertEqual(len(self.raw_df), 3952)
        season_counts = self.raw_df["season"].value_counts().to_dict()
        self.assertEqual(season_counts.get("2025/26"), 1976)
        self.assertEqual(season_counts.get("2024/25"), 1976)

    def test_schema_columns_presence(self):
        """Verify presence of all required base identifiers and 9 enriched metadata fields."""
        for col in REQUIRED_BASE_COLUMNS:
            self.assertIn(col, self.df.columns, f"Missing base identifier column: {col}")
        for col in REQUIRED_METADATA_COLUMNS:
            self.assertIn(col, self.df.columns, f"Missing enriched metadata column: {col}")

    def test_zero_nulls_in_all_metadata_columns(self):
        """Assert 0 nulls across all 3,952 rows for every metadata column."""
        for col in REQUIRED_METADATA_COLUMNS:
            null_count = self.df[col].isnull().sum()
            self.assertEqual(null_count, 0, f"Found {null_count} nulls in '{col}' across 3,952 rows.")

    def test_validate_master_dataset_passes_on_genuine_dataset(self):
        """Verify validate_master_dataset returns True on the official dataset."""
        result = validate_master_dataset(self.df)
        self.assertTrue(result)

    def test_validate_master_dataset_rejects_none_or_empty(self):
        """Verify validation failure for None or empty inputs."""
        with self.assertRaises(ValueError):
            validate_master_dataset(None)
        with self.assertRaises(ValueError):
            validate_master_dataset(pd.DataFrame())

    def test_validate_master_dataset_rejects_missing_column(self):
        """Verify validation failure when a required column is removed."""
        corrupted_df = self.df.drop(columns=["nationality"]).copy()
        with self.assertRaises(ValueError) as ctx:
            validate_master_dataset(corrupted_df)
        self.assertIn("missing required columns", str(ctx.exception).lower())

    def test_validate_master_dataset_rejects_nulls(self):
        """Verify validation failure when NaNs exist in a metadata column."""
        corrupted_df = self.df.copy()
        corrupted_df.loc[0, "preferred_foot"] = np.nan
        with self.assertRaises(ValueError) as ctx:
            validate_master_dataset(corrupted_df)
        self.assertIn("null/nan values", str(ctx.exception).lower())

    def test_validate_master_dataset_rejects_out_of_range_height(self):
        """Verify validation failure for unrealistic heights (<160 or >205 cm)."""
        corrupted_df = self.df.copy()
        corrupted_df.loc[0, "height_cm"] = 150
        with self.assertRaises(ValueError) as ctx:
            validate_master_dataset(corrupted_df)
        self.assertIn("height_cm", str(ctx.exception))

    def test_validate_master_dataset_rejects_out_of_range_weight(self):
        """Verify validation failure for unrealistic weights (<55 or >105 kg)."""
        corrupted_df = self.df.copy()
        corrupted_df.loc[0, "weight_kg"] = 120
        with self.assertRaises(ValueError) as ctx:
            validate_master_dataset(corrupted_df)
        self.assertIn("weight_kg", str(ctx.exception))

    def test_validate_master_dataset_rejects_invalid_foot(self):
        """Verify validation failure for non-standard preferred foot strings."""
        corrupted_df = self.df.copy()
        corrupted_df.loc[0, "preferred_foot"] = "UnknownFoot"
        with self.assertRaises(ValueError) as ctx:
            validate_master_dataset(corrupted_df)
        self.assertIn("preferred_foot", str(ctx.exception))

    def test_validate_master_dataset_rejects_non_positive_market_value(self):
        """Verify validation failure for zero or negative market valuations."""
        corrupted_df = self.df.copy()
        corrupted_df.loc[0, "market_value_eur"] = 0
        with self.assertRaises(ValueError) as ctx:
            validate_master_dataset(corrupted_df)
        self.assertIn("market_value_eur", str(ctx.exception))

    def test_validate_master_dataset_rejects_invalid_wage_tier(self):
        """Verify validation failure for unregistered wage tiers."""
        corrupted_df = self.df.copy()
        corrupted_df.loc[0, "wage_tier"] = "Tier X (Super Max)"
        with self.assertRaises(ValueError) as ctx:
            validate_master_dataset(corrupted_df)
        self.assertIn("wage_tier", str(ctx.exception))

    def test_validate_master_dataset_rejects_invalid_primary_position(self):
        """Verify validation failure for illegal primary position codes."""
        corrupted_df = self.df.copy()
        corrupted_df.loc[0, "primary_position"] = "QUARTERBACK"
        with self.assertRaises(ValueError) as ctx:
            validate_master_dataset(corrupted_df)
        self.assertIn("primary_position", str(ctx.exception))

    def test_temporal_consistency_between_seasons(self):
        """
        Verify physical DNA invariance and logical age/valuation evolution
        for the same player across 2024/25 and 2025/26.
        """
        s25 = self.df[self.df["season"] == "2025/26"].set_index(["player", "team"])
        s24 = self.df[self.df["season"] == "2024/25"].set_index(["player", "team"])

        common_keys = s25.index.intersection(s24.index)
        self.assertEqual(len(common_keys), 1976)

        # Invariant physical DNA
        for key in common_keys:
            r25 = s25.loc[key]
            r24 = s24.loc[key]

            # Invariant fields
            self.assertEqual(r25["nationality"], r24["nationality"])
            self.assertEqual(r25["preferred_foot"], r24["preferred_foot"])
            self.assertEqual(r25["height_cm"], r24["height_cm"])
            self.assertEqual(r25["weight_kg"], r24["weight_kg"])
            self.assertEqual(r25["primary_position"], r24["primary_position"])

            # Age increments by 1
            self.assertEqual(r25["age"], r24["age"] + 1)

            # Contract expiry within valid ranges
            self.assertGreaterEqual(r25["contract_expiry"], 2026)
            self.assertLessEqual(r25["contract_expiry"], 2035)
            self.assertGreaterEqual(r24["contract_expiry"], 2024)

            # Market valuation is positive
            self.assertGreater(r25["market_value_eur"], 0)
            self.assertGreater(r24["market_value_eur"], 0)

    def test_ground_truth_superstar_profiles(self):
        """Verify exact ground truth calibration for prominent world stars."""
        # Lamine Yamal (Barcelona)
        yamal = get_player_profile(self.df, "Lamine Yamal", season="2025/26")
        self.assertIsNotNone(yamal)
        self.assertEqual(yamal["nationality"], "Spain")
        self.assertEqual(yamal["preferred_foot"], "Left")
        self.assertEqual(yamal["height_cm"], 180)
        self.assertEqual(yamal["weight_kg"], 68)
        self.assertEqual(yamal["primary_position"], "RW")
        self.assertEqual(yamal["secondary_position"], "LW")
        self.assertEqual(yamal["market_value_eur"], 150_000_000)
        self.assertEqual(yamal["contract_expiry"], 2031)
        self.assertEqual(yamal["wage_tier"], "Tier 1 (€200k+/wk)")

        # Erling Haaland (Manchester City)
        haaland = get_player_profile(self.df, "Erling Haaland", season="2025/26")
        self.assertIsNotNone(haaland)
        self.assertEqual(haaland["nationality"], "Norway")
        self.assertEqual(haaland["preferred_foot"], "Left")
        self.assertEqual(haaland["height_cm"], 194)
        self.assertEqual(haaland["weight_kg"], 88)
        self.assertEqual(haaland["primary_position"], "ST")
        self.assertEqual(haaland["market_value_eur"], 200_000_000)

        # Rodri (Manchester City)
        rodri = get_player_profile(self.df, "Rodri", season="2025/26")
        self.assertIsNotNone(rodri)
        self.assertEqual(rodri["nationality"], "Spain")
        self.assertEqual(rodri["preferred_foot"], "Right")
        self.assertEqual(rodri["height_cm"], 191)
        self.assertEqual(rodri["weight_kg"], 82)
        self.assertEqual(rodri["primary_position"], "DM")
        self.assertEqual(rodri["market_value_eur"], 130_000_000)

        # Kylian Mbappe (Real Madrid)
        mbappe = get_player_profile(self.df, "Kylian Mbappe", season="2025/26")
        self.assertIsNotNone(mbappe)
        self.assertEqual(mbappe["nationality"], "France")
        self.assertEqual(mbappe["primary_position"], "ST")
        self.assertEqual(mbappe["market_value_eur"], 180_000_000)

        # Harry Kane (Bayern Munich)
        kane = get_player_profile(self.df, "Harry Kane", season="2025/26")
        self.assertIsNotNone(kane)
        self.assertEqual(kane["nationality"], "England")
        self.assertEqual(kane["primary_position"], "ST")
        self.assertEqual(kane["market_value_eur"], 100_000_000)

        # Florian Wirtz (Bayer Leverkusen)
        wirtz = get_player_profile(self.df, "Florian Wirtz", season="2025/26")
        self.assertIsNotNone(wirtz)
        self.assertEqual(wirtz["nationality"], "Germany")
        self.assertEqual(wirtz["primary_position"], "AM")
        self.assertEqual(wirtz["market_value_eur"], 130_000_000)

    def test_get_player_profile_edge_cases(self):
        """Test get_player_profile with partial match, non-existent, and empty inputs."""
        # Partial match
        prof = get_player_profile(self.df, "Yamal")
        self.assertIsNotNone(prof)
        self.assertIn("Lamine Yamal", prof["player"])

        # Case insensitive
        prof_lower = get_player_profile(self.df, "lamine yamal")
        self.assertIsNotNone(prof_lower)
        self.assertEqual(prof_lower["player"], "Lamine Yamal")

        # Non-existent
        none_prof = get_player_profile(self.df, "NonExistentPlayer12345")
        self.assertIsNone(none_prof)

        # None input
        self.assertIsNone(get_player_profile(self.df, None))
        self.assertIsNone(get_player_profile(self.df, ""))

    def test_min_minutes_filtering(self):
        """Verify load_master_dataset filters out rows below min_minutes."""
        self.assertTrue((self.filtered_df["minutes"] >= 900).all())
        self.assertLessEqual(len(self.filtered_df), len(self.df))

    def test_load_master_dataset_file_not_found(self):
        """Verify load_master_dataset raises FileNotFoundError for missing path."""
        fake_path = Path("data/processed/non_existent_file.csv")
        with self.assertRaises(FileNotFoundError):
            load_master_dataset(filepath=fake_path)

    def test_get_cohort_peers_filtering(self):
        """Verify cohort peer filtering works correctly across cohorts and leagues."""
        peers = get_cohort_peers(self.df, "Winger / Attacking Mid", league="La Liga", season="2025/26")
        self.assertFalse(peers.empty)
        self.assertTrue((peers["position_group"] == "Winger / Attacking Mid").all())
        self.assertTrue((peers["league"] == "La Liga").all())
        self.assertTrue((peers["season"] == "2025/26").all())

    def test_format_market_value(self):
        """Verify currency formatting helper."""
        self.assertEqual(format_market_value(150_000_000), "€150M")
        self.assertEqual(format_market_value(2_500_000), "€2.5M")
        self.assertEqual(format_market_value(500_000), "€500k")
        self.assertEqual(format_market_value(750), "€750")

    def test_available_helpers(self):
        """Verify season, league, and club helper extraction functions."""
        seasons = get_available_seasons(self.df)
        self.assertIn("2025/26", seasons)
        self.assertIn("2024/25", seasons)

        leagues = get_available_leagues(self.df)
        self.assertEqual(len(leagues), 5)
        self.assertIn("La Liga", leagues)
        self.assertIn("Premier League", leagues)

        clubs = get_available_clubs(self.df, league="La Liga")
        self.assertEqual(len(clubs), 20)
        self.assertIn("Barcelona", clubs)
        self.assertIn("Real Madrid", clubs)


if __name__ == "__main__":
    unittest.main()
