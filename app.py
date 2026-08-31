"""
ScoutBench - Tactical Football Scouting & Player Dossier Workbench
Interactive Streamlit Application with autocomplete Search by Name and
hierarchical League -> Club -> Player filtering.
"""

import streamlit as st
import pandas as pd
import numpy as np

from src.data_loader import load_master_dataset, get_player_profile, get_cohort_peers
from src.config import (
    PIZZA_METRIC_TEMPLATES, 
    METRIC_LABELS, 
    DEFAULT_MIN_MINUTES,
    COLOR_PALETTES
)
from src.metrics_engine import (
    compute_player_percentiles, 
    extract_strengths_and_vulnerabilities, 
    classify_tactical_archetype
)
from src.visualizer import create_pizza_radar, create_quadrant_scatter

# -----------------------------------------------------------------------------
# Streamlit Page Configuration & Styling
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="ScoutBench | Football Scouting Workbench",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# Sidebar: Navigation & Filters
# -----------------------------------------------------------------------------
st.sidebar.title("⚽ ScoutBench")
st.sidebar.markdown("*Tactical Recruitment & Player Dossier Workbench*")
st.sidebar.markdown("---")

col_s1, col_s2 = st.sidebar.columns(2)
with col_s1:
    selected_season = st.selectbox("📅 Season", ["2025/26", "2024/25"], index=0)
with col_s2:
    min_minutes = st.number_input("Min Minutes", min_value=300, max_value=2500, value=900, step=100)

palette_names = list(COLOR_PALETTES.keys())
default_palette_idx = palette_names.index("The Athletic (Editorial Pitch)") if "The Athletic (Editorial Pitch)" in palette_names else 0
selected_palette_name = st.sidebar.selectbox("🎨 UI Color Theme", palette_names, index=default_palette_idx)
theme = COLOR_PALETTES[selected_palette_name]

# Custom CSS for Selected Color Theme
st.markdown(f"""
<style>
    .main {{
        background-color: {theme['canvas_bg']};
    }}
    .stApp {{
        background-color: {theme['canvas_bg']};
    }}
    .metric-card {{
        background-color: {theme['card_bg']};
        border-radius: 12px;
        padding: 16px;
        border: 1px solid {theme['border_color']};
        margin-bottom: 12px;
    }}
    .archetype-badge {{
        display: inline-block;
        background: {theme['accent_color']};
        color: {'#000000' if selected_palette_name in ['Opta Pro (Midnight Pitch)', 'DataMB Studio (Scandinavian Deep)'] else '#FFFFFF'};
        padding: 6px 14px;
        border-radius: 20px;
        font-weight: 800;
        font-size: 13px;
        margin-top: 5px;
        letter-spacing: 0.5px;
    }}
    .strength-badge {{
        background-color: {theme['slice_colors'].get('Defending & Pressing', '#10B981')}22;
        border: 1px solid {theme['slice_colors'].get('Defending & Pressing', '#10B981')};
        color: {theme['slice_colors'].get('Defending & Pressing', '#10B981')};
        padding: 5px 12px;
        border-radius: 6px;
        font-size: 13px;
        margin: 4px 0;
        font-weight: 600;
    }}
    .vuln-badge {{
        background-color: {theme['accent_color']}22;
        border: 1px solid {theme['accent_color']};
        color: {theme['accent_color']};
        padding: 5px 12px;
        border-radius: 6px;
        font-size: 13px;
        margin: 4px 0;
        font-weight: 600;
    }}
</style>
""", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# Data Loading & Initialization
# -----------------------------------------------------------------------------
@st.cache_data
def get_dataset(min_mins: int):
    return load_master_dataset(min_minutes=min_mins)

@st.cache_data
def build_search_index(min_mins: int, season: str):
    """Build a lookup dict mapping player name -> 'Player (Club · Position)' for the selectbox display."""
    data = load_master_dataset(min_minutes=min_mins)
    if "season" in data.columns:
        data = data[data["season"] == season]
    lookup = {}
    for _, row in data.iterrows():
        lookup[row["player"]] = f"{row['player']}  —  {row['team']} · {row['position']}"
    return lookup

df_all = get_dataset(min_minutes)
df = df_all[df_all["season"] == selected_season].copy() if "season" in df_all.columns else df_all
search_index = build_search_index(min_minutes, selected_season)

# Search Mode Selector
search_mode = st.sidebar.radio(
    "Navigation Method",
    ["🔍 Search by Name", "📂 League & Club Filter"],
    horizontal=True
)

if search_mode == "🔍 Search by Name":
    st.sidebar.markdown("#### Search Player")
    all_names = sorted(df["player"].unique().tolist())
    chosen = st.sidebar.selectbox(
        "Start typing a player name...",
        options=all_names,
        index=None,
        placeholder="e.g. Pedri, Lamine Yamal, Cubarsi, Rodri...",
        format_func=lambda p: search_index.get(p, p),
        key="name_search"
    )
    if chosen is not None:
        st.session_state.target_player = chosen

else:  # Hierarchical Browser (League -> Club -> Player)
    st.sidebar.markdown("#### Browse by League & Club")

    # 1. League selector
    leagues = sorted(df["league"].unique().tolist())
    default_lg = leagues.index("La Liga") if "La Liga" in leagues else 0
    selected_league = st.sidebar.selectbox("1. Select League", leagues, index=default_lg)

    league_df = df[df["league"] == selected_league]

    # 2. Club selector (strictly filtered by league)
    clubs = sorted(league_df["team"].unique().tolist())
    default_club = clubs.index("Barcelona") if "Barcelona" in clubs else 0
    selected_club = st.sidebar.selectbox("2. Select Club", clubs, index=default_club)

    club_df = league_df[league_df["team"] == selected_club]

    # 3. Player selector (strictly filtered by club)
    club_players = sorted(club_df["player"].unique().tolist())
    if club_players:
        prev = st.session_state.get("target_player")
        default_pl = club_players.index(prev) if prev in club_players else 0
        chosen_player = st.sidebar.selectbox("3. Select Player", club_players, index=default_pl)
        st.session_state.target_player = chosen_player
    else:
        st.sidebar.warning("No players in this club meet the minimum minutes filter.")

st.sidebar.markdown("---")
st.sidebar.info(
    "ScoutBench features **6 specialized positional templates** (Goalkeeper, Centreback, Fullback, "
    "Central Midfielder, Winger/AM, Striker) with pAdj normalization — matching DataMB standards."
)

# -----------------------------------------------------------------------------
# Main Application Content: Player Dossier
# -----------------------------------------------------------------------------
target_player_name = st.session_state.get("target_player", None)

if target_player_name is None:
    st.markdown("## 👋 Welcome to ScoutBench")
    st.markdown("Select a player using **Search by Name** or the **League & Club Filter** in the sidebar to view their tactical dossier.")
    st.stop()

player_row = get_player_profile(df, target_player_name)

if player_row is not None:
    pos_group = player_row["position_group"]
    
    # Load the specialized metric template for this exact position role
    template_key = pos_group if pos_group in PIZZA_METRIC_TEMPLATES else "Central / Defensive Midfielder"
    metric_categories = PIZZA_METRIC_TEMPLATES[template_key]
    
    # Extract flat list of metrics in this template
    template_metrics = [m for sublist in metric_categories.values() for m in sublist]
    
    # Get cohort peers for percentile calculation
    cohort_df = get_cohort_peers(df, pos_group)
    percentiles = compute_player_percentiles(player_row, cohort_df, template_metrics)
    
    # Classify archetype and extract traits
    archetype = classify_tactical_archetype(percentiles, pos_group)
    strengths, vulnerabilities = extract_strengths_and_vulnerabilities(percentiles)
    
    # ---------------------------------------------------------------------
    # 1. Header & Player Overview Banner
    # ---------------------------------------------------------------------
    col_title, col_badge = st.columns([3, 1.2])
    with col_title:
        st.title(f"{player_row['player']}")
        st.markdown(
            f"**Club:** `{player_row['team']}` | **League:** `{player_row['league']}` | "
            f"**Position:** `{pos_group}` | **Age:** `{player_row['age']}` | "
            f"**Minutes:** `{player_row['minutes']:,}` | **Team Poss:** `{player_row['team_possession_pct']}%`"
        )
    with col_badge:
        st.markdown("<div style='text-align: right;'>", unsafe_allow_html=True)
        st.markdown(f"<span class='archetype-badge'>🏷️ {archetype}</span>", unsafe_allow_html=True)
        st.markdown(f"<p style='color:#A0AEC0; font-size:12px; margin-top:5px;'>Positional Cohort: <b>{pos_group}</b> ({len(cohort_df)} peers)</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    st.markdown("---")
    
    # ---------------------------------------------------------------------
    # 2. Main Content: Pizza Radar & Tactical Insights
    # ---------------------------------------------------------------------
    col_radar, col_insights = st.columns([1.6, 1])
    
    with col_radar:
        st.subheader("🎯 Tactical Percentile Radar")
        fig_pizza = create_pizza_radar(
            player_name=player_row["player"],
            team_name=player_row["team"],
            league_name=player_row["league"],
            season=player_row.get("season", "2025/26"),
            archetype=archetype,
            minutes=player_row["minutes"],
            categories=metric_categories,
            percentiles=percentiles,
            palette=theme
        )
        st.pyplot(fig_pizza, width="stretch")
        
    with col_insights:
        st.subheader("📊 Tactical Profile Breakdown")
        
        st.markdown("#### 🟢 Elite Strengths (≥80th %ile)")
        if strengths:
            for s in strengths[:5]:
                st.markdown(
                    f"<div class='strength-badge'><b>{s['label']}</b>: {s['percentile']}%ile</div>", 
                    unsafe_allow_html=True
                )
        else:
            st.write("Balanced performance across standard metrics.")
            
        st.markdown("#### 🔴 Tactical Vulnerabilities (≤35th %ile)")
        if vulnerabilities:
            for v in vulnerabilities[:5]:
                st.markdown(
                    f"<div class='vuln-badge'><b>{v['label']}</b>: {v['percentile']}%ile</div>", 
                    unsafe_allow_html=True
                )
        else:
            st.write("No major statistical deficiencies in cohort.")
            
        st.markdown("---")
        st.markdown("#### 📋 Core Statistical Snapshot")
        
        # Contextual snapshot based on position role
        if pos_group == "Goalkeeper":
            st.markdown(f"""
            - **PSxG +/- (Shot Stopping) / 90:** `{player_row.get('psxg_net_per90', 0)}` ({percentiles.get('psxg_net_per90', 50)}%ile)
            - **Save Percentage:** `{player_row.get('save_pct', 0)}%` ({percentiles.get('save_pct', 50)}%ile)
            - **Long Pass Distribution %:** `{player_row.get('passes_completed_long_pct', 0)}%` ({percentiles.get('passes_completed_long_pct', 50)}%ile)
            - **Sweeper Keeper Actions / 90:** `{player_row.get('def_actions_outside_pen_per90', 0)}` ({percentiles.get('def_actions_outside_pen_per90', 50)}%ile)
            - **Crosses Claimed / Stopped %:** `{player_row.get('crosses_stopped_pct', 0)}%` ({percentiles.get('crosses_stopped_pct', 50)}%ile)
            """)
        elif pos_group == "Centreback":
            st.markdown(f"""
            - **Progressive Passes / 90:** `{player_row.get('progressive_passes_per90', 0)}` ({percentiles.get('progressive_passes_per90', 50)}%ile)
            - **Prog. Passing Distance / 90:** `{player_row.get('progressive_passing_distance_per90', 0)}m` ({percentiles.get('progressive_passing_distance_per90', 50)}%ile)
            - **Pass Completion %:** `{player_row.get('pass_completion_pct', 0)}%` ({percentiles.get('pass_completion_pct', 50)}%ile)
            - **Aerial Duel Win %:** `{player_row.get('aerial_win_pct', 0)}%` ({percentiles.get('aerial_win_pct', 50)}%ile)
            - **pAdj Tackles + Interceptions:** `{player_row.get('padj_tackles_per90', 0)} / {player_row.get('padj_interceptions_per90', 0)}`
            """)
        elif pos_group == "Centre-Forward / Striker":
            st.markdown(f"""
            - **Non-Penalty xG / 90:** `{player_row.get('npxG_per90', 0)}` ({percentiles.get('npxG_per90', 50)}%ile)
            - **Shots on Target %:** `{player_row.get('shots_on_target_pct', 0)}%` ({percentiles.get('shots_on_target_pct', 50)}%ile)
            - **Touches in Penalty Box / 90:** `{player_row.get('touches_att_pen_per90', 0)}` ({percentiles.get('touches_att_pen_per90', 50)}%ile)
            - **Shot-Creating Actions (SCA) / 90:** `{player_row.get('sca_per90', 0)}` ({percentiles.get('sca_per90', 50)}%ile)
            - **Aerial Duel Win %:** `{player_row.get('aerial_win_pct', 0)}%` ({percentiles.get('aerial_win_pct', 50)}%ile)
            """)
        else:
            st.markdown(f"""
            - **Progressive Passes / 90:** `{player_row.get('progressive_passes_per90', 0)}` ({percentiles.get('progressive_passes_per90', 50)}%ile)
            - **Progressive Carries / 90:** `{player_row.get('progressive_carries_per90', 0)}` ({percentiles.get('progressive_carries_per90', 50)}%ile)
            - **Shot-Creating Actions (SCA) / 90:** `{player_row.get('sca_per90', 0)}` ({percentiles.get('sca_per90', 50)}%ile)
            - **Pass Completion Rate:** `{player_row.get('pass_completion_pct', 0)}%` ({percentiles.get('pass_completion_pct', 50)}%ile)
            - **pAdj Ball Recoveries / 90:** `{player_row.get('ball_recoveries_per90', 0)}` ({percentiles.get('ball_recoveries_per90', 50)}%ile)
            """)

    # ---------------------------------------------------------------------
    # 3. Interactive Quadrant Scatter Benchmark
    # ---------------------------------------------------------------------
    st.markdown("---")
    st.subheader("📈 Cohort Quadrant Benchmark")
    st.markdown(f"Compare **{player_row['player']}** against all **{len(cohort_df)}** players in the **{pos_group}** cohort.")
    
    col_x, col_y = st.columns(2)
    
    # Only offer metrics that exist for this positional cohort
    valid_cohort_metrics = [m for m in template_metrics if m in cohort_df.columns]
    
    if pos_group == "Goalkeeper":
        default_x = valid_cohort_metrics.index("save_pct") if "save_pct" in valid_cohort_metrics else 0
        default_y = valid_cohort_metrics.index("psxg_net_per90") if "psxg_net_per90" in valid_cohort_metrics else 1
    elif pos_group == "Centreback":
        default_x = valid_cohort_metrics.index("pass_completion_pct") if "pass_completion_pct" in valid_cohort_metrics else 0
        default_y = valid_cohort_metrics.index("progressive_passes_per90") if "progressive_passes_per90" in valid_cohort_metrics else 1
    elif pos_group == "Centre-Forward / Striker":
        default_x = valid_cohort_metrics.index("touches_att_pen_per90") if "touches_att_pen_per90" in valid_cohort_metrics else 0
        default_y = valid_cohort_metrics.index("npxG_per90") if "npxG_per90" in valid_cohort_metrics else 1
    elif pos_group == "Winger / Attacking Mid":
        default_x = valid_cohort_metrics.index("take_ons_attempted_per90") if "take_ons_attempted_per90" in valid_cohort_metrics else 0
        default_y = valid_cohort_metrics.index("sca_per90") if "sca_per90" in valid_cohort_metrics else 1
    else:
        default_x = valid_cohort_metrics.index("pass_completion_pct") if "pass_completion_pct" in valid_cohort_metrics else 0
        default_y = valid_cohort_metrics.index("progressive_passes_per90") if "progressive_passes_per90" in valid_cohort_metrics else 1

    with col_x:
        selected_x = st.selectbox("X-Axis Metric", valid_cohort_metrics, index=default_x, format_func=lambda m: METRIC_LABELS.get(m, m))
    with col_y:
        selected_y = st.selectbox("Y-Axis Metric", valid_cohort_metrics, index=default_y, format_func=lambda m: METRIC_LABELS.get(m, m))
        
    fig_scatter = create_quadrant_scatter(
        df=cohort_df,
        x_metric=selected_x,
        y_metric=selected_y,
        target_player=target_player_name,
        position_group=pos_group,
        palette=theme
    )
    st.plotly_chart(fig_scatter, width="stretch")
