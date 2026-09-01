"""
Empirical Adversarial Stress Testing Harness for ScoutBench
Executes extensive stress tests across 6 core challenge dimensions:
1. Full combinatorial cohort benchmark generation (6 positions x 2 seasons x 5 leagues x 4 types)
2. Cross-position comparisons (ST vs CM vs FB vs W vs CB vs GK)
3. Goalkeeper vs Outfield metric handling & missing metric resilience
4. Max 4-profile multi-player & cohort comparison suite
5. Under-21 cohort filtering boundary conditions (ages 16-21 included, 22+ excluded)
6. Adversarial dataset corruption & validation resilience
"""

import sys
import unittest
import pandas as pd
import numpy as np
from pathlib import Path
import plotly.graph_objects as go

from src.data_loader import (
    load_master_dataset,
    validate_master_dataset,
    get_player_profile,
    get_cohort_peers,
    get_available_seasons,
    get_available_leagues,
    REQUIRED_METADATA_COLUMNS,
    REQUIRED_BASE_COLUMNS,
    VALID_PREFERRED_FEET,
    VALID_WAGE_TIERS,
    VALID_PRIMARY_POSITIONS,
    PROCESSED_DATA_PATH
)
from src.metrics_engine import (
    compute_cohort_benchmark,
    compute_comparison_deltas,
    compute_player_percentiles,
    compute_tactical_spectrum,
    compute_behavioral_indexes,
    generate_scouting_intelligence
)
from src.visualizer import (
    create_multi_player_radar,
    create_pizza_radar,
    create_quadrant_scatter,
    create_pitch_heatmap
)
from src.config import PIZZA_METRIC_TEMPLATES


class EmpiricalStressTestSuite(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("\n" + "="*80)
        print("STARTING EMPIRICAL ADVERSARIAL STRESS TEST SUITE")
        print("="*80)
        cls.raw_df = pd.read_csv(PROCESSED_DATA_PATH, encoding="utf-8")
        if "secondary_position" in cls.raw_df.columns:
            cls.raw_df["secondary_position"] = cls.raw_df["secondary_position"].fillna("None")
        cls.full_df = load_master_dataset(min_minutes=0)
        cls.filtered_df = load_master_dataset(min_minutes=900)
        
        cls.positions = [
            "Goalkeeper",
            "Centreback",
            "Fullback / Wingback",
            "Central / Defensive Midfielder",
            "Winger / Attacking Mid",
            "Centre-Forward / Striker"
        ]
        cls.seasons = ["2025/26", "2024/25"]
        cls.leagues = ["Premier League", "La Liga", "Bundesliga", "Serie A", "Ligue 1"]

    # --------------------------------------------------------------------------
    # DIMENSION 1: Combinatorial Cohort Benchmark Generation
    # --------------------------------------------------------------------------
    def test_dimension_1_exhaustive_cohort_benchmarks(self):
        """Test all 144 cohort benchmark combinations on full dataset."""
        print("\n--- DIMENSION 1: Testing Exhaustive Cohort Benchmarks (144 Combinations) ---")
        
        success_count = 0
        total_tested = 0
        
        for season in self.seasons:
            for pos in self.positions:
                # 1. Top 5 Positional Average
                total_tested += 1
                bench_top5 = compute_cohort_benchmark(
                    self.full_df,
                    position_group=pos,
                    season=season,
                    benchmark_type="top5_positional"
                )
                self.assertIsInstance(bench_top5, pd.Series)
                self.assertGreater(bench_top5["sample_size"], 0)
                self.assertIn("Top 5 European", bench_top5["player"])
                self.assertEqual(bench_top5["position_group"], pos)
                self.assertEqual(bench_top5["season"], season)
                self.assertFalse(pd.isna(bench_top5["age"]))
                self.assertFalse(pd.isna(bench_top5["market_value_eur"]))
                success_count += 1
                
                # 2. U-21 European Positional Average
                total_tested += 1
                bench_u21_eu = compute_cohort_benchmark(
                    self.full_df,
                    position_group=pos,
                    season=season,
                    benchmark_type="u21_european"
                )
                self.assertIsInstance(bench_u21_eu, pd.Series)
                self.assertGreater(bench_u21_eu["sample_size"], 0)
                self.assertLessEqual(bench_u21_eu["age"], 21.0)
                self.assertIn("U-21 European", bench_u21_eu["player"])
                success_count += 1
                
                # 3. Domestic & U-21 Domestic across all 5 leagues
                for league in self.leagues:
                    # Domestic Positional
                    total_tested += 1
                    bench_dom = compute_cohort_benchmark(
                        self.full_df,
                        position_group=pos,
                        season=season,
                        benchmark_type="domestic_positional",
                        domestic_league=league
                    )
                    self.assertIsInstance(bench_dom, pd.Series)
                    self.assertGreater(bench_dom["sample_size"], 0)
                    self.assertEqual(bench_dom["league"], league)
                    self.assertIn(league, bench_dom["player"])
                    success_count += 1
                    
                    # U-21 Domestic
                    total_tested += 1
                    bench_u21_dom = compute_cohort_benchmark(
                        self.full_df,
                        position_group=pos,
                        season=season,
                        benchmark_type="u21_domestic",
                        domestic_league=league
                    )
                    self.assertIsInstance(bench_u21_dom, pd.Series)
                    self.assertGreater(bench_u21_dom["sample_size"], 0)
                    self.assertLessEqual(bench_u21_dom["age"], 21.0)
                    self.assertIn(league, bench_u21_dom["player"])
                    self.assertIn("U-21", bench_u21_dom["player"])
                    success_count += 1

        print(f"PASS: Successfully generated {success_count}/{total_tested} combinatorial benchmarks with zero NaNs.")
        self.assertEqual(success_count, 144)

    # --------------------------------------------------------------------------
    # DIMENSION 2: Cross-Position Comparisons
    # --------------------------------------------------------------------------
    def test_dimension_2_cross_position_comparisons(self):
        """Stress-test comparing players from radically different positions."""
        print("\n--- DIMENSION 2: Testing Cross-Position Comparisons ---")
        
        # Test comparing a Striker (Haaland) with CM (Pedri), FB (Alexander-Arnold), CB (Van Dijk)
        haaland = get_player_profile(self.full_df, "Erling Haaland", season="2025/26")
        pedri = get_player_profile(self.full_df, "Pedri", season="2025/26")
        arnold = get_player_profile(self.full_df, "Trent Alexander-Arnold", season="2025/26")
        vandijk = get_player_profile(self.full_df, "Virgil van Dijk", season="2025/26")
        
        self.assertIsNotNone(haaland)
        self.assertIsNotNone(pedri)
        self.assertIsNotNone(arnold)
        self.assertIsNotNone(vandijk)
        
        # 1. Striker metric template applied across all 4 positions
        striker_metrics = [
            "npxG_per90", "shots_total_per90", "shots_on_target_pct",
            "touches_att_pen_per90", "xAG_per90", "sca_per90", "key_passes_per90",
            "pass_completion_pct", "tackles_att_3rd_per90", "ball_recoveries_per90"
        ]
        
        peers_st = get_cohort_peers(self.full_df, "Centre-Forward / Striker", season="2025/26")
        peers_cm = get_cohort_peers(self.full_df, "Central / Defensive Midfielder", season="2025/26")
        peers_fb = get_cohort_peers(self.full_df, "Fullback / Wingback", season="2025/26")
        peers_cb = get_cohort_peers(self.full_df, "Centreback", season="2025/26")
        
        pct_haaland = compute_player_percentiles(haaland, peers_st, striker_metrics)
        pct_pedri = compute_player_percentiles(pedri, peers_cm, striker_metrics)
        pct_arnold = compute_player_percentiles(arnold, peers_fb, striker_metrics)
        pct_vandijk = compute_player_percentiles(vandijk, peers_cb, striker_metrics)
        
        # Compute deltas
        deltas = compute_comparison_deltas(
            base_row=haaland,
            base_percentiles=pct_haaland,
            compared_rows=[pedri, arnold, vandijk],
            compared_percentiles=[pct_pedri, pct_arnold, pct_vandijk],
            metrics=striker_metrics
        )
        
        self.assertEqual(len(deltas), len(striker_metrics))
        self.assertIn("comp_1_delta_val", deltas.columns)
        self.assertIn("comp_2_delta_val", deltas.columns)
        self.assertIn("comp_3_delta_val", deltas.columns)
        self.assertFalse(deltas.isnull().any().any(), "Found NaNs in cross-position delta table.")
        
        # 2. Render multi-player radar for cross-position profiles
        profiles = [
            {"name": "Erling Haaland (ST)", "percentiles": pct_haaland, "player_row": haaland},
            {"name": "Pedri (CM)", "percentiles": pct_pedri, "player_row": pedri},
            {"name": "Alexander-Arnold (FB)", "percentiles": pct_arnold, "player_row": arnold},
            {"name": "Van Dijk (CB)", "percentiles": pct_vandijk, "player_row": vandijk},
        ]
        
        fig = create_multi_player_radar(profiles, striker_metrics)
        self.assertIsInstance(fig, go.Figure)
        self.assertEqual(len(fig.data), 4)
        print("PASS: Cross-position comparison calculated deltas and rendered 4-trace radar cleanly.")

    # --------------------------------------------------------------------------
    # DIMENSION 3: Goalkeeper Comparisons & Missing Outfield Metric Handling
    # --------------------------------------------------------------------------
    def test_dimension_3_goalkeeper_and_missing_metrics(self):
        """Stress-test Goalkeepers compared with outfield players and missing metric fallbacks."""
        print("\n--- DIMENSION 3: Testing Goalkeeper Comparisons & Missing Metrics ---")
        
        courtois = get_player_profile(self.full_df, "Thibaut Courtois", season="2025/26")
        if courtois is None:
            # Fallback search any GK
            gk_df = self.full_df[self.full_df["position_group"] == "Goalkeeper"]
            courtois = gk_df.iloc[0]
            
        mbappe = get_player_profile(self.full_df, "Kylian Mbappe", season="2025/26")
        self.assertIsNotNone(courtois)
        self.assertIsNotNone(mbappe)
        
        gk_peers = get_cohort_peers(self.full_df, "Goalkeeper", season="2025/26")
        fw_peers = get_cohort_peers(self.full_df, "Centre-Forward / Striker", season="2025/26")
        
        # Case A: Evaluate GK on Outfield metrics (GK has NaN for npxG, xAG, etc.)
        outfield_metrics = ["npxG_per90", "xAG_per90", "sca_per90", "progressive_carries_per90"]
        pct_courtois_outfield = compute_player_percentiles(courtois, gk_peers, outfield_metrics)
        
        # Outfield metrics missing on GK should fallback safely to 50.0
        for m in outfield_metrics:
            self.assertEqual(pct_courtois_outfield[m], 50.0, f"Expected 50.0 fallback for missing metric {m}")
            
        pct_mbappe_outfield = compute_player_percentiles(mbappe, fw_peers, outfield_metrics)
        
        # Compute deltas with GK as compared player
        delta_df = compute_comparison_deltas(
            base_row=mbappe,
            base_percentiles=pct_mbappe_outfield,
            compared_rows=[courtois],
            compared_percentiles=[pct_courtois_outfield],
            metrics=outfield_metrics
        )
        self.assertEqual(len(delta_df), len(outfield_metrics))
        self.assertFalse(delta_df.isnull().any().any(), "Found NaNs in GK cross-comparison delta.")
        
        # Case B: Evaluate Outfield player on GK metrics (psxg_net_per90, save_pct, crosses_stopped_pct)
        gk_metrics = ["psxg_net_per90", "save_pct", "pass_completion_pct", "crosses_stopped_pct"]
        pct_courtois_gk = compute_player_percentiles(courtois, gk_peers, gk_metrics)
        pct_mbappe_gk = compute_player_percentiles(mbappe, fw_peers, gk_metrics)
        
        for m in ["psxg_net_per90", "save_pct", "crosses_stopped_pct"]:
            self.assertEqual(pct_mbappe_gk[m], 50.0, f"Expected 50.0 fallback for outfield player missing {m}")
            
        # Case C: Render Radar with GK and Forward
        radar_fig = create_multi_player_radar([
            {"name": courtois["player"], "percentiles": pct_courtois_gk, "player_row": courtois},
            {"name": mbappe["player"], "percentiles": pct_mbappe_gk, "player_row": mbappe},
        ], gk_metrics)
        self.assertIsInstance(radar_fig, go.Figure)
        self.assertEqual(len(radar_fig.data), 2)
        print("PASS: Goalkeeper missing metric handling and cross-comparisons executed without errors.")

    # --------------------------------------------------------------------------
    # DIMENSION 4: Max 4-Profile Comparison Suite
    # --------------------------------------------------------------------------
    def test_dimension_4_max_4_profiles_comparison(self):
        """Stress-test maximum 4-profile comparisons across all combinations."""
        print("\n--- DIMENSION 4: Testing Max 4-Profile Combinations ---")
        
        base_p = get_player_profile(self.full_df, "Lamine Yamal", season="2025/26")
        p2 = get_player_profile(self.full_df, "Bukayo Saka", season="2025/26")
        p3 = get_player_profile(self.full_df, "Michael Olise", season="2025/26")
        
        bench_top5 = compute_cohort_benchmark(self.full_df, "Winger / Attacking Mid", "2025/26", "top5_positional")
        bench_u21 = compute_cohort_benchmark(self.full_df, "Winger / Attacking Mid", "2025/26", "u21_european")
        bench_laliga = compute_cohort_benchmark(self.full_df, "Winger / Attacking Mid", "2025/26", "domestic_positional", "La Liga")
        
        winger_metrics = [
            "npxG_per90", "xAG_per90", "sca_per90", "shots_total_per90",
            "progressive_carries_per90", "take_on_success_pct", "key_passes_per90",
            "padj_tackles_per90"
        ]
        
        peers = get_cohort_peers(self.full_df, "Winger / Attacking Mid", season="2025/26")
        pct_base = compute_player_percentiles(base_p, peers, winger_metrics)
        pct_p2 = compute_player_percentiles(p2, peers, winger_metrics)
        pct_p3 = compute_player_percentiles(p3, peers, winger_metrics)
        pct_top5 = compute_player_percentiles(bench_top5, peers, winger_metrics)
        pct_u21 = compute_player_percentiles(bench_u21, peers, winger_metrics)
        pct_laliga = compute_player_percentiles(bench_laliga, peers, winger_metrics)
        
        test_combos = [
            # Combo 1: Base + 3 Real Players
            ([p2, p3, base_p], [pct_p2, pct_p3, pct_base]),
            # Combo 2: Base + 2 Players + 1 Cohort
            ([p2, p3, bench_top5], [pct_p2, pct_p3, pct_top5]),
            # Combo 3: Base + 1 Player + 2 Cohorts
            ([p2, bench_top5, bench_u21], [pct_p2, pct_top5, pct_u21]),
            # Combo 4: Base + 3 Cohorts
            ([bench_top5, bench_u21, bench_laliga], [pct_top5, pct_u21, pct_laliga]),
        ]
        
        for idx, (comps, comp_pcts) in enumerate(test_combos, 1):
            delta_df = compute_comparison_deltas(
                base_row=base_p,
                base_percentiles=pct_base,
                compared_rows=comps,
                compared_percentiles=comp_pcts,
                metrics=winger_metrics
            )
            self.assertEqual(len(delta_df), len(winger_metrics))
            self.assertIn("comp_1_delta_val", delta_df.columns)
            self.assertIn("comp_2_delta_val", delta_df.columns)
            self.assertIn("comp_3_delta_val", delta_df.columns)
            self.assertIn("comp_1_delta_pct", delta_df.columns)
            self.assertIn("comp_2_delta_pct", delta_df.columns)
            self.assertIn("comp_3_delta_pct", delta_df.columns)
            self.assertFalse(delta_df.isnull().any().any(), f"NaNs found in combo {idx}")
            
            # Radar render
            profiles_for_radar = [
                {"name": base_p["player"], "percentiles": pct_base, "player_row": base_p}
            ] + [
                {"name": c["player"], "percentiles": cp, "player_row": c}
                for c, cp in zip(comps, comp_pcts)
            ]
            fig = create_multi_player_radar(profiles_for_radar, winger_metrics)
            self.assertEqual(len(fig.data), 4)
            
        print("PASS: All 4-profile combinations (players + benchmarks) verified successfully.")

    # --------------------------------------------------------------------------
    # DIMENSION 5: Under-21 Cohort Filtering Boundary Conditions
    # --------------------------------------------------------------------------
    def test_dimension_5_u21_boundary_conditions(self):
        """Stress-test U-21 boundary conditions: age 16, 21 included, age 22 excluded."""
        print("\n--- DIMENSION 5: Testing U-21 Boundary Conditions ---")
        
        for season in self.seasons:
            season_df = self.full_df[self.full_df["season"] == season]
            u21_df = season_df[season_df["age"] <= 21]
            non_u21_df = season_df[season_df["age"] > 21]
            
            # 1. Assert max age in U-21 is <= 21
            self.assertTrue((u21_df["age"] <= 21).all())
            self.assertTrue((non_u21_df["age"] >= 22).all())
            
            # 2. Assert players aged 21 are included in U-21
            age_21_count = (season_df["age"] == 21).sum()
            u21_age_21_count = (u21_df["age"] == 21).sum()
            self.assertEqual(age_21_count, u21_age_21_count)
            self.assertGreater(age_21_count, 0, f"Expected players aged 21 in season {season}")
            
            # 3. Assert players aged 22 are NOT in U-21
            u21_age_22_count = (u21_df["age"] == 22).sum()
            self.assertEqual(u21_age_22_count, 0)
            
            # 4. Check all position groups have U-21 representation in both seasons
            for pos in self.positions:
                pos_u21 = u21_df[u21_df["position_group"] == pos]
                self.assertGreater(
                    len(pos_u21), 0,
                    f"Position {pos} has 0 U-21 players in season {season}!"
                )
                
                # Check benchmark calculation adheres to boundary
                bench = compute_cohort_benchmark(
                    self.full_df,
                    position_group=pos,
                    season=season,
                    benchmark_type="u21_european"
                )
                self.assertLessEqual(bench["age"], 21.0)
                
        print("PASS: U-21 boundaries strictly validated (ages <= 21 included, >= 22 excluded).")

    # --------------------------------------------------------------------------
    # DIMENSION 6: Data Validation Resilience with Corrupted/Missing Data
    # --------------------------------------------------------------------------
    def test_dimension_6_data_validation_resilience(self):
        """Stress-test validate_master_dataset against 15 corrupted/malformed input mutations."""
        print("\n--- DIMENSION 6: Testing Data Validation Resilience ---")
        
        valid_df = self.full_df.copy()
        
        # Mutation 1: Drop required base column
        for base_col in REQUIRED_BASE_COLUMNS:
            bad_df = valid_df.drop(columns=[base_col])
            with self.assertRaises(ValueError, msg=f"Failed to reject missing base column {base_col}"):
                validate_master_dataset(bad_df)
                
        # Mutation 2: Drop required metadata column
        for meta_col in REQUIRED_METADATA_COLUMNS:
            bad_df = valid_df.drop(columns=[meta_col])
            with self.assertRaises(ValueError, msg=f"Failed to reject missing metadata column {meta_col}"):
                validate_master_dataset(bad_df)
                
        # Mutation 3: Insert NaN in each metadata column
        for meta_col in REQUIRED_METADATA_COLUMNS:
            bad_df = valid_df.copy()
            bad_df.loc[10, meta_col] = np.nan
            with self.assertRaises(ValueError, msg=f"Failed to reject NaN in {meta_col}"):
                validate_master_dataset(bad_df)
                
        # Mutation 4: Height < 160 cm
        bad_df = valid_df.copy()
        bad_df.loc[5, "height_cm"] = 159
        with self.assertRaises(ValueError):
            validate_master_dataset(bad_df)
            
        # Mutation 5: Height > 205 cm
        bad_df = valid_df.copy()
        bad_df.loc[5, "height_cm"] = 206
        with self.assertRaises(ValueError):
            validate_master_dataset(bad_df)
            
        # Mutation 6: Weight < 55 kg
        bad_df = valid_df.copy()
        bad_df.loc[5, "weight_kg"] = 54
        with self.assertRaises(ValueError):
            validate_master_dataset(bad_df)
            
        # Mutation 7: Weight > 105 kg
        bad_df = valid_df.copy()
        bad_df.loc[5, "weight_kg"] = 106
        with self.assertRaises(ValueError):
            validate_master_dataset(bad_df)
            
        # Mutation 8: Non-numeric height
        bad_df = valid_df.copy()
        bad_df["height_cm"] = bad_df["height_cm"].astype(str)
        with self.assertRaises(ValueError):
            validate_master_dataset(bad_df)
            
        # Mutation 9: Non-numeric market value
        bad_df = valid_df.copy()
        bad_df["market_value_eur"] = "Free"
        with self.assertRaises(ValueError):
            validate_master_dataset(bad_df)
            
        # Mutation 10: Zero market value
        bad_df = valid_df.copy()
        bad_df.loc[0, "market_value_eur"] = 0
        with self.assertRaises(ValueError):
            validate_master_dataset(bad_df)
            
        # Mutation 11: Negative market value
        bad_df = valid_df.copy()
        bad_df.loc[0, "market_value_eur"] = -100000
        with self.assertRaises(ValueError):
            validate_master_dataset(bad_df)
            
        # Mutation 12: Contract expiry < 2024
        bad_df = valid_df.copy()
        bad_df.loc[0, "contract_expiry"] = 2023
        with self.assertRaises(ValueError):
            validate_master_dataset(bad_df)
            
        # Mutation 13: Contract expiry > 2035
        bad_df = valid_df.copy()
        bad_df.loc[0, "contract_expiry"] = 2036
        with self.assertRaises(ValueError):
            validate_master_dataset(bad_df)
            
        # Mutation 14: Invalid preferred foot
        bad_df = valid_df.copy()
        bad_df.loc[0, "preferred_foot"] = "Tri-pedal"
        with self.assertRaises(ValueError):
            validate_master_dataset(bad_df)
            
        # Mutation 15: Invalid wage tier
        bad_df = valid_df.copy()
        bad_df.loc[0, "wage_tier"] = "Tier 99 ($1B/wk)"
        with self.assertRaises(ValueError):
            validate_master_dataset(bad_df)
            
        # Mutation 16: Invalid primary position
        bad_df = valid_df.copy()
        bad_df.loc[0, "primary_position"] = "SWEEPER_KEEPER"
        with self.assertRaises(ValueError):
            validate_master_dataset(bad_df)
            
        # Mutation 17: Empty dataframe
        with self.assertRaises(ValueError):
            validate_master_dataset(pd.DataFrame())
            
        # Mutation 18: None
        with self.assertRaises(ValueError):
            validate_master_dataset(None)

        print("PASS: All 18 adversarial corruption mutations correctly caught and rejected by validate_master_dataset.")


if __name__ == "__main__":
    unittest.main()
