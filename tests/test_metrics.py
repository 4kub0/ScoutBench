"""
ScoutBench Unit Tests
Tests for normalization, percentile ranking, continuous tactical spectrum,
universal behavioral indexes, and pro-tier scouting intelligence generation.
"""

import unittest
import pandas as pd
import numpy as np
from src.normalization import calculate_per90, calculate_padj
from src.metrics_engine import (
    compute_player_percentiles, 
    compute_tactical_spectrum,
    compute_behavioral_indexes,
    classify_tactical_archetype, 
    extract_strengths_and_vulnerabilities,
    generate_scouting_intelligence
)


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

    def test_tactical_spectrum_and_archetype(self):
        # Deep Tempo Dictator Profile (Pedri / Kroos archetype)
        midfielder_pcts = {
            "progressive_passes_per90": 95.0,
            "passes_into_final_third_per90": 92.0,
            "pass_completion_pct": 90.0,
            "take_on_success_pct": 80.0,
            "progressive_carries_per90": 70.0,
            "padj_tackles_per90": 40.0,
            "padj_interceptions_per90": 40.0,
            "ball_recoveries_per90": 55.0,
            "sca_per90": 75.0,
            "npxG_per90": 30.0
        }
        spectrum = compute_tactical_spectrum(midfielder_pcts, "Central / Defensive Midfielder")
        self.assertEqual(len(spectrum["axes"]), 4)
        self.assertEqual(spectrum["primary_archetype"], "Deep Tempo Dictator")
        self.assertGreaterEqual(spectrum["axes"][0]["score"], 0.0)
        self.assertLessEqual(spectrum["axes"][0]["score"], 100.0)
        
        archetype = classify_tactical_archetype(midfielder_pcts, "Central / Defensive Midfielder")
        self.assertEqual(archetype, "Deep Tempo Dictator")

    def test_behavioral_indexes(self):
        # High Pressing Winger (Gordon profile)
        gordon_pcts = {
            "tackles_att_3rd_per90": 95.0,
            "padj_tackles_per90": 85.0,
            "padj_interceptions_per90": 75.0,
            "ball_recoveries_per90": 80.0,
            "progressive_passing_distance_per90": 60.0,
            "progressive_carries_per90": 85.0,
            "passes_into_final_third_per90": 50.0,
            "pass_completion_pct": 65.0,
            "take_on_success_pct": 60.0,
            "tackle_win_pct": 70.0,
            "npxG_per90": 70.0,
            "xAG_per90": 65.0,
            "sca_per90": 70.0
        }
        indexes = compute_behavioral_indexes(gordon_pcts, "Winger / Attacking Mid")
        self.assertIn("High-Press & Work-Rate", indexes)
        self.assertIn("Verticality & Directness", indexes)
        self.assertIn("Press-Resistance & Retention", indexes)
        self.assertIn("Offensive Threat & Opportunity", indexes)
        
        # High Press index should be elite (>= 80)
        self.assertGreaterEqual(indexes["High-Press & Work-Rate"]["score"], 80.0)

    def test_scouting_intelligence_generation(self):
        pcts = {
            "tackles_att_3rd_per90": 92.0,
            "padj_tackles_per90": 88.0,
            "padj_interceptions_per90": 70.0,
            "ball_recoveries_per90": 80.0,
            "progressive_carries_per90": 85.0,
            "npxG_per90": 75.0
        }
        player_row = pd.Series({"player": "Anthony Gordon", "team": "Newcastle", "league": "Premier League"})
        spectrum = compute_tactical_spectrum(pcts, "Winger / Attacking Mid")
        indexes = compute_behavioral_indexes(pcts, "Winger / Attacking Mid")
        
        intel = generate_scouting_intelligence(player_row, pcts, spectrum, indexes, "Winger / Attacking Mid")
        self.assertTrue(len(intel["system_notes"]) > 0)
        # Should have elite counter presser badge note
        notes_text = " ".join([n["text"] for n in intel["system_notes"]])
        self.assertIn("High-Press", notes_text)


if __name__ == "__main__":
    unittest.main()
