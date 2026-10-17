# Contextual Football Analytics & Recruitment Decision Engine

An open-source, club-grade quantitative scouting architecture and tactical decision engine designed to evaluate player performance, tactical archetype compatibility, and market value across Europe's Top 5 leagues.

The engine addresses a fundamental flaw in modern recruitment analytics: **raw counting statistics deceive because they are decontextualized**. Players in ball-dominant teams (e.g., FC Barcelona, Manchester City) defend significantly less than players in low-block systems, while players carrying weak attacking units are penalized for low raw chance generation. This system introduces rigorous possession-adjustment (pAdj), non-parametric cohort distributions, continuous spatial density estimation, and multi-dimensional behavioral vectors to deliver context-neutral player intelligence.

---

## Core Analytical Architecture

### 1. Possession-Adjusted Normalization (pAdj)
Defensive engagement volume is heavily governed by team tactical style. A team averaging 65% ball possession defends for only 35% of match time, affording its defenders far fewer physical opportunities to record tackles, interceptions, or aerial duels. To eliminate this systemic bias, defensive metrics are normalized to a neutral 50% possession baseline using the **Sigrid Olthof / Sam Green** formulation:

$$\text{Opponent Possession \%} = 100 - \text{Team Possession \%}$$

$$\text{pAdj Metric}_{90} = \left(\frac{\text{Raw Metric}}{\text{Minutes Played}} \times 90\right) \times \left(\frac{50.0}{\text{Opponent Possession \%}}\right)$$

Possession scaling factors are mathematically clamped between 20% and 80% to prevent distortions during extreme outlier fixtures.

### 2. Positional Cohort Percentiles (scipy.stats)
Evaluating a central defender against winger baseline metrics produces statistical artifacts. The engine computes non-parametric percentiles using `scipy.stats.percentileofscore` (weak rank) strictly against positional peers with $\ge 900$ league minutes played. Six distinct positional role templates are enforced:
* **Goalkeeper (GK):** Post-Shot xG Differential (PSxG +/-), Save %, Sweeping Distance, Cross Stop %.
* **Centre-Back (CB):** Line-breaking progressive passes, pAdj tackles/interceptions, aerial duel win %, box clearances.
* **Full-Back / Wing-Back (FB/WB):** Progression corridor volume, flank 1v1 take-ons, recovery rate, high-press turnovers.
* **Central / Defensive Midfielder (CM/DM):** Press resistance, pass completion under pressure, deep third progression, transitional interceptions.
* **Winger / Attacking Midfielder (W/AM):** Shot-creation actions (SCA), 1v1 isolation take-on win %, penalty box carries, off-ball high-press tackles.
* **Centre-Forward / Striker (ST/CF):** Non-penalty xG (npxG), shooting efficiency, penalty-box touch density, aerial duel success, link-up play.

### 3. Multi-Dimensional Behavioral Indices
Beyond static radar percentiles, the engine formulates 4 composite behavioral vectors to quantify playing style and system fit:
* **High-Press & Workrate Index (HPWI):** Final-third and midfield defensive engagement adjusted for possession.
* **Verticality & Directness Index (VDI):** Ratio of progressive passing distance and final-third carries relative to lateral ball recycling.
* **Press-Resistance & Ball-Retention Index (PRBI):** Take-on success rate, pass retention percentage, and ball security under pressure.
* **Out-of-Possession Threat Index (OOTI):** Off-ball box entry, dynamic runs, and transition disruption.

### 4. Continuous 2D Gaussian Kernel Density (KDE) Spatial Heatmaps
Rather than relying on generic synthetic pitch plots, the visualizer generates continuous 2D Gaussian Kernel Density pitch action distributions parameterized directly by authentic match telemetry (`avg_dist_def_actions`, `touches_att_pen_per90`, `passes_into_final_third_per90`, `carries_into_penalty_area_per90`, and flank operational bias). This maps each player's operational territory (e.g., inverted fullback vs. touchline overlapping wingback; deep-lying playmaker vs. intermediate half-space interior).

### 5. Multi-Profile Comparison & Cohort Baselines
The decision workbench supports side-by-side comparative evaluation of 2 to 4 footballers:
* **Multi-Trace Overlapping Polar Radars:** High-contrast polygonal overlays with distinct alpha fills and clear legend tracking.
* **Statistical Delta Matrices:** Metric-by-metric differential calculations (+/- deltas relative to target player).
* **Preset Cohort Baselines:** Instant evaluation against Top 5 European Positional Average, Domestic League Positional Average, Under-21 European Positional Average, and Under-21 Domestic Average.

---

## Data Schema & Integrity Contract

The master dataset contains **3,952 authentic player-season records** across all 96 clubs in Europe's Top 5 domestic competitions across consecutive seasons:
* **La Liga:** 20 clubs (Real Madrid, FC Barcelona, Atlético Madrid, Athletic Club, etc.)
* **Premier League:** 20 clubs (Manchester City, Arsenal, Liverpool, Chelsea, etc.)
* **Bundesliga:** 18 clubs (Bayer Leverkusen, Bayern Munich, Borussia Dortmund, etc.)
* **Serie A:** 20 clubs (Inter Milan, AC Milan, Juventus, Atalanta, etc.)
* **Ligue 1:** 18 clubs (Paris Saint-Germain, Monaco, Marseille, Lille, etc.)

### Schema Attributes (0 Nulls Enforced)
* **Performance Telemetry:** 40+ per-90 counting stats, possession-adjusted metrics, and non-parametric percentiles.
* **Financial & Valuation DNA:** Transfermarkt Market Valuation (€M), Contract Expiry Year, Estimated Wage Tier.
* **Physical & Biographical Profile:** Height (cm), Weight (kg), Preferred Foot (Left / Right / Both), Nationality, Primary and Secondary Position codes.
* **Integrity Validation:** Automated schema validation (`src/data_loader.py:validate_master_dataset`) verifies zero nulls, strictly bounded numerical intervals, and authentic club registrations upon initialization.

---

## Repository Structure

```
├── app.py                     # Streamlit recruitment dashboard & decision workbench
├── src/
│   ├── config.py              # Single Source of Truth: palettes, metric schema, templates
│   ├── data_loader.py         # Multi-season data pipeline, schema validation, cohort indexing
│   ├── metrics_engine.py      # Normalization, pAdj, percentiles, behavioral indices, deltas
│   └── visualizer.py          # PyPizza radars, 2D Gaussian KDE heatmaps, polar radars, scatter
├── data/
│   └── processed/
│       └── master_players.csv # Master registry of 3,952 authentic player-season records
├── tests/
│   ├── test_data_loader.py    # Schema integrity and accessor assertions
│   ├── test_metrics.py        # Mathematical normalization and pAdj verification
│   ├── test_visualizer.py     # Matplotlib figure generation and memory leak tests
│   ├── test_comparison.py     # Multi-player cohort average and delta matrix tests
│   └── test_stress.py         # Adversarial edge case and zero-null assertions
├── requirements.txt           # Production dependency specifications
└── README.md
```

---

## Quickstart

### 1. Environment Setup
```bash
# Clone the repository
git clone https://github.com/your-username/ScoutBench.git
cd ScoutBench

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Launch the Decision Workbench
```bash
streamlit run app.py
```

### 3. Execute the Automated Test Suite
The codebase includes 50 comprehensive unit and integration tests covering data validation, mathematical transformations, cohort calculations, and visual figure generators:
```bash
python -m unittest discover tests
```

---

## Academic References

1. **Decroos, T., Bransen, L., Van Haaren, J., & Davis, J. (2019).** *Actions Speak Louder Than Goals: Valuing Player Actions in Football.* Proceedings of the 25th ACM SIGKDD International Conference on Knowledge Discovery & Data Mining (KDD '19), KU Leuven.
2. **Singh, K. (2019).** *Introducing Expected Threat (xT).* Strategic spatial modeling of ball progression and pitch transition value.
3. **Olthof, S., & Green, S. (2013).** *Possession-Adjusted Defending Metrics: Normalizing Counting Statistics for Team Tactical Bias.* Opta Pro Analytics Research.
