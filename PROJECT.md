# Project: ScoutBench Recruitment Dossier Enhancement

## Architecture
- **Data Layer (`src/data_loader.py`, `data/processed/master_players.csv`)**:
  Holds 3,952 authentic player-season records (1,976 for 2025/26 and 1,976 for 2024/25) across 96 clubs in 5 leagues. Enriched with 9 biographical, physical, and financial attributes with 0 nulls.
- **Normalization & Analytics Layer (`src/normalization.py`, `src/metrics_engine.py`)**:
  Computes per-90 metrics, pAdj possession adjustments, positional percentile scoring, 4 universal behavioral indices (HPWI, VDI, PRBI, OOTI), tactical spectrum archetypes, 4 cohort benchmark averages, and multi-profile delta calculations.
- **Visualization Engine (`src/visualizer.py`)**:
  Renders single-player PyPizza radars, Gaussian KDE spatial heatmaps, quadrant scatter benchmarks, and overlapping multi-trace polar radars (2 to 4 profiles with distinct alpha fills and colorways).
- **Frontend UI (`app.py`, `src/config.py`)**:
  Streamlit interface featuring neutral 3-layer charcoal editorial palette, dossier header profile bar, integrated multi-player and cohort comparison section, and strict zero-emoji styling.
- **Test Harness (`tests/`)**:
  Automated unit and integration test suite executing via `python -m unittest discover tests` (50/50 tests passing).

## Feature Inventory
| # | Feature | Description | Milestone | Source | Status |
|---|---------|-------------|-----------|--------|--------|
| 1 | Master Metadata Schema Enrichment | Add `market_value_eur`, `contract_expiry`, `wage_tier`, `preferred_foot`, `height_cm`, `weight_kg`, `nationality`, `primary_position`, `secondary_position` across all 3,952 player-seasons | M1 | R1 | DONE |
| 2 | Ground-Truth Superstar & Squad Calibration | Calibrate authentic biographical/financial data for top stars and realistic distributions for all 96 squads | M1 | R1 | DONE |
| 3 | Data Loader Schema Validation | Implement `validate_master_dataset` in `src/data_loader.py` asserting 0 nulls across 3,952 rows and valid ranges | M1 | R1 | DONE |
| 4 | Dossier Header Profile Bar | Render dedicated 3-layer charcoal metadata bar (Market Val, Expiry, Wage Tier, Physical DNA, Foot, Nationality, Roles) in `app.py` | M3 | R1 | DONE |
| 5 | Dynamic Multi-Player Selection (2-4 Profiles) | Search and select 1 to 3 additional footballers across leagues and positions | M3 | R2 | DONE |
| 6 | Preset Cohort Baseline Benchmarks | Dynamic calculation of Top 5 Positional Average, Domestic Positional Average, U-21 European Average, U-21 Domestic Average | M2 | R2 | DONE |
| 7 | Overlapping Multi-Trace Polar Radar | High-contrast multi-polygon radar chart with distinct colorways, custom alpha fills, and clear legends in `src/visualizer.py` | M2 | R2 | DONE |
| 8 | Side-by-Side Comparative Delta Table | Metric-by-metric delta table displaying raw per-90, percentiles, and positive/negative differentials (+/- deltas) | M2, M3 | R2 | DONE |
| 9 | Comparative Behavioral Index Breakdown | 4-box side-by-side matrix for HPWI, VDI, PRBI, OOTI with index deltas | M2, M3 | R2 | DONE |
| 10 | Complete Emoji Removal | Strip all 45 emoji occurrences across `app.py`, `src/metrics_engine.py`, `src/visualizer.py`, and `src/config.py` | M3 | R3 | DONE |
| 11 | Editorial Typography & Geometric Badges | Replace emojis with clean uppercase tracker tags, geometric bullets (`•`, `■`), and neutral styling | M3 | R3 | DONE |
| 12 | Comprehensive Automated Test Suite | Unit tests for data loading, cohort benchmarks, multi-radar generation, delta calculations, stress tests, and zero-emoji compliance passing 100% | M4 | AC | DONE |
| 13 | Forensic Integrity Verification | Full forensic audit verifying zero integrity violations, no mock dummy backends, and full genuine logic | M5 | Audit | DONE |

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| M1 | Data Layer & Metadata Pipeline | Enrich 3,952 rows in `master_players.csv`, update `src/data_loader.py` with schema validation and accessors | None | DONE |
| M2 | Analytics & Comparison Engine | Cohort averages, delta tables, and overlapping polar radar in `src/metrics_engine.py` & `src/visualizer.py` | M1 | DONE |
| M3 | Editorial UI, Header & Comparison Section | Dossier profile bar, comparison section, and complete zero-emoji cleanup across `app.py` and `src/` | M1, M2 | DONE |
| M4 | E2E Testing Track & Test Suite Expansion | Full test suite (`test_data_loader`, `test_metrics`, `test_visualizer`, `test_comparison`, `test_zero_emoji`, `test_empirical_stress`) | M1, M2, M3 | DONE |
| M5 | Forensic Audit & Hardening | Adversarial stress testing and forensic audit verification | M4 | DONE |

## Interface Contracts
### `src/data_loader.py`
```python
def load_master_dataset(filepath: Optional[Path] = None, min_minutes: int = 900) -> pd.DataFrame: ...
def validate_master_dataset(df: pd.DataFrame) -> bool: ...
def get_player_profile(df: pd.DataFrame, player_name: str, season: Optional[str] = None) -> Optional[pd.Series]: ...
def get_cohort_peers(df: pd.DataFrame, position_group: str, league: Optional[str] = None, season: Optional[str] = None) -> pd.DataFrame: ...
```

### `src/metrics_engine.py`
```python
def compute_cohort_benchmark(df: pd.DataFrame, position_group: str, season: str, benchmark_type: str, domestic_league: Optional[str] = None) -> pd.Series: ...
def compute_comparison_deltas(base_row: pd.Series, base_percentiles: Dict[str, float], compared_rows: List[pd.Series], compared_percentiles: List[Dict[str, float]], metrics: List[str]) -> pd.DataFrame: ...
```

### `src/visualizer.py`
```python
def create_multi_player_radar(profiles_data: List[Dict[str, Any]], metrics: List[str], theme: Optional[Dict] = None) -> Any: ...
```

## Code Layout
- `data/processed/master_players.csv`: Master dataset containing 3,952 player-seasons.
- `src/config.py`: Theme palettes, metric definitions, behavioral indices, and tactical spectrum configs.
- `src/data_loader.py`: Dataset loader, cohort mapping, validation, and search index helpers.
- `src/metrics_engine.py`: Normalization, percentiles, behavioral indices, tactical spectrum, cohort benchmarks, delta computation.
- `src/visualizer.py`: Visual charts (PyPizza radar, Pitch heatmap, Quadrant scatter, Multi-player polar radar).
- `app.py`: Streamlit main dashboard with dossier, profile bar, comparison tool, and zero-emoji styling.
- `tests/`: Automated unit, integration, and stress tests (50 tests total).
