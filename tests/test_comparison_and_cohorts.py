"""
ScoutBench Unit Tests for Milestone M2:
- Cohort Reference Baseline Benchmarks (4 Presets)
- Statistical Delta Table Calculations (+/- Differentials)
- Overlapping Multi-Player Polar Radar Generation (2 to 4 Profiles)
- Backward Compatibility & Zero-Emoji Verification
"""

import unittest
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from src.data_loader import load_master_dataset, get_player_profile, get_cohort_peers
from src.metrics_engine import (
    compute_cohort_benchmark,
    compute_comparison_deltas,
    compute_player_percentiles,
    compute_tactical_spectrum,
    compute_behavioral_indexes,
    generate_scouting_intelligence
)
from src.visualizer import create_multi_player_radar, create_pizza_radar
from src.config import PIZZA_METRIC_TEMPLATES, COLOR_PALETTES


class TestComparisonAndCohorts(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.df = load_master_dataset(min_minutes=900)
        cls.raw_df = load_master_dataset(min_minutes=0)

    # --------------------------------------------------------------------------
    # 1. Cohort Benchmark Presets
    # --------------------------------------------------------------------------

    def test_cohort_benchmark_top5_positional(self):
        """Verify Top 5 European Positional Average preset computation."""
        pos_group = "Central / Defensive Midfielder"
        season = "2025/26"
        benchmark = compute_cohort_benchmark(
            self.df,
            position_group=pos_group,
            season=season,
            benchmark_type="top5_positional"
        )
        
        self.assertIsInstance(benchmark, pd.Series)
        self.assertIn("Top 5 European", benchmark["player"])
        self.assertEqual(benchmark["team"], "Cohort Benchmark")
        self.assertEqual(benchmark["position_group"], pos_group)
        self.assertEqual(benchmark["season"], season)
        
        # Verify genuine arithmetic mean
        expected_subset = self.df[(self.df["season"] == season) & (self.df["position_group"] == pos_group)]
        self.assertEqual(benchmark["sample_size"], len(expected_subset))
        self.assertAlmostEqual(
            benchmark["progressive_passes_per90"],
            expected_subset["progressive_passes_per90"].mean(),
            places=2
        )
        self.assertAlmostEqual(
            benchmark["pass_completion_pct"],
            expected_subset["pass_completion_pct"].mean(),
            places=2
        )

    def test_cohort_benchmark_domestic_positional(self):
        """Verify Domestic League Positional Average preset computation."""
        pos_group = "Winger / Attacking Mid"
        season = "2025/26"
        league = "La Liga"
        benchmark = compute_cohort_benchmark(
            self.df,
            position_group=pos_group,
            season=season,
            benchmark_type="domestic_positional",
            domestic_league=league
        )
        
        self.assertIsInstance(benchmark, pd.Series)
        self.assertIn(league, benchmark["player"])
        self.assertEqual(benchmark["league"], league)
        
        expected_subset = self.df[
            (self.df["season"] == season) & 
            (self.df["position_group"] == pos_group) & 
            (self.df["league"] == league)
        ]
        self.assertEqual(benchmark["sample_size"], len(expected_subset))
        self.assertAlmostEqual(
            benchmark["npxG_per90"],
            expected_subset["npxG_per90"].mean(),
            places=2
        )

    def test_cohort_benchmark_u21_european(self):
        """Verify Under-21 European Positional Average preset computation."""
        pos_group = "Centre-Forward / Striker"
        season = "2025/26"
        benchmark = compute_cohort_benchmark(
            self.raw_df,
            position_group=pos_group,
            season=season,
            benchmark_type="u21_european"
        )
        
        self.assertIsInstance(benchmark, pd.Series)
        self.assertIn("U-21", benchmark["player"])
        
        expected_subset = self.raw_df[
            (self.raw_df["season"] == season) & 
            (self.raw_df["position_group"] == pos_group) & 
            (self.raw_df["age"] <= 21)
        ]
        self.assertEqual(benchmark["sample_size"], len(expected_subset))
        self.assertGreater(benchmark["sample_size"], 0)
        self.assertLessEqual(benchmark["age"], 21.0)
        self.assertAlmostEqual(
            benchmark["shots_total_per90"],
            expected_subset["shots_total_per90"].mean(),
            places=2
        )

    def test_cohort_benchmark_u21_domestic(self):
        """Verify Under-21 Domestic League Average preset computation."""
        pos_group = "Fullback / Wingback"
        season = "2025/26"
        league = "Premier League"
        benchmark = compute_cohort_benchmark(
            self.raw_df,
            position_group=pos_group,
            season=season,
            benchmark_type="u21_domestic",
            domestic_league=league
        )
        
        self.assertIsInstance(benchmark, pd.Series)
        self.assertIn("U-21", benchmark["player"])
        self.assertIn(league, benchmark["player"])
        
        expected_subset = self.raw_df[
            (self.raw_df["season"] == season) & 
            (self.raw_df["position_group"] == pos_group) & 
            (self.raw_df["league"] == league) & 
            (self.raw_df["age"] <= 21)
        ]
        self.assertEqual(benchmark["sample_size"], len(expected_subset))
        self.assertAlmostEqual(
            benchmark["padj_tackles_per90"],
            expected_subset["padj_tackles_per90"].mean(),
            places=2
        )

    def test_cohort_benchmark_validation_errors(self):
        """Verify exception handling for invalid benchmark types or missing league inputs."""
        # Missing domestic_league for domestic_positional
        with self.assertRaises(ValueError):
            compute_cohort_benchmark(
                self.df,
                position_group="Centreback",
                season="2025/26",
                benchmark_type="domestic_positional"
            )
            
        # Missing domestic_league for u21_domestic
        with self.assertRaises(ValueError):
            compute_cohort_benchmark(
                self.df,
                position_group="Centreback",
                season="2025/26",
                benchmark_type="u21_domestic"
            )
            
        # Invalid benchmark type string
        with self.assertRaises(ValueError):
            compute_cohort_benchmark(
                self.df,
                position_group="Centreback",
                season="2025/26",
                benchmark_type="unknown_benchmark_preset"
            )
            
        # Empty DataFrame
        with self.assertRaises(ValueError):
            compute_cohort_benchmark(
                pd.DataFrame(),
                position_group="Centreback",
                season="2025/26",
                benchmark_type="top5_positional"
            )

    # --------------------------------------------------------------------------
    # 2. Delta Table Computations
    # --------------------------------------------------------------------------

    def test_compute_comparison_deltas(self):
        """Verify calculation of raw and percentile deltas against base target player."""
        base_row = pd.Series({"player": "Pedri", "progressive_passes_per90": 8.5, "npxG_per90": 0.15})
        base_pcts = {"progressive_passes_per90": 95.0, "npxG_per90": 40.0}
        
        comp_row_1 = pd.Series({"player": "Gavi", "progressive_passes_per90": 6.0, "npxG_per90": 0.25})
        comp_pcts_1 = {"progressive_passes_per90": 75.0, "npxG_per90": 65.0}
        
        comp_row_2 = pd.Series({"player": "Cohort Benchmark", "progressive_passes_per90": 5.0, "npxG_per90": 0.15})
        comp_pcts_2 = {"progressive_passes_per90": 50.0, "npxG_per90": 40.0}
        
        metrics = ["progressive_passes_per90", "npxG_per90"]
        
        delta_df = compute_comparison_deltas(
            base_row=base_row,
            base_percentiles=base_pcts,
            compared_rows=[comp_row_1, comp_row_2],
            compared_percentiles=[comp_pcts_1, comp_pcts_2],
            metrics=metrics
        )
        
        self.assertEqual(len(delta_df), 2)
        self.assertIn("metric", delta_df.columns)
        self.assertIn("base_val", delta_df.columns)
        self.assertIn("base_pct", delta_df.columns)
        self.assertIn("comp_1_delta_val", delta_df.columns)
        self.assertIn("comp_1_delta_pct", delta_df.columns)
        self.assertIn("comp_2_delta_val", delta_df.columns)
        self.assertIn("comp_2_delta_pct", delta_df.columns)
        
        # Check row 0: progressive_passes_per90
        # Gavi vs Pedri: 6.0 - 8.5 = -2.5, 75.0 - 95.0 = -20.0
        r0 = delta_df.iloc[0]
        self.assertEqual(r0["metric"], "progressive_passes_per90")
        self.assertEqual(r0["base_val"], 8.5)
        self.assertEqual(r0["base_pct"], 95.0)
        self.assertEqual(r0["comp_1_val"], 6.0)
        self.assertEqual(r0["comp_1_pct"], 75.0)
        self.assertEqual(r0["comp_1_delta_val"], -2.5)
        self.assertEqual(r0["comp_1_delta_pct"], -20.0)
        
        # Check row 1: npxG_per90
        # Gavi vs Pedri: 0.25 - 0.15 = +0.10, 65.0 - 40.0 = +25.0
        # Benchmark vs Pedri: 0.15 - 0.15 = 0.00, 40.0 - 40.0 = 0.0
        r1 = delta_df.iloc[1]
        self.assertEqual(r1["metric"], "npxG_per90")
        self.assertEqual(r1["comp_1_delta_val"], 0.1)
        self.assertEqual(r1["comp_1_delta_pct"], 25.0)
        self.assertEqual(r1["comp_2_delta_val"], 0.0)
        self.assertEqual(r1["comp_2_delta_pct"], 0.0)

    # --------------------------------------------------------------------------
    # 3. Multi-Player Overlapping Radar Chart Generation
    # --------------------------------------------------------------------------

    def test_multi_player_radar_chart_generation(self):
        """Verify Scatterpolar multi-trace generation for 2, 3, and 4 player profiles."""
        metrics = [
            "npxG_per90", "xAG_per90", "sca_per90",
            "progressive_passes_per90", "progressive_carries_per90", "padj_tackles_per90"
        ]
        
        p1 = {"name": "Lamine Yamal", "percentiles": {m: 90.0 for m in metrics}}
        p2 = {"name": "Bukayo Saka", "percentiles": {m: 85.0 for m in metrics}}
        p3 = {"name": "Top 5 Winger Average", "percentiles": {m: 50.0 for m in metrics}, "is_benchmark": True}
        p4 = {"name": "Michael Olise", "percentiles": {m: 82.0 for m in metrics}}
        
        # 2 Profiles
        fig_2 = create_multi_player_radar([p1, p2], metrics)
        self.assertIsInstance(fig_2, go.Figure)
        self.assertEqual(len(fig_2.data), 2)
        # Check closed polygon: length of r is len(metrics) + 1
        self.assertEqual(len(fig_2.data[0].r), len(metrics) + 1)
        self.assertEqual(fig_2.data[0].r[0], fig_2.data[0].r[-1])
        
        # 3 Profiles
        fig_3 = create_multi_player_radar([p1, p2, p3], metrics)
        self.assertEqual(len(fig_3.data), 3)
        self.assertEqual(fig_3.data[2].line.dash, "dash")
        
        # 4 Profiles
        fig_4 = create_multi_player_radar([p1, p2, p3, p4], metrics)
        self.assertEqual(len(fig_4.data), 4)

    # --------------------------------------------------------------------------
    # 4. Backward Compatibility & Zero-Emoji Compliance
    # --------------------------------------------------------------------------

    def test_backward_compatibility_and_zero_emojis(self):
        """Verify single player radar and metrics work and scouting intelligence badges contain 0 emojis."""
        yamal = get_player_profile(self.df, "Lamine Yamal", season="2025/26")
        self.assertIsNotNone(yamal)
        
        peers = get_cohort_peers(self.df, yamal["position_group"], season="2025/26")
        metrics = ["npxG_per90", "xAG_per90", "sca_per90", "progressive_carries_per90"]
        pcts = compute_player_percentiles(yamal, peers, metrics)
        
        spectrum = compute_tactical_spectrum(pcts, yamal["position_group"])
        indexes = compute_behavioral_indexes(pcts, yamal["position_group"])
        intel = generate_scouting_intelligence(yamal, pcts, spectrum, indexes, yamal["position_group"])
        
        self.assertIn("system_notes", intel)
        # Verify no emojis in badges
        for note in intel["system_notes"]:
            badge = note["badge"]
            self.assertTrue(badge.isupper() or "-" in badge, f"Badge is not clean uppercase: {badge}")
            self.assertFalse(any(ord(c) > 127 for c in badge), f"Found non-ASCII emoji in badge: {badge}")


if __name__ == "__main__":
    unittest.main()
