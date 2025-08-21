# parser/skill_frequencies.py
from __future__ import annotations
from pathlib import Path
from collections import Counter
import re
import pandas as pd

# Always anchor paths to the repo, not the current working dir
THIS_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = THIS_DIR.parent                      # .../data science navigator
DATA_DIR = PROJECT_ROOT / "data"
JOBS_DIR = DATA_DIR / "jobs"

# Skills we track
REQUIRED_SKILLS = [
    "python", "r", "sql", "excel", "aws", "spark", "tableau", "hadoop", "sas", "azure"
]

PATTERN = re.compile(r"\b(" + "|".join(map(re.escape, REQUIRED_SKILLS)) + r")\b", re.I)

def compute_counts(jobs_dir: Path = JOBS_DIR) -> Counter:
    """
    Read the first CSV in data/jobs, scan text columns, and return a Counter of skill mentions.
    Does NOT run at import time.
    """
    csvs = sorted(jobs_dir.glob("*.csv"))
    if not csvs:
        # Return empty instead of raising, so the API can still start
        return Counter()

    csv_path = csvs[0]
    df = pd.read_csv(csv_path, encoding_errors="ignore")

    # Prefer typical text columns if present; else fall back to all string/object columns
    pref_names = {"job description", "description", "requirements", "responsibilities"}
    text_cols = [c for c in df.columns if isinstance(c, str) and c.strip().lower() in pref_names]
    if not text_cols:
        text_cols = [c for c in df.columns if df[c].dtype == "object"]

    texts = []
    for c in text_cols:
        col = df[c].fillna("").astype(str).tolist()
        texts.append("\n".join(col))
    big_text = "\n".join(texts)

    counts = Counter(m.group(1).lower() for m in PATTERN.finditer(big_text))
    return counts

# Lazy cache so imports never crash
_COUNTS: Counter | None = None

def get_counts() -> Counter:
    global _COUNTS
    if _COUNTS is None:
        try:
            _COUNTS = compute_counts()
        except Exception as e:
            print(f"[skill_frequencies] Warning: could not compute counts yet: {e}")
            _COUNTS = Counter()
    return _COUNTS

def demand_rank() -> dict[str, int]:
    """
    Produce a rank dictionary (1 = most demanded). If counts empty, return zeros.
    """
    counts = get_counts()
    if not counts:
        return {s: 0 for s in REQUIRED_SKILLS}
    ranked = {skill: i+1 for i, (skill, _) in enumerate(counts.most_common())}
    # Ensure all REQUIRED_SKILLS are present
    for s in REQUIRED_SKILLS:
        ranked.setdefault(s, 0)
    return ranked
