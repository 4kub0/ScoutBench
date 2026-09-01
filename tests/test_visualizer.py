"""
Unit tests for visualizer functions (PyPizza radar, Pitch Heatmap, Spatial generator).
"""

import unittest
import pandas as pd
import matplotlib.pyplot as plt
from src.visualizer import create_pizza_radar, create_pitch_heatmap, generate_player_spatial_distribution
from src.config import COLOR_PALETTES, PIZZA_METRIC_TEMPLATES


class TestVisualizer(unittest.TestCase):

    def test_heatmap_generation_all_positions(self):
        theme = COLOR_PALETTES['The Athletic (Editorial Pitch)']
        positions = [
            ('Goalkeeper', 'GK'),
            ('Centreback', 'CB'),
            ('Fullback / Wingback', 'LB'),
            ('Central / Defensive Midfielder', 'CM'),
            ('Winger / Attacking Mid', 'LW'),
            ('Centre-Forward / Striker', 'ST')
        ]
        
        for pos_group, pos_code in positions:
            player_row = pd.Series({
                'player': f'Test {pos_code}',
                'team': 'Test Club',
                'league': 'Test League',
                'position': pos_code,
                'team_possession_pct': 58.0,
                'avg_dist_def_actions': 17.5,
                'touches_att_pen_per90': 4.0,
                'progressive_carries_per90': 3.5,
                'npxG_per90': 0.40,
                'xAG_per90': 0.25
            })
            fig = create_pitch_heatmap(player_row, pos_group, palette=theme)
            self.assertIsInstance(fig, plt.Figure)
            plt.close(fig)

    def test_spatial_distribution_bounds(self):
        player_row = pd.Series({
            'player': 'Erling Haaland',
            'position': 'ST',
            'touches_att_pen_per90': 7.5,
            'npxG_per90': 0.85
        })
        x, y = generate_player_spatial_distribution(player_row, 'Centre-Forward / Striker', n_points=300)
        self.assertEqual(len(x), 300)
        self.assertEqual(len(y), 300)
        self.assertTrue((x >= 2.0).all() and (x <= 118.0).all())
        self.assertTrue((y >= 2.0).all() and (y <= 78.0).all())


if __name__ == '__main__':
    unittest.main()
