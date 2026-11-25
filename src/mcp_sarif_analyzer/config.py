import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

DATA_INPUT = DATA_DIR / "input"
DEFAULT_SARIF = DATA_INPUT / "zlib-git-master-09a1572.sarif"
SARIF_PATH = Path(os.environ.get("SARIF_PATH", DEFAULT_SARIF))

REVIEWS_DIR = DATA_DIR / "reviews"
REPORTS_DIR = DATA_DIR / "reports"

ALLOWED_VERDICTS = ("P0", "P1", "P2", "NA", "FP", "Need_analysis")
