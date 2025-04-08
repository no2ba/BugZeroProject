import os
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
REPORTS_DIR = BASE_DIR / "reports"
REPORTS_DIR.mkdir(exist_ok=True)

# Browser settings
BROWSER = "chrome"  # Options: chrome, firefox, edge
HEADLESS = False
IMPLICIT_WAIT = 10  # seconds

# Path settings
TRANSLATION_TABLE_PATH = BASE_DIR / "config" / "translation_table.xlsx"
DEFAULT_TESTCASE_PATH = BASE_DIR / "test_cases.xlsx"
CHROME_DRIVER_PATH = BASE_DIR / "config" / "chromedriver"