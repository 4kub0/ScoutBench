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
    compute_tactical_spectrum,
    compute_behavioral_indexes,
    classify_tactical_archetype,
    extract_strengths_and_vulnerabilities,
    generate_scouting_intelligence,
    compute_cohort_benchmark,
    compute_comparison_deltas
)
from src.visualizer import (
    create_pizza_radar, 
    create_pitch_heatmap, 
    create_quadrant_scatter,
    create_multi_player_radar
)

# Helper: convert hex to rgba (avoids browser-dependent hex-alpha appending)
def _hex_to_rgba(hex_code: str, alpha: float) -> str:
    h = hex_code.lstrip("#")
    return f"rgba({int(h[0:2], 16)}, {int(h[2:4], 16)}, {int(h[4:6], 16)}, {alpha})"

# Streamlit Page Configuration & Styling
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="ScoutBench | Football Scouting Workbench",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# Sidebar: Navigation & Filters
# -----------------------------------------------------------------------------
st.sidebar.title("ScoutBench")
st.sidebar.caption("Tactical scouting workbench")

# Reserve a container at the top for search (populated after data loads)
_search_container = st.sidebar.container()

st.sidebar.markdown("---")
col_s1, col_s2 = st.sidebar.columns(2)
with col_s1:
    selected_season = st.selectbox("Season", ["2025/26", "2024/25"], index=0)
with col_s2:
    min_minutes = st.number_input("Min Minutes", min_value=300, max_value=2500, value=900, step=100)

palette_names = ["The Athletic", "Opta Dark", "Monochrome", "DataMB"]
default_palette_idx = palette_names.index("The Athletic") if "The Athletic" in palette_names else 0
selected_palette_name = st.sidebar.selectbox("Theme", palette_names, index=default_palette_idx)
theme = COLOR_PALETTES[selected_palette_name]

# Custom CSS for Selected Color Theme
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
    .stApp {{
        background-color: {theme['canvas_bg']};
        font-family: 'Inter', 'Segoe UI', -apple-system, system-ui, sans-serif;
    }}
    .main {{
        background-color: {theme['canvas_bg']};
    }}
    .main h3 {{
        margin-top: 48px;
        margin-bottom: 16px;
    }}
    .archetype-badge {{
        display: inline-block;
        background: {theme['accent_color']};
        color: {'#000000' if selected_palette_name in ['Opta Dark', 'DataMB'] else '#FFFFFF'};
        padding: 6px 14px;
        border-radius: 20px;
        font-weight: 800;
        font-size: 13px;
        margin-top: 5px;
        letter-spacing: 0.5px;
    }}
    .secondary-badge {{
        display: inline-block;
        background: {theme['card_bg']};
        border: 1px solid {theme['text_secondary']};
        color: {theme['text_secondary']};
        padding: 4px 10px;
        border-radius: 16px;
        font-weight: 600;
        font-size: 11px;
        margin-top: 4px;
    }}
    .strength-badge {{
        background-color: {_hex_to_rgba(theme.get('positive_color', '#10B981'), 0.13)};
        border: 1px solid {theme.get('positive_color', '#10B981')};
        color: {theme.get('positive_color', '#10B981')};
        padding: 6px 12px;
        border-radius: 8px;
        font-size: 13px;
        margin: 4px 0;
        font-weight: 600;
    }}
    .vuln-badge {{
        background-color: {_hex_to_rgba(theme.get('negative_color', '#E06D53'), 0.13)};
        border: 1px solid {theme.get('negative_color', '#E06D53')};
        color: {theme.get('negative_color', '#E06D53')};
        padding: 6px 12px;
        border-radius: 8px;
        font-size: 13px;
        margin: 4px 0;
        font-weight: 600;
    }}
    .intel-note-positive {{
        background-color: {_hex_to_rgba(theme.get('positive_color', '#10B981'), 0.09)};
        border-left: 4px solid {theme.get('positive_color', '#10B981')};
        padding: 10px 14px;
        border-radius: 0 8px 8px 0;
        margin-bottom: 10px;
        font-size: 13px;
    }}
    .intel-note-warning {{
        background-color: {_hex_to_rgba(theme.get('negative_color', '#E06D53'), 0.09)};
        border-left: 4px solid {theme.get('negative_color', '#E06D53')};
        padding: 10px 14px;
        border-radius: 0 8px 8px 0;
        margin-bottom: 10px;
        font-size: 13px;
    }}
    .intel-note-neutral {{
        background-color: {_hex_to_rgba(theme['border_color'], 0.40)};
        border-left: 4px solid {theme['text_secondary']};
        padding: 10px 14px;
        border-radius: 0 8px 8px 0;
        margin-bottom: 10px;
        font-size: 13px;
    }}
    .index-box {{
        background-color: {theme['card_bg']};
        border: 1px solid {theme['border_color']};
        border-radius: 10px;
        padding: 14px;
        text-align: center;
    }}
    .index-title {{
        font-size: 12px;
        color: {theme['text_secondary']};
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 4px;
    }}
    .index-value {{
        font-size: 24px;
        font-weight: 800;
        color: {theme['text_primary']};
    }}
    .profile-bar-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
        gap: 12px;
        background-color: {theme['card_bg']};
        border: 1px solid {theme['border_color']};
        border-radius: 8px;
        padding: 14px 18px;
        margin-top: 14px;
        margin-bottom: 18px;
    }}
    .profile-item {{
        display: flex;
        flex-direction: column;
    }}
    .profile-label {{
        font-size: 10px;
        font-weight: 700;
        color: {theme['text_secondary']};
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-bottom: 3px;
    }}
    .profile-value {{
        font-size: 14px;
        font-weight: 700;
        color: {theme['text_primary']};
    }}
    .stat-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
        gap: 10px;
        margin-top: 8px;
        margin-bottom: 12px;
    }}
    .stat-cell {{
        background-color: {theme['card_bg']};
        border: 1px solid {theme['border_color']};
        border-radius: 8px;
        padding: 10px 14px;
    }}
    .stat-cell-label {{
        font-size: 10px;
        font-weight: 700;
        color: {theme['text_secondary']};
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 4px;
    }}
    .stat-cell-value {{
        font-size: 16px;
        font-weight: 800;
        color: {theme['text_primary']};
    }}
    .stat-cell-pct {{
        font-size: 11px;
        color: {theme['text_secondary']};
        font-weight: 600;
    }}
    .delta-table-container {{
        width: 100%;
        border-collapse: collapse;
        margin-top: 15px;
        margin-bottom: 25px;
        font-size: 13px;
    }}
    .delta-table-container th {{
        background-color: {theme['card_bg']};
        color: {theme['text_secondary']};
        font-weight: 700;
        text-transform: uppercase;
        font-size: 11px;
        letter-spacing: 0.5px;
        padding: 10px 12px;
        border-bottom: 2px solid {theme['border_color']};
        text-align: left;
    }}
    .delta-table-container td {{
        padding: 10px 12px;
        border-bottom: 1px solid {theme['border_color']};
        color: {theme['text_primary']};
    }}
    .delta-table-container tr:hover {{
        background-color: {_hex_to_rgba(theme['card_bg'], 0.53)};
    }}
    .delta-pos {{
        color: {theme.get('positive_color', '#10B981')};
        font-weight: 700;
    }}
    .delta-neg {{
        color: {theme.get('negative_color', '#E06D53')};
        font-weight: 700;
    }}
    .delta-neu {{
        color: {theme['text_secondary']};
        font-weight: 600;
    }}
    .comp-index-card {{
        background-color: {theme['card_bg']};
        border: 1px solid {theme['border_color']};
        border-radius: 10px;
        padding: 14px;
        margin-bottom: 12px;
    }}
    .comp-index-header {{
        font-size: 12px;
        font-weight: 700;
        color: {theme['text_secondary']};
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 8px;
        border-bottom: 1px solid {theme['border_color']};
        padding-bottom: 4px;
    }}
    .comp-index-row {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 6px;
        font-size: 13px;
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

# Populate the search container (renders at the top of sidebar)
with _search_container:
    search_mode = st.radio(
        "Find Player",
        ["Search", "Browse"],
        horizontal=True
    )

    if search_mode == "Search":
        all_names = sorted(df["player"].unique().tolist())
        chosen = st.selectbox(
            "Player",
            options=all_names,
            index=None,
            placeholder="Search by name...",
            format_func=lambda p: search_index.get(p, p),
            key="name_search"
        )
        if chosen is not None:
            st.session_state.target_player = chosen

    else:  # Browse
        leagues = sorted(df["league"].unique().tolist())
        default_lg = leagues.index("La Liga") if "La Liga" in leagues else 0
        selected_league = st.selectbox("League", leagues, index=default_lg)

        league_df = df[df["league"] == selected_league]

        clubs = sorted(league_df["team"].unique().tolist())
        default_club = clubs.index("Barcelona") if "Barcelona" in clubs else 0
        selected_club = st.selectbox("Club", clubs, index=default_club)

        club_df = league_df[league_df["team"] == selected_club]

        club_players = sorted(club_df["player"].unique().tolist())
        if club_players:
            prev = st.session_state.get("target_player")
            default_pl = club_players.index(prev) if prev in club_players else 0
            chosen_player = st.selectbox("Player", club_players, index=default_pl)
            st.session_state.target_player = chosen_player
        else:
            st.warning("No players in this club meet the minimum minutes filter.")

with st.sidebar.expander("About ScoutBench"):
    st.info(
        "Features **6 positional templates** (Goalkeeper, Centreback, Fullback, "
        "Central Midfielder, Winger/AM, Striker) with pAdj normalization and continuous tactical spectrums."
    )

# -----------------------------------------------------------------------------
# Main Application Content: Player Dossier
# -----------------------------------------------------------------------------
target_player_name = st.session_state.get("target_player", None)

if target_player_name is None:
    st.markdown("## Welcome to ScoutBench")
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
    
    # Continuous Tactical Spectrum & Universal Behavioral Indexes
    spectrum = compute_tactical_spectrum(percentiles, pos_group)
    behavioral_indexes = compute_behavioral_indexes(percentiles, pos_group)
    archetype = spectrum["primary_archetype"]
    secondary_archetype = spectrum.get("secondary_archetype")
    
    # Deep Scouting Intelligence Report
    scouting_intel = generate_scouting_intelligence(
        player_row=player_row,
        percentiles=percentiles,
        spectrum=spectrum,
        behavioral_indexes=behavioral_indexes,
        position_group=pos_group
    )
    
    # -------------------------------------------------------------------------
    # 0. Dossier Header & Profile Overview
    # -------------------------------------------------------------------------
    st.title(f"{player_row['player']}")
    badge_html = f"<span class='archetype-badge'>{archetype}</span>"
    if secondary_archetype:
        badge_html += f" <span class='secondary-badge'>Tendency: {secondary_archetype}</span>"
    badge_html += f" <span style='color:{theme['text_secondary']}; font-size:11px; margin-left:12px;'>{pos_group} · {len(cohort_df)} peers</span>"
    st.markdown(badge_html, unsafe_allow_html=True)
    st.markdown(
        f"**{player_row['team']}** · {player_row['league']} · "
        f"Age {player_row['age']} · {player_row['minutes']:,} min · "
        f"{player_row['team_possession_pct']}% team possession"
    )

    # 3-Layer Charcoal Header Profile Bar (R1)
    market_val = player_row.get("market_value_eur", 0)
    if pd.notna(market_val) and market_val > 0:
        if market_val >= 1_000_000:
            market_val_str = f"€{market_val / 1_000_000:.1f}M"
        elif market_val >= 1_000:
            market_val_str = f"€{market_val / 1_000:.0f}k"
        else:
            market_val_str = f"€{int(market_val)}"
    else:
        market_val_str = "N/A"

    expiry_val = player_row.get("contract_expiry", "N/A")
    expiry_str = str(int(expiry_val)) if pd.notna(expiry_val) and isinstance(expiry_val, (int, float)) else str(expiry_val)
    wage_tier_str = str(player_row.get("wage_tier", "N/A"))

    height_val = player_row.get("height_cm", "N/A")
    weight_val = player_row.get("weight_kg", "N/A")
    if pd.notna(height_val) and pd.notna(weight_val):
        physical_dna_str = f"{int(height_val)} cm · {int(weight_val)} kg"
    else:
        physical_dna_str = "N/A"

    foot_str = str(player_row.get("preferred_foot", "N/A"))
    nationality_str = str(player_row.get("nationality", "N/A"))

    pri_pos = str(player_row.get("primary_position", "N/A"))
    sec_pos = str(player_row.get("secondary_position", "None"))
    if sec_pos and sec_pos != "None" and sec_pos != pri_pos:
        role_codes_str = f"{pri_pos} · {sec_pos}"
    else:
        role_codes_str = pri_pos

    st.markdown(f"""
    <div class='profile-bar-grid'>
        <div class='profile-item'>
            <span class='profile-label'>Market Value</span>
            <span class='profile-value'>{market_val_str}</span>
        </div>
        <div class='profile-item'>
            <span class='profile-label'>Contract Until</span>
            <span class='profile-value'>{expiry_str}</span>
        </div>
        <div class='profile-item'>
            <span class='profile-label'>Wage Band</span>
            <span class='profile-value'>{wage_tier_str}</span>
        </div>
        <div class='profile-item'>
            <span class='profile-label'>Height / Weight</span>
            <span class='profile-value'>{physical_dna_str}</span>
        </div>
        <div class='profile-item'>
            <span class='profile-label'>Preferred Foot</span>
            <span class='profile-value'>{foot_str}</span>
        </div>
        <div class='profile-item'>
            <span class='profile-label'>Nationality</span>
            <span class='profile-value'>{nationality_str}</span>
        </div>
        <div class='profile-item'>
            <span class='profile-label'>Positions</span>
            <span class='profile-value'>{role_codes_str}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
        
    # =========================================================================
    # CARD 1: PyPizza Tactical Radar & Continuous Pitch Action Heatmap (Side-by-Side)
    # =========================================================================
    st.markdown("### Tactical Profile")
    
    col_radar, col_heatmap = st.columns([1.15, 1])
    
    with col_radar:
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
        
    with col_heatmap:
        fig_heatmap = create_pitch_heatmap(
            player_row=player_row,
            position_group=pos_group,
            palette=theme
        )
        st.pyplot(fig_heatmap, width="stretch")
        
    # Core Statistical Snapshot grid directly beneath the dual canvases
    st.markdown("#### Core Stats")
    if pos_group == "Goalkeeper":
        core_stats = [
            ("PSxG Net / 90", f"{player_row.get('psxg_net_per90', 0)}", percentiles.get('psxg_net_per90', 50)),
            ("Save %", f"{player_row.get('save_pct', 0)}%", percentiles.get('save_pct', 50)),
            ("Long Pass %", f"{player_row.get('passes_completed_long_pct', 0)}%", percentiles.get('passes_completed_long_pct', 50)),
            ("Sweeper Actions / 90", f"{player_row.get('def_actions_outside_pen_per90', 0)}", percentiles.get('def_actions_outside_pen_per90', 50)),
            ("Crosses Claimed %", f"{player_row.get('crosses_stopped_pct', 0)}%", percentiles.get('crosses_stopped_pct', 50)),
            ("Def Action Distance", f"{player_row.get('avg_dist_def_actions', 0)}m", percentiles.get('avg_dist_def_actions', 50)),
        ]
    elif pos_group == "Centreback":
        core_stats = [
            ("Prog. Passes / 90", f"{player_row.get('progressive_passes_per90', 0)}", percentiles.get('progressive_passes_per90', 50)),
            ("Prog. Distance / 90", f"{player_row.get('progressive_passing_distance_per90', 0)}m", percentiles.get('progressive_passing_distance_per90', 50)),
            ("Pass Completion %", f"{player_row.get('pass_completion_pct', 0)}%", percentiles.get('pass_completion_pct', 50)),
            ("Aerial Duel Win %", f"{player_row.get('aerial_win_pct', 0)}%", percentiles.get('aerial_win_pct', 50)),
            ("pAdj Tackles / 90", f"{player_row.get('padj_tackles_per90', 0)}", percentiles.get('padj_tackles_per90', 50)),
            ("pAdj Interceptions / 90", f"{player_row.get('padj_interceptions_per90', 0)}", percentiles.get('padj_interceptions_per90', 50)),
        ]
    elif pos_group == "Centre-Forward / Striker":
        core_stats = [
            ("Non-Penalty xG / 90", f"{player_row.get('npxG_per90', 0)}", percentiles.get('npxG_per90', 50)),
            ("Shots on Target %", f"{player_row.get('shots_on_target_pct', 0)}%", percentiles.get('shots_on_target_pct', 50)),
            ("Box Touches / 90", f"{player_row.get('touches_att_pen_per90', 0)}", percentiles.get('touches_att_pen_per90', 50)),
            ("SCA / 90", f"{player_row.get('sca_per90', 0)}", percentiles.get('sca_per90', 50)),
            ("Aerial Duel Win %", f"{player_row.get('aerial_win_pct', 0)}%", percentiles.get('aerial_win_pct', 50)),
            ("Att 3rd Tackles / 90", f"{player_row.get('tackles_att_3rd_per90', 0)}", percentiles.get('tackles_att_3rd_per90', 50)),
        ]
    else:
        core_stats = [
            ("Prog. Passes / 90", f"{player_row.get('progressive_passes_per90', 0)}", percentiles.get('progressive_passes_per90', 50)),
            ("Prog. Carries / 90", f"{player_row.get('progressive_carries_per90', 0)}", percentiles.get('progressive_carries_per90', 50)),
            ("SCA / 90", f"{player_row.get('sca_per90', 0)}", percentiles.get('sca_per90', 50)),
            ("Pass Completion %", f"{player_row.get('pass_completion_pct', 0)}%", percentiles.get('pass_completion_pct', 50)),
            ("Ball Recoveries / 90", f"{player_row.get('ball_recoveries_per90', 0)}", percentiles.get('ball_recoveries_per90', 50)),
            ("pAdj Tackles / 90", f"{player_row.get('padj_tackles_per90', 0)}", percentiles.get('padj_tackles_per90', 50)),
        ]

    cells_html = "".join([
        f"<div class='stat-cell'>"
        f"<div class='stat-cell-label'>{lbl}</div>"
        f"<div class='stat-cell-value'>{val}</div>"
        f"<div class='stat-cell-pct'>{pct:.0f}%ile cohort</div>"
        f"</div>"
        for lbl, val, pct in core_stats
    ])
    st.markdown(f"<div class='stat-grid'>{cells_html}</div>", unsafe_allow_html=True)
            
    st.caption("*pAdj normalized · Gaussian KDE spatial density*")

    # =========================================================================
    # CARD 2: Tactical Panel (Tactical Spectrum & Behavioral Indexes)
    # =========================================================================
    st.markdown("### Role Spectrum")
    
    col_spectrum, col_behavior = st.columns([1.2, 1.2])
    
    with col_spectrum:
        st.markdown(f"#### Tactical Role ({pos_group})")
        st.markdown("*Continuous attribute weighting derived from match actions (0–100):*")
        
        for axis in spectrum["axes"]:
            score_val = axis["score"]
            st.markdown(f"**{axis['name']}** — `{score_val:.0f}/100` *(Archetype: {axis['archetype']})*")
            st.progress(score_val / 100.0)
            st.caption(axis["description"])
            st.markdown("<div style='margin-bottom: 8px;'></div>", unsafe_allow_html=True)
            
    with col_behavior:
        st.markdown("#### Behavioral Indexes")
        st.markdown("*Off-the-ball intensity, retention, and progression (0–100):*")
        
        c_b1, c_b2 = st.columns(2)
        with c_b1:
            hpwi_val = behavioral_indexes["High-Press & Work-Rate"]["score"]
            st.markdown(f"""
            <div class='index-box'>
                <div class='index-title'>High-Press & Work-Rate</div>
                <div class='index-value'>{hpwi_val:.0f}<span style='font-size:14px; color:{theme['text_secondary']};'>/100</span></div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<div style='margin-bottom: 12px;'></div>", unsafe_allow_html=True)
            
            prbi_val = behavioral_indexes["Press-Resistance & Retention"]["score"]
            st.markdown(f"""
            <div class='index-box'>
                <div class='index-title'>Press-Resistance & Retention</div>
                <div class='index-value'>{prbi_val:.0f}<span style='font-size:14px; color:{theme['text_secondary']};'>/100</span></div>
            </div>
            """, unsafe_allow_html=True)
            
        with c_b2:
            vdi_val = behavioral_indexes["Verticality & Directness"]["score"]
            st.markdown(f"""
            <div class='index-box'>
                <div class='index-title'>Verticality & Directness</div>
                <div class='index-value'>{vdi_val:.0f}<span style='font-size:14px; color:{theme['text_secondary']};'>/100</span></div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<div style='margin-bottom: 12px;'></div>", unsafe_allow_html=True)
            
            ooti_val = behavioral_indexes["Offensive Threat & Opportunity"]["score"]
            st.markdown(f"""
            <div class='index-box'>
                <div class='index-title'>Offensive Threat & Burden</div>
                <div class='index-value'>{ooti_val:.0f}<span style='font-size:14px; color:{theme['text_secondary']};'>/100</span></div>
            </div>
            """, unsafe_allow_html=True)

    # =========================================================================
    # CARD 3: Deep Scouting Intelligence Card
    # =========================================================================
    st.markdown("### Scouting Report")
    
    col_traits, col_system = st.columns([1, 1.2])
    
    with col_traits:
        st.markdown("#### Strengths (≥80th %ile)")
        if scouting_intel["strengths"]:
            for s in scouting_intel["strengths"][:5]:
                st.markdown(
                    f"<div class='strength-badge'><b>{s['label']}</b>: {s['percentile']}%ile</div>", 
                    unsafe_allow_html=True
                )
        else:
            st.write("Balanced performance across standard positional metrics.")
            
        st.markdown("#### Vulnerabilities (≤35th %ile)")
        if scouting_intel["vulnerabilities"]:
            for v in scouting_intel["vulnerabilities"][:5]:
                st.markdown(
                    f"<div class='vuln-badge'><b>{v['label']}</b>: {v['percentile']}%ile</div>", 
                    unsafe_allow_html=True
                )
        else:
            st.write("No major statistical deficiencies in positional cohort.")
            
    with col_system:
        st.markdown("#### System Context")
        if scouting_intel["system_notes"]:
            for note in scouting_intel["system_notes"]:
                tone_class = f"intel-note-{note['tone']}"
                st.markdown(f"""
                <div class='{tone_class}'>
                    <b>{note['badge']}</b><br>
                    {note['text']}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.write("Standard tactical distribution profile across peer group.")

    # =========================================================================
    # CARD 4: Interactive Cohort Quadrant Benchmark
    # =========================================================================
    st.markdown("### Cohort Benchmark")
    st.markdown(f"**{player_row['player']}** vs. {len(cohort_df)} players in the **{pos_group}** positional cohort.")
    
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

    # =========================================================================
    # CARD 5: Dynamic Multi-Player & Cohort Comparison Tool (R2)
    # =========================================================================
    st.markdown("### Comparison")
    st.markdown(f"Compare **{player_row['player']}** against up to 3 players or cohort averages.")

    col_comp_players, col_comp_cohorts = st.columns([1.2, 1.0])
    
    all_comparison_names = [p for p in sorted(df["player"].unique().tolist()) if p != target_player_name]
    
    with col_comp_players:
        selected_comp_players = st.multiselect(
            "Select Comparison Footballer(s) (Up to 3):",
            options=all_comparison_names,
            max_selections=3,
            placeholder="Search players across all leagues & positions...",
            format_func=lambda p: search_index.get(p, p),
            key="multi_player_comparison_select"
        )
        
    with col_comp_cohorts:
        preset_options = [
            "Top 5 European Positional Average",
            f"Domestic ({player_row['league']}) Positional Average",
            "Under-21 European Positional Average",
            f"Under-21 Domestic ({player_row['league']}) Average"
        ]
        selected_presets = st.multiselect(
            "Toggle Preset Cohort Benchmark(s):",
            options=preset_options,
            placeholder="Select cohort baseline averages...",
            key="cohort_preset_comparison_select"
        )

    # Assemble compared profiles list
    compared_profiles = []
    
    # 1. Add selected individual players
    for cp_name in selected_comp_players:
        cp_row = get_player_profile(df, cp_name)
        if cp_row is not None:
            cp_pos = cp_row["position_group"]
            cp_cohort = get_cohort_peers(df, cp_pos)
            cp_pcts = compute_player_percentiles(cp_row, cp_cohort, template_metrics)
            cp_indexes = compute_behavioral_indexes(cp_pcts, cp_pos)
            compared_profiles.append({
                "name": f"{cp_row['player']} ({cp_row['team']})",
                "player_row": cp_row,
                "percentiles": cp_pcts,
                "indexes": cp_indexes,
                "is_benchmark": False
            })

    # 2. Add selected cohort benchmark averages
    for preset_label in selected_presets:
        try:
            if preset_label == "Top 5 European Positional Average":
                b_row = compute_cohort_benchmark(
                    df, position_group=pos_group, season=selected_season, benchmark_type="top5_positional"
                )
            elif preset_label.startswith("Domestic"):
                b_row = compute_cohort_benchmark(
                    df, position_group=pos_group, season=selected_season, benchmark_type="domestic_positional", domestic_league=player_row["league"]
                )
            elif preset_label == "Under-21 European Positional Average":
                b_row = compute_cohort_benchmark(
                    df_all, position_group=pos_group, season=selected_season, benchmark_type="u21_european"
                )
            elif preset_label.startswith("Under-21 Domestic"):
                b_row = compute_cohort_benchmark(
                    df_all, position_group=pos_group, season=selected_season, benchmark_type="u21_domestic", domestic_league=player_row["league"]
                )
            else:
                continue

            b_pcts = compute_player_percentiles(b_row, cohort_df, template_metrics)
            b_indexes = compute_behavioral_indexes(b_pcts, pos_group)
            compared_profiles.append({
                "name": str(b_row["player"]),
                "player_row": b_row,
                "percentiles": b_pcts,
                "indexes": b_indexes,
                "is_benchmark": True,
                "color": "#94A3B8"
            })
        except Exception as e:
            st.warning(f"Could not compute benchmark '{preset_label}': {e}")

    # Enforce maximum 3 comparison profiles (4 total on radar)
    if len(compared_profiles) > 3:
        st.info("Displaying the first 3 selected comparison profiles for radar chart readability (maximum 4 total profiles).")
        compared_profiles = compared_profiles[:3]

    if not compared_profiles:
        st.markdown(
            f"<div style='background-color:{theme['card_bg']}; border:1px dashed {theme['border_color']}; border-radius:8px; padding:20px; text-align:center; color:{theme['text_secondary']}; margin-top:15px;'>"
            f"Add players above to compare tactical profiles side by side."
            f"</div>",
            unsafe_allow_html=True
        )
    else:
        # Base target profile
        base_profile = {
            "name": f"{player_row['player']} (Base)",
            "player_row": player_row,
            "percentiles": percentiles,
            "indexes": behavioral_indexes,
            "is_benchmark": False,
            "color": theme.get("accent_color", "#E06D53")
        }
        all_radar_profiles = [base_profile] + compared_profiles

        # ---------------------------------------------------------------------
        # 5.1 Overlapping Multi-Trace Polar Radar Chart
        # ---------------------------------------------------------------------
        st.markdown("#### Overlapping Radar")
        st.markdown(f"*Comparing percentile ranks across {len(template_metrics)} positional metrics for **{len(all_radar_profiles)} profiles**:*")
        
        fig_multi_radar = create_multi_player_radar(
            profiles_data=all_radar_profiles,
            metrics=template_metrics,
            theme=theme
        )
        st.plotly_chart(fig_multi_radar, width="stretch")

        # ---------------------------------------------------------------------
        # 5.2 Side-by-Side Comparative Delta Table
        # ---------------------------------------------------------------------
        st.markdown("#### Delta Matrix")
        st.markdown(f"*Statistical differentials against base player (**{player_row['player']}**):*")

        delta_df = compute_comparison_deltas(
            base_row=player_row,
            base_percentiles=percentiles,
            compared_rows=[p["player_row"] for p in compared_profiles],
            compared_percentiles=[p["percentiles"] for p in compared_profiles],
            metrics=template_metrics
        )

        # Build clean HTML table
        table_html = [
            f"<div style='overflow-x:auto;'><table class='delta-table-container'>",
            "<thead><tr>",
            f"<th>Metric</th>",
            f"<th>{player_row['player']} (Base)</th>"
        ]

        for idx, comp_prof in enumerate(compared_profiles):
            slot = idx + 1
            comp_title = comp_prof["name"]
            table_html.append(f"<th>{comp_title}</th>")
            table_html.append(f"<th>Δ vs Base</th>")

        table_html.append("</tr></thead><tbody>")

        for _, row in delta_df.iterrows():
            m_label = row["metric_label"]
            b_val = row["base_val"]
            b_pct = row["base_pct"]

            table_html.append("<tr>")
            table_html.append(f"<td style='font-weight:600;'>{m_label}</td>")
            table_html.append(f"<td><b>{b_val:.2f}</b> <span style='color:{theme['text_secondary']}; font-size:11px;'>({b_pct:.0f}%ile)</span></td>")

            for idx in range(len(compared_profiles)):
                slot = idx + 1
                c_val = row.get(f"comp_{slot}_val", 0.0)
                c_pct = row.get(f"comp_{slot}_pct", 50.0)
                d_val = row.get(f"comp_{slot}_delta_val", 0.0)
                d_pct = row.get(f"comp_{slot}_delta_pct", 0.0)

                if d_val > 0.001:
                    delta_class = "delta-pos"
                    delta_str = f"+{d_val:.2f} (+{d_pct:.0f}%)"
                elif d_val < -0.001:
                    delta_class = "delta-neg"
                    delta_str = f"{d_val:.2f} ({d_pct:.0f}%)"
                else:
                    delta_class = "delta-neu"
                    delta_str = "0.00 (0%)"

                table_html.append(f"<td><b>{c_val:.2f}</b> <span style='color:{theme['text_secondary']}; font-size:11px;'>({c_pct:.0f}%ile)</span></td>")
                table_html.append(f"<td class='{delta_class}'>{delta_str}</td>")

            table_html.append("</tr>")

        table_html.append("</tbody></table></div>")
        st.markdown("".join(table_html), unsafe_allow_html=True)

        # ---------------------------------------------------------------------
        # 5.3 Comparative Behavioral Index Breakdown
        # ---------------------------------------------------------------------
        st.markdown("#### Behavioral Breakdown")
        st.markdown("*Side-by-side across 4 universal indexes (0–100):*")

        index_keys = [
            ("High-Press & Work-Rate", "HPWI"),
            ("Verticality & Directness", "VDI"),
            ("Press-Resistance & Retention", "PRBI"),
            ("Offensive Threat & Opportunity", "OOTI")
        ]

        b_cols = st.columns(4)
        for idx_col, (idx_full_name, idx_short) in enumerate(index_keys):
            with b_cols[idx_col]:
                base_score = behavioral_indexes.get(idx_full_name, {}).get("score", 50.0)
                
                card_html = [
                    f"<div class='comp-index-card'>",
                    f"<div class='comp-index-header'>{idx_short} · {idx_full_name}</div>",
                    f"<div class='comp-index-row'>",
                    f"<span><b>{player_row['player']}</b> (Base)</span>",
                    f"<span><b>{base_score:.0f}</b>/100</span>",
                    f"</div>"
                ]

                for comp_prof in compared_profiles:
                    c_name = comp_prof["name"]
                    c_score = comp_prof["indexes"].get(idx_full_name, {}).get("score", 50.0)
                    delta_score = c_score - base_score

                    if delta_score > 0:
                        d_style = f"color:{theme.get('positive_color', '#10B981')}; font-weight:700;"
                        d_text = f"+{delta_score:.0f}"
                    elif delta_score < 0:
                        d_style = f"color:{theme.get('negative_color', '#E06D53')}; font-weight:700;"
                        d_text = f"{delta_score:.0f}"
                    else:
                        d_style = f"color:{theme['text_secondary']}; font-weight:600;"
                        d_text = "0"

                    card_html.append(
                        f"<div class='comp-index-row'>"
                        f"<span style='color:{theme['text_secondary']}; font-size:12px;'>{c_name}</span>"
                        f"<span><b>{c_score:.0f}</b> <span style='{d_style}; font-size:11px;'>(Δ {d_text})</span></span>"
                        f"</div>"
                    )

                card_html.append("</div>")
                st.markdown("".join(card_html), unsafe_allow_html=True)
