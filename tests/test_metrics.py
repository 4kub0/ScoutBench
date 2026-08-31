"""
ScoutBench Unit Tests
Tests for normalization, percentile ranking, and tactical archetype classification.
"""

import unittest
import pandas as pd
import numpy as np
from src.normalization import calculate_per90, calculate_padj
from src.metrics_engine import compute_player_percentiles, classify_tactical_archetype, extract_strengths_and_vulnerabilities


class TestScoutBenchMetrics(unittest.TestCase):

    def test_per90_calculation(self):
        raw = pd.Series([10.0, 5.0, 0.0])
        minutes = pd.Series([900.0, 450.0, 900.0])
        res = calculate_per90(raw, minutes)
        
        self.assertAlmostEqual(res.iloc[0], 1.0, places=2)
        self.assertAlmostEqual(res.iloc[1], 1.0, places=2)
        self.assertAlmostEqual(res.iloc[2], 0.0, places=2)

    def test_padj_calculation(self):
        # 60% possession team vs 40% possession team
        per90 = pd.Series([2.0, 2.0])
        possession = pd.Series([60.0, 40.0])
        res = calculate_padj(per90, possession)
        
        # High possession team (opp poss = 40%) -> 2.0 * (50 / 40) = 2.5
        self.assertAlmostEqual(res.iloc[0], 2.50, places=2)
        # Low possession team (opp poss = 60%) -> 2.0 * (50 / 60) = 1.67
        self.assertAlmostEqual(res.iloc[1], 1.67, places=2)

    def test_percentile_ranking(self):
        cohort_data = pd.DataFrame({
            "prog_passes": [2.0, 4.0, 6.0, 8.0, 10.0],
            "xG": [0.1, 0.2, 0.3, 0.4, 0.5]
        })
        player = pd.Series({"prog_passes": 10.0, "xG": 0.1})
        
        pcts = compute_player_percentiles(player, cohort_data, ["prog_passes", "xG"])
        self.assertEqual(pcts["prog_passes"], 100.0)
        self.assertEqual(pcts["xG"], 20.0)

    def test_archetype_classification(self):
        # Deep Tempo Dictator Profile
        midfielder_pcts = {
            "pass_completion_pct": 92.0,
            "progressive_passes_per90": 88.0,
            "passes_into_final_third_per90": 85.0
        }
        archetype = classify_tactical_archetype(midfielder_pcts, "Central / Defensive Midfielder")
        self.assertEqual(archetype, "Deep Tempo Dictator")

    def test_strengths_and_vulnerabilities(self):
        pcts = {
            "metric_a": 95.0,
            "metric_b": 20.0,
            "metric_c": 50.0
        }
        strengths, vulns = extract_strengths_and_vulnerabilities(pcts, high_threshold=85, low_threshold=35)
        self.assertEqual(len(strengths), 1)
        self.assertEqual(strengths[0]["metric"], "metric_a")
        self.assertEqual(len(vulns), 1)
        self.assertEqual(vulns[0]["metric"], "metric_b")


if __name__ == "__main__":
    unittest.main()
