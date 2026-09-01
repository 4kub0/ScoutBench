"""
ScoutBench Automated Zero-Emoji Compliance Test Suite (Milestone M3 / Requirement R3)
Scans all core Python files in src/, tests/, app.py, and scripts/ to enforce strict Zero-Emoji Policy.
Asserts that 0 emoji characters exist across the entire application and analytics codebase.
"""

import os
import unittest
import unicodedata
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# Explicit set of permitted editorial typographical punctuation, geometric markers, and math operators
ALLOWED_EDITORIAL_CODES = {
    0x00A0,  # Non-breaking space
    0x00A3,  # Pound sign (£)
    0x00B1,  # Plus-minus (±)
    0x00B7,  # Middle dot (·)
    0x0394,  # Greek capital letter Delta (Δ)
    0x2013,  # En-dash (–)
    0x2014,  # Em-dash (—)
    0x2022,  # Bullet (•)
    0x2026,  # Ellipsis (…)
    0x20AC,  # Euro (€)
    0x2190,  # Leftwards arrow (←)
    0x2191,  # Upwards arrow (↑)
    0x2192,  # Rightwards arrow (→)
    0x2193,  # Downwards arrow (↓)
    0x2264,  # Less-than or equal (≤)
    0x2265,  # Greater-than or equal (≥)
    0x25A0,  # Black square (■)
}


def is_emoji_character(char: str) -> bool:
    """
    Determines whether a Unicode character is an emoji or pictorial symbol.
    Returns False for standard ASCII, Latin-1 text, and approved editorial typography.
    """
    code = ord(char)
    
    if code < 0x00A0:
        return False
        
    if code in ALLOWED_EDITORIAL_CODES:
        return False
        
    # Standard emoji Unicode code point ranges
    emoji_ranges = [
        (0x1F600, 0x1F64F),  # Emoticons
        (0x1F300, 0x1F5FF),  # Misc Symbols and Pictographs
        (0x1F680, 0x1F6FF),  # Transport and Map
        (0x1F900, 0x1F9FF),  # Supplemental Symbols and Pictographs
        (0x1FA00, 0x1FAFF),  # Symbols and Pictographs Extended-A
        (0x2600, 0x27BF),    # Misc Symbols & Dingbats (e.g. \u26bd, \u26a1)
        (0xFE00, 0xFE0F),    # Variation Selectors
        (0x2300, 0x23FF),    # Misc Technical
        (0x2B50, 0x2B55),    # Star symbols (\u2b50)
        (0x1F1E6, 0x1F1FF),  # Regional Indicator Symbols (Flags)
    ]
    
    for start, end in emoji_ranges:
        if start <= code <= end:
            return True
            
    cat = unicodedata.category(char)
    if cat in ('So', 'Sk') and code >= 0x2000:
        return True
        
    return False


def scan_file_for_emojis(filepath: Path):
    """Scans a file line-by-line and returns a list of (line_num, list_of_emojis, line_content)."""
    violations = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for idx, line in enumerate(f, 1):
            emojis = [c for c in line if is_emoji_character(c)]
            if emojis:
                violations.append((idx, emojis, line.strip()))
    return violations


class TestZeroEmojiCompliance(unittest.TestCase):
    """Automated verification of the Zero-Emoji Editorial Policy across ScoutBench."""

    def test_emoji_detector_calibration(self):
        """Verify that our emoji detector correctly identifies emojis vs editorial symbols."""
        # Known emojis should return True (using raw unicode escapes so test file itself contains 0 emojis)
        self.assertTrue(is_emoji_character('\u26bd'))        # Soccer ball
        self.assertTrue(is_emoji_character('\U0001f680'))    # Rocket
        self.assertTrue(is_emoji_character('\U0001f3af'))    # Target
        self.assertTrue(is_emoji_character('\U0001f4ca'))    # Bar chart
        self.assertTrue(is_emoji_character('\u2b50'))        # Star
        self.assertTrue(is_emoji_character('\U0001f7e2'))    # Green circle
        self.assertTrue(is_emoji_character('\U0001f3f7'))    # Label

        # Allowed editorial typography should return False
        self.assertFalse(is_emoji_character('\u2022'))       # Bullet (•)
        self.assertFalse(is_emoji_character('\u25a0'))       # Black square (■)
        self.assertFalse(is_emoji_character('\u2014'))       # Em-dash (—)
        self.assertFalse(is_emoji_character('\u2013'))       # En-dash (–)
        self.assertFalse(is_emoji_character('\u00b7'))       # Middle dot (·)
        self.assertFalse(is_emoji_character('\u20ac'))       # Euro (€)
        self.assertFalse(is_emoji_character('\u0394'))       # Delta (Δ)
        self.assertFalse(is_emoji_character('\u2264'))       # Less than or equal (≤)
        self.assertFalse(is_emoji_character('\u2265'))       # Greater than or equal (≥)
        self.assertFalse(is_emoji_character('\u00b1'))       # Plus-minus (±)

    def test_zero_emojis_in_app_py(self):
        """Assert 0 emojis in the Streamlit frontend entrypoint app.py."""
        app_path = REPO_ROOT / 'app.py'
        self.assertTrue(app_path.exists(), 'app.py not found')
        violations = scan_file_for_emojis(app_path)
        
        msg = f"Found {len(violations)} emoji violations in app.py: {violations}"
        self.assertEqual(len(violations), 0, msg)

    def test_zero_emojis_in_src_directory(self):
        """Assert 0 emojis across all Python modules in src/."""
        src_dir = REPO_ROOT / 'src'
        self.assertTrue(src_dir.exists(), 'src directory not found')
        
        all_violations = {}
        for py_file in src_dir.glob('*.py'):
            violations = scan_file_for_emojis(py_file)
            if violations:
                all_violations[py_file.name] = violations
                
        self.assertEqual(
            len(all_violations), 0,
            f"Found emoji violations in src/ files: {all_violations}"
        )

    def test_zero_emojis_in_tests_directory(self):
        """Assert 0 emojis across all Python unit test files in tests/."""
        tests_dir = REPO_ROOT / 'tests'
        self.assertTrue(tests_dir.exists(), 'tests directory not found')
        
        all_violations = {}
        for py_file in tests_dir.glob('*.py'):
            violations = scan_file_for_emojis(py_file)
            if violations:
                all_violations[py_file.name] = violations
                
        self.assertEqual(
            len(all_violations), 0,
            f"Found emoji violations in tests/ files: {all_violations}"
        )

    def test_zero_emojis_in_scripts_directory(self):
        """Assert 0 emojis across all Python scripts in scripts/."""
        scripts_dir = REPO_ROOT / 'scripts'
        if not scripts_dir.exists():
            return
        all_violations = {}
        for py_file in scripts_dir.glob('*.py'):
            violations = scan_file_for_emojis(py_file)
            if violations:
                all_violations[py_file.name] = violations
        
        self.assertEqual(
            len(all_violations), 0,
            f"Found emoji violations in scripts/ files: {all_violations}"
        )


if __name__ == '__main__':
    unittest.main()