"""
ScoutBench Configuration Module
Defines tactical metric sets for 6 distinct positional roles (matching DataMB / Pro standards),
metric labels, and theme settings.
"""

from typing import Dict, List

DEFAULT_MIN_MINUTES = 900

# --------------------------------------------------------------------------
# 6 Specialized Positional Role Templates for Pizza Radar Charts
# Categorized into: Attacking & Creation (Red), Possession & Progression (Blue), Defending & Pressing (Green)
# --------------------------------------------------------------------------

PIZZA_METRIC_TEMPLATES: Dict[str, Dict[str, List[str]]] = {
    "Goalkeeper": {
        "Shot-Stopping & Distribution": [
            "psxg_net_per90",          # Post-Shot xG minus Goals Allowed (Shot stopping value)
            "save_pct",                # Save percentage
            "pass_completion_pct",     # Overall passing accuracy
            "passes_completed_long_pct" # Long ball distribution accuracy
        ],
        "Sweeping & Aerial Command": [
            "def_actions_outside_pen_per90", # Sweeper keeper actions outside box
            "crosses_stopped_pct",           # Claiming crosses %
            "avg_dist_def_actions"           # Average distance of defensive actions from goal
        ]
    },
    "Centreback": {
        "Ball Progression & Build-Up": [
            "pass_completion_pct",
            "progressive_passes_per90",
            "progressive_passing_distance_per90",
            "passes_into_final_third_per90"
        ],
        "Carrying & Retention": [
            "progressive_carries_per90",
            "take_on_success_pct"
        ],
        "Defending & Aerial Dominance": [
            "padj_tackles_per90",
            "padj_interceptions_per90",
            "ball_recoveries_per90",
            "blocks_per90",
            "aerial_win_pct",
            "tackle_win_pct"
        ]
    },
    "Fullback / Wingback": {
        "Attacking & Creation": [
            "xAG_per90",
            "sca_per90",
            "key_passes_per90",
            "passes_into_penalty_area_per90"
        ],
        "Progression & Flank Threat": [
            "pass_completion_pct",
            "progressive_passes_per90",
            "progressive_carries_per90",
            "passes_into_final_third_per90",
            "take_ons_attempted_per90",
            "take_on_success_pct"
        ],
        "Defending & Transitions": [
            "padj_tackles_per90",
            "padj_interceptions_per90",
            "ball_recoveries_per90",
            "tackles_att_3rd_per90",
            "aerial_win_pct"
        ]
    },
    "Central / Defensive Midfielder": {
        "Attacking & Creation": [
            "npxG_per90",
            "xAG_per90",
            "sca_per90",
            "key_passes_per90",
            "passes_into_penalty_area_per90"
        ],
        "Possession & Progression": [
            "pass_completion_pct",
            "progressive_passes_per90",
            "progressive_carries_per90",
            "passes_into_final_third_per90",
            "take_on_success_pct"
        ],
        "Defending & Pressing": [
            "padj_tackles_per90",
            "padj_interceptions_per90",
            "ball_recoveries_per90",
            "blocks_per90",
            "aerial_win_pct"
        ]
    },
    "Winger / Attacking Mid": {
        "Attacking & Goal Threat": [
            "npxG_per90",
            "xAG_per90",
            "sca_per90",
            "shots_total_per90",
            "touches_att_pen_per90"
        ],
        "1v1 Isolation & Progression": [
            "take_ons_attempted_per90",
            "take_on_success_pct",
            "progressive_carries_per90",
            "progressive_passes_per90",
            "carries_into_penalty_area_per90",
            "key_passes_per90"
        ],
        "Defending & Work Rate": [
            "padj_tackles_per90",
            "padj_interceptions_per90",
            "ball_recoveries_per90",
            "tackles_att_3rd_per90"
        ]
    },
    "Centre-Forward / Striker": {
        "Finishing & Box Dominance": [
            "npxG_per90",
            "shots_total_per90",
            "shots_on_target_pct",
            "touches_att_pen_per90",
            "aerial_win_pct"
        ],
        "Link-Up & Creation": [
            "xAG_per90",
            "sca_per90",
            "key_passes_per90",
            "pass_completion_pct",
            "carries_into_penalty_area_per90"
        ],
        "Defending & High Press": [
            "tackles_att_3rd_per90",
            "ball_recoveries_per90",
            "padj_tackles_per90"
        ]
    }
}

# --------------------------------------------------------------------------
# Human-Readable Display Labels
# --------------------------------------------------------------------------
METRIC_LABELS: Dict[str, str] = {
    # Outfield Attacking
    "npxG_per90": "Non-Penalty xG",
    "xAG_per90": "Expected Assisted Goals (xAG)",
    "sca_per90": "Shot-Creating Actions (SCA)",
    "key_passes_per90": "Key Passes",
    "passes_into_penalty_area_per90": "Passes into 18-Yard Box",
    "shots_total_per90": "Shots Total",
    "shots_on_target_pct": "Shots on Target %",
    "touches_att_pen_per90": "Touches in Penalty Box",
    # Outfield Possession
    "pass_completion_pct": "Pass Completion %",
    "progressive_passes_per90": "Progressive Passes",
    "progressive_carries_per90": "Progressive Carries",
    "passes_into_final_third_per90": "Passes into Final 3rd",
    "take_on_success_pct": "Take-On Win %",
    "take_ons_attempted_per90": "Take-Ons Attempted",
    "carries_into_penalty_area_per90": "Carries into 18-Yard Box",
    "progressive_passing_distance_per90": "Prog. Passing Distance",
    # Outfield Defending
    "padj_tackles_per90": "pAdj Tackles Won",
    "padj_interceptions_per90": "pAdj Interceptions",
    "ball_recoveries_per90": "Ball Recoveries",
    "blocks_per90": "Blocks",
    "aerial_win_pct": "Aerial Duel Win %",
    "tackles_att_3rd_per90": "High-Press Tackles (Att 3rd)",
    "tackle_win_pct": "Tackle Win %",
    # Goalkeeping Metrics
    "psxg_net_per90": "PSxG +/- (Shot Stopping)",
    "save_pct": "Save Percentage",
    "passes_completed_long_pct": "Long Ball Accuracy %",
    "def_actions_outside_pen_per90": "Sweeper Actions / 90",
    "crosses_stopped_pct": "Crosses Stopped %",
    "avg_dist_def_actions": "Avg Distance of Def Actions"
}

# --------------------------------------------------------------------------
# Professional Theme & Color Palette Configurations
# --------------------------------------------------------------------------
COLOR_PALETTES = {
    "Opta Pro (Midnight Pitch)": {
        "canvas_bg": "#0B0F17",
        "card_bg": "#151D2A",
        "border_color": "#233044",
        "text_primary": "#F8FAFC",
        "text_secondary": "#94A3B8",
        "grid_color": "#1E293B",
        "accent_color": "#F59E0B",
        "slice_colors": {
            "Attacking & Creation": "#F59E0B",
            "Attacking & Goal Threat": "#F59E0B",
            "Finishing & Box Dominance": "#F59E0B",
            "Shot-Stopping & Distribution": "#F59E0B",
            "Possession & Progression": "#0284C7",
            "Progression & Flank Threat": "#0284C7",
            "1v1 Isolation & Progression": "#0284C7",
            "Link-Up & Creation": "#38BDF8",
            "Ball Progression & Build-Up": "#0284C7",
            "Carrying & Retention": "#38BDF8",
            "Defending & Pressing": "#10B981",
            "Defending & Transitions": "#10B981",
            "Defending & Work Rate": "#10B981",
            "Defending & High Press": "#10B981",
            "Defending & Aerial Dominance": "#10B981",
            "Sweeping & Aerial Command": "#10B981"
        }
    },
    "The Athletic (Editorial Pitch)": {
        "canvas_bg": "#111215",
        "card_bg": "#1A1C23",
        "border_color": "#2A2D38",
        "text_primary": "#EAE6DF",
        "text_secondary": "#A5A7AF",
        "grid_color": "#262833",
        "accent_color": "#E06D53",
        "slice_colors": {
            "Attacking & Creation": "#E06D53",
            "Attacking & Goal Threat": "#E06D53",
            "Finishing & Box Dominance": "#E06D53",
            "Shot-Stopping & Distribution": "#E06D53",
            "Possession & Progression": "#608BA6",
            "Progression & Flank Threat": "#608BA6",
            "1v1 Isolation & Progression": "#608BA6",
            "Link-Up & Creation": "#7DA6C2",
            "Ball Progression & Build-Up": "#608BA6",
            "Carrying & Retention": "#7DA6C2",
            "Defending & Pressing": "#4E876A",
            "Defending & Transitions": "#4E876A",
            "Defending & Work Rate": "#4E876A",
            "Defending & High Press": "#4E876A",
            "Defending & Aerial Dominance": "#4E876A",
            "Sweeping & Aerial Command": "#4E876A"
        }
    },
    "Linear Carbon (Minimalist Swiss)": {
        "canvas_bg": "#090A0C",
        "card_bg": "#13151A",
        "border_color": "#222630",
        "text_primary": "#FFFFFF",
        "text_secondary": "#8B949E",
        "grid_color": "#1C2028",
        "accent_color": "#F43F5E",
        "slice_colors": {
            "Attacking & Creation": "#F43F5E",
            "Attacking & Goal Threat": "#F43F5E",
            "Finishing & Box Dominance": "#F43F5E",
            "Shot-Stopping & Distribution": "#F43F5E",
            "Possession & Progression": "#6366F1",
            "Progression & Flank Threat": "#6366F1",
            "1v1 Isolation & Progression": "#6366F1",
            "Link-Up & Creation": "#818CF8",
            "Ball Progression & Build-Up": "#6366F1",
            "Carrying & Retention": "#818CF8",
            "Defending & Pressing": "#14B8A6",
            "Defending & Transitions": "#14B8A6",
            "Defending & Work Rate": "#14B8A6",
            "Defending & High Press": "#14B8A6",
            "Defending & Aerial Dominance": "#14B8A6",
            "Sweeping & Aerial Command": "#14B8A6"
        }
    },
    "DataMB Studio (Scandinavian Deep)": {
        "canvas_bg": "#080E15",
        "card_bg": "#101C27",
        "border_color": "#1C2E3F",
        "text_primary": "#F1F5F9",
        "text_secondary": "#7E92A2",
        "grid_color": "#182635",
        "accent_color": "#FF6B6B",
        "slice_colors": {
            "Attacking & Creation": "#FF6B6B",
            "Attacking & Goal Threat": "#FF6B6B",
            "Finishing & Box Dominance": "#FF6B6B",
            "Shot-Stopping & Distribution": "#FF6B6B",
            "Possession & Progression": "#4D96FF",
            "Progression & Flank Threat": "#4D96FF",
            "1v1 Isolation & Progression": "#4D96FF",
            "Link-Up & Creation": "#6BAAFF",
            "Ball Progression & Build-Up": "#4D96FF",
            "Carrying & Retention": "#6BAAFF",
            "Defending & Pressing": "#6BCB77",
            "Defending & Transitions": "#6BCB77",
            "Defending & Work Rate": "#6BCB77",
            "Defending & High Press": "#6BCB77",
            "Defending & Aerial Dominance": "#6BCB77",
            "Sweeping & Aerial Command": "#6BCB77"
        }
    }
}

DEFAULT_PALETTE_NAME = "The Athletic (Editorial Pitch)"
RADAR_THEME = {
    "background_color": COLOR_PALETTES[DEFAULT_PALETTE_NAME]["card_bg"],
    "slice_colors": COLOR_PALETTES[DEFAULT_PALETTE_NAME]["slice_colors"],
    "text_color": COLOR_PALETTES[DEFAULT_PALETTE_NAME]["text_primary"],
    "grid_color": COLOR_PALETTES[DEFAULT_PALETTE_NAME]["grid_color"],
    "accent_color": COLOR_PALETTES[DEFAULT_PALETTE_NAME]["accent_color"]
}
