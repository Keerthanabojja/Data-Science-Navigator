# parser/extract_text.py
from pathlib import Path
import re
import pandas as pd

# Always anchor paths to this file's location, not the working directory
THIS_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = THIS_DIR.parent          # .../data science navigator
DATA_DIR = PROJECT_ROOT / "data"
CVS_DIR = DATA_DIR / "cvs"

# Prefer this file name; adjust here if yours is different
RESUME_CSV = CVS_DIR / "UpdatedResumeDataSet.csv"

SKILL_PATTERN = re.compile(
    r"\b(python|r|sql|excel|aws|spark|tableau|hadoop|sas|azure|pandas|numpy|scikit-learn|power bi)\b",
    flags=re.IGNORECASE
)

def load_resume_df():
    """Load the resumes CSV lazily and from a robust absolute path."""
    if not RESUME_CSV.exists():
        raise FileNotFoundError(f"Resume CSV not found at: {RESUME_CSV}")
    return pd.read_csv(RESUME_CSV)

def parse_resume(file_storage_or_bytes) -> list[str]:
    """
    Very simple text extraction → skill spotting.
    Accepts a Flask FileStorage or raw bytes/str for quick testing.
    """
    if hasattr(file_storage_or_bytes, "read"):  # Flask FileStorage
        content = file_storage_or_bytes.read()
        try:
            text = content.decode("utf-8", errors="ignore")
        except AttributeError:
            text = str(content)
    else:
        # If someone passes a string/bytes directly
        text = file_storage_or_bytes if isinstance(file_storage_or_bytes, str) else str(file_storage_or_bytes)

    skills = set(m.group(1).lower() for m in SKILL_PATTERN.finditer(text))
    # normalize synonyms etc. if you want
    synonyms = {"power bi": "powerbi"}
    normalized = {synonyms.get(s, s) for s in skills}
    return sorted(normalized)
