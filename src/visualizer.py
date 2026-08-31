"""
ScoutBench Visualizer Module
Renders professional, dark-mode PyPizza radar charts (via mplsoccer) and interactive Plotly quadrant scatter plots.
"""

from typing import Dict, List, Tuple
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from mplsoccer import PyPizza

from src.config import RADAR_THEME, METRIC_LABELS


def create_pizza_radar(
    player_name: str,
    team_name: str,
    league_name: str,
    season: str,
    archetype: str,
    minutes: int,
    categories: Dict[str, List[str]],
    percentiles: Dict[str, float],
    palette: dict = None
) -> plt.Figure:
    """
    Renders an elite, publication-grade dark-themed Pizza Radar chart using mplsoccer.PyPizza.
    """
    theme = palette or RADAR_THEME
    all_metrics = []
    slice_colors = []
    values = []
    param_labels = []
    
    cat_color_map = theme.get("slice_colors", RADAR_THEME["slice_colors"])
    
    # Track slice counts per category to draw clean boundary lines
    slice_counts = []
    
    for cat_name, metric_list in categories.items():
        slice_counts.append(len(metric_list))
        color = cat_color_map.get(cat_name, theme.get("accent_color", "#38BDF8"))
        for m in metric_list:
            all_metrics.append(m)
            slice_colors.append(color)
            values.append(percentiles.get(m, 50.0))
            # Format clean multi-line label for tight fit
            label = METRIC_LABELS.get(m, m)
            if len(label) > 18:
                # Break long labels into two lines
                words = label.split()
                mid = len(words) // 2
                label = " ".join(words[:mid]) + "\n" + " ".join(words[mid:])
            param_labels.append(label)

    # Initialize PyPizza
    bg_col = theme.get("card_bg", theme.get("background_color", "#151D2A"))
    grid_col = theme.get("grid_color", "#233044")
    accent_col = theme.get("accent_color", "#F59E0B")
    text_col = theme.get("text_primary", theme.get("text_color", "#F8FAFC"))

    baker = PyPizza(
        params=param_labels,
        background_color=bg_col,
        straight_line_color=grid_col,
        straight_line_lw=1,
        last_circle_lw=1.5,
        last_circle_color=accent_col,
        other_circle_lw=1,
        other_circle_ls="-.",
        other_circle_color=grid_col
    )

    # Plot pizza
    fig, ax = baker.make_pizza(
        values=values,
        figsize=(10, 10.5),
        color_blank_space="same",
        slice_colors=slice_colors,
        blank_alpha=0.15,
        kwargs_slices=dict(
            edgecolor=bg_col, zorder=2, linewidth=1.5
        ),
        kwargs_params=dict(
            color=text_col, fontsize=10.5,
            va="center", alpha=0.9
        ),
        kwargs_values=dict(
            color=text_col, fontsize=9.5,
            zorder=3,
            bbox=dict(
                edgecolor=grid_col, facecolor=bg_col,
                boxstyle="round,pad=0.2", lw=1
            )
        )
    )

    # Add custom styled title & subtitles
    title_text = f"{player_name}"
    subtitle_text = f"{team_name} | {league_name} ({season}) | {minutes:,} Mins\nTactical Archetype: {archetype}"

    fig.text(
        0.515, 0.965, title_text, size=20,
        ha="center", color=text_col, fontweight="bold"
    )
    fig.text(
        0.515, 0.925, subtitle_text, size=11,
        ha="center", color=theme.get("text_secondary", "#94A3B8")
    )

    # Add Legend for categories at the bottom
    legend_y = 0.035
    cat_names = list(categories.keys())
    if len(cat_names) == 3:
        fig.text(0.22, legend_y, f"■ {cat_names[0]}", size=10, color=cat_color_map.get(cat_names[0], theme.get("accent_color", "#E06D53")), fontweight="bold")
        fig.text(0.46, legend_y, f"■ {cat_names[1]}", size=10, color=cat_color_map.get(cat_names[1], "#608BA6"), fontweight="bold")
        fig.text(0.74, legend_y, f"■ {cat_names[2]}", size=10, color=cat_color_map.get(cat_names[2], "#4E876A"), fontweight="bold")
    elif len(cat_names) == 2:
        fig.text(0.32, legend_y, f"■ {cat_names[0]}", size=10, color=cat_color_map.get(cat_names[0], theme.get("accent_color", "#E06D53")), fontweight="bold")
        fig.text(0.62, legend_y, f"■ {cat_names[1]}", size=10, color=cat_color_map.get(cat_names[1], "#4E876A"), fontweight="bold")

    # Add credit watermark
    fig.text(
        0.98, 0.01, "ScoutBench Analytics | Percentiles vs. Positional Cohort (Min. 900 Mins)",
        size=8, color=theme.get("text_secondary", "#94A3B8"), ha="right"
    )

    return fig


def create_quadrant_scatter(
    df: pd.DataFrame,
    x_metric: str,
    y_metric: str,
    target_player: str,
    position_group: str,
    palette: dict = None
) -> go.Figure:
    """
    Renders an interactive 4-quadrant benchmark scatter plot using Plotly
    with median quadrant lines and a glowing highlight on the target player.
    """
    theme = palette or RADAR_THEME
    x_label = METRIC_LABELS.get(x_metric, x_metric)
    y_label = METRIC_LABELS.get(y_metric, y_metric)
    
    # Filter valid non-null rows
    plot_df = df.dropna(subset=[x_metric, y_metric]).copy()
    
    # Medians for quadrant dividers
    x_median = plot_df[x_metric].median()
    y_median = plot_df[y_metric].median()
    
    # Mark target player
    plot_df["is_target"] = plot_df["player"] == target_player
    
    fig = go.Figure()
    
    # 1. Base cohort scatter points
    other_players = plot_df[~plot_df["is_target"]]
    fig.add_trace(go.Scatter(
        x=other_players[x_metric],
        y=other_players[y_metric],
        mode="markers",
        marker=dict(
            size=7,
            color="#64748B",
            opacity=0.60,
            line=dict(width=0.5, color="#94A3B8")
        ),
        text=other_players.apply(
            lambda r: f"<b>{r['player']}</b> ({r.get('team', '')})<br>Age: {r.get('age', 'N/A')}<br>{x_label}: {r[x_metric]}<br>{y_label}: {r[y_metric]}",
            axis=1
        ),
        hoverinfo="text",
        name="Cohort Peers"
    ))
    
    # 2. Target player glowing highlight
    target_row = plot_df[plot_df["is_target"]]
    accent_col = theme.get("accent_color", "#F59E0B")
    card_bg = theme.get("card_bg", theme.get("background_color", "#151D2A"))
    canvas_bg = theme.get("canvas_bg", "#0B0F17")
    grid_col = theme.get("grid_color", "#233044")
    text_col = theme.get("text_primary", "#F8FAFC")

    if not target_row.empty:
        r = target_row.iloc[0]
        fig.add_trace(go.Scatter(
            x=[r[x_metric]],
            y=[r[y_metric]],
            mode="markers+text",
            marker=dict(
                size=16,
                color=accent_col,
                symbol="star",
                line=dict(width=2, color="#FFFFFF")
            ),
            text=[f"<b>{target_player}</b>"],
            textposition="top center",
            textfont=dict(color=accent_col, size=13),
            hovertext=f"<b>⭐ {target_player}</b> ({r.get('team', '')})<br>{x_label}: {r[x_metric]}<br>{y_label}: {r[y_metric]}",
            hoverinfo="text",
            name=target_player
        ))
        
    # 3. Median quadrant lines
    fig.add_vline(x=x_median, line_dash="dash", line_color=grid_col, opacity=0.8)
    fig.add_hline(y=y_median, line_dash="dash", line_color=grid_col, opacity=0.8)
    
    # Dark mode layout styling
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor=canvas_bg,
        plot_bgcolor=card_bg,
        title=f"<b>Tactical Benchmark: {x_label} vs. {y_label}</b><br><span style='font-size:12px; color:#94A3B8;'>Cohort: {position_group} (Dashed lines indicate Cohort Medians)</span>",
        xaxis=dict(
            title=f"<b>{x_label}</b>",
            gridcolor=grid_col,
            zerolinecolor=grid_col,
            color=text_col
        ),
        yaxis=dict(
            title=f"<b>{y_label}</b>",
            gridcolor=grid_col,
            zerolinecolor=grid_col,
            color=text_col
        ),
        legend=dict(
            x=0.01, y=0.99,
            bgcolor=card_bg,
            bordercolor=grid_col
        ),
        margin=dict(l=40, r=40, t=60, b=40)
    )
    
    return fig
