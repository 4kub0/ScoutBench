"""
ScoutBench Direct Real FBref Extractor (using curl_cffi with Chrome Impersonation)
Extracts official Big-5 European consolidated tables for 2024/25 and 2025/26:
- Standard Stats (Playing time, Age, Positions)
- Shooting (npxG, Shots, SoT)
- Passing (xAG, Key Passes, Prog Passes, Final 3rd)
- Goal & Shot Creation (SCA, GCA)
- Defense (Tackles, Interceptions, Blocks)
- Possession (Carries, Take-Ons, Box Touches)
- Advanced Keepers (PSxG +/-, Save %, Sweeper actions, Crosses stopped %)
"""

from pathlib import Path
import time
import re
import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
PROCESSED_DIR = DATA_DIR / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def get_html_with_curl(url: str) -> str:
    from curl_cffi import requests
    response = requests.get(url, impersonate="chrome124", timeout=30)
    if response.status_code == 200:
        return response.text
    raise Exception(f"Failed to fetch {url}, status code: {response.status_code}")


def parse_fbref_table(html: str, table_id_substring: str = "stats_") -> pd.DataFrame:
    soup = BeautifulSoup(html, "html.parser")
    
    # 1. First search direct tables
    tables = soup.find_all("table")
    target_table = None
    for t in tables:
        if table_id_substring in t.get("id", ""):
            target_table = t
            break
            
    # 2. If not found in rendered DOM, FBref frequently hides stats tables inside HTML comments
    if not target_table:
        comments = soup.find_all(string=lambda text: isinstance(text, type(soup.contents[0])) if hasattr(text, 'contents') else False)
        # Search raw comments in string
        for c in soup.find_all(string=lambda t: t and f'id="{table_id_substring}' in str(t) or (t and '<table' in str(t))):
            comment_soup = BeautifulSoup(str(c), "html.parser")
            for t in comment_soup.find_all("table"):
                if table_id_substring in t.get("id", "") or "stats_" in t.get("id", ""):
                    target_table = t
                    break
            if target_table:
                break

    if not target_table:
        # Fallback: parse whatever table exists with stats class
        for t in tables:
            if "stats_table" in t.get("class", []):
                target_table = t
                break

    if not target_table:
        raise ValueError(f"Could not find table matching '{table_id_substring}'")

    # Read table with pandas
    df = pd.read_html(StringIO(str(target_table)))[0]
    
    # Flatten MultiIndex columns
    if isinstance(df.columns, pd.MultiIndex):
        flat_cols = []
        for col in df.columns:
            c = col[-1] if col[-1] and not str(col[-1]).startswith("Unnamed") else col[0]
            flat_cols.append(str(c).strip())
        df.columns = flat_cols
        
    # Drop repeated header rows
    if "Player" in df.columns:
        df = df[df["Player"] != "Player"].reset_index(drop=True)
    elif "player" in df.columns:
        df = df[df["player"] != "Player"].reset_index(drop=True)
        
    return df


def test_single_table():
    print("Testing connection to FBref via curl_cffi...")
    url = "https://fbref.com/en/comps/Big5/stats/players/Big-5-European-Leagues-Stats"
    html = get_html_with_curl(url)
    print(f"[OK] Fetched {len(html):,} bytes.")
    df = parse_fbref_table(html, "stats_standard")
    print(f"[OK] Parsed Standard Stats Table: {len(df):,} players found.")
    print("Sample rows:")
    print(df[["Player", "Squad", "Comp", "Pos", "Min"]].head())
    return df


if __name__ == "__main__":
    test_single_table()
