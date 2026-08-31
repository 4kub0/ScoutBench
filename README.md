# ⚽ ScoutBench: Tactical Football Scouting & Player Dossier Workbench

**ScoutBench** is an open-source, club-grade football scouting and tactical analytics platform inspired by modern recruitment methodologies at data-driven European football clubs.

---

## 🌟 Key Features

* **Positional Percentile Radar Cards (PyPizza):** Dark-themed, publication-grade pizza plots rendered with `mplsoccer`, categorizing 15+ metrics into *Attacking & Creation*, *Possession & Progression*, and *Defending & Pressing*.
* **Possession-Adjusted Normalization (pAdj):** Implements the **Sigrid Olthof / Sam Green** formula to adjust defensive counting stats for team possession bias.
* **Tactical Archetype Classification:** Algorithmic badge tagging (*Deep Tempo Dictator*, *1v1 Isolation Winger*, *Ball-Playing High-Line CB*, *Box-to-Box Engine*) based on multi-dimensional percentile profiles.
* **Interactive Cohort Benchmarks (Plotly):** Dynamic quadrant scatterplots comparing any target player against their entire positional cohort across custom tactical axes with median thresholds.
* **Multi-League Coverage:** Full coverage across La Liga, Premier League, Bundesliga, Serie A, and Ligue 1.

---

## 🔬 Mathematical & Analytical Framework

### 1. Per-90 Normalization
All cumulative counting statistics are scaled to a standard 90-minute basis to ensure fair comparisons across players with varying playing time:
$$\text{Metric}_{90} = \left(\frac{\text{Raw Metric}}{\text{Minutes}}\right) \times 90$$

### 2. Possession-Adjustment (pAdj)
Dominant possession teams (e.g., FC Barcelona ~65% possession) spend significantly less time defending than counter-attacking teams. To avoid penalizing elite defenders on high-possession teams, defensive actions are normalized to a neutral 50% possession baseline:
$$\text{pAdj Metric}_{90} = \text{Metric}_{90} \times \left(\frac{50}{100 - \text{Team Possession \%}}\right)$$

### 3. Percentile Rank Engine
Calculated using `scipy.stats.percentileofscore` strictly against positional peers with $\ge 900$ minutes played to eliminate small-sample statistical noise.

---

## 🚀 Quickstart Guide

### 1. Installation
```bash
# Clone the repository
git clone https://github.com/your-username/ScoutBench.git
cd ScoutBench

# Install dependencies
pip install -r requirements.txt
```

### 2. Generate / Update Master Database
```bash
python scripts/build_dataset.py
```

### 3. Launch Interactive Workbench
```bash
streamlit run app.py
```

### 4. Run Unit Tests
```bash
python -m unittest discover tests
```

---

## 📚 Analytical References & Research
* **VAEP Framework:** Decroos et al. (KU Leuven), *"Valuing Actions by Estimating Probabilities in Most-Played Sports"*, KDD 2019.
* **Expected Threat ($xT$):** Karun Singh, *"Introducing Expected Threat ($xT$)"*, 2019.
* **Possession Adjustment:** Sigrid Olthof & Sam Green, *"Adjusting Defensive Metrics for Team Possession"*, 2013.
