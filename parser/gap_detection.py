import os
import json

# Required skills for the target role
REQUIRED_SKILLS = [
    "r", "python", "sql", "excel", "aws",
    "spark", "tableau", "hadoop", "sas", "azure"
]

# Demand ranking dict from Day 6 counts
DEMAND_RANK = {
    "r": 3909, "python": 2057, "sql": 2022, "excel": 1855,
    "aws": 949, "spark": 897, "tableau": 673, "hadoop": 638,
    "sas": 537, "azure": 304
}

# Folders
SKILLS_DIR = os.path.abspath(os.path.join(os.getcwd(), '..', 'data', 'cvs', 'skills'))
OUTPUT_DIR = os.path.abspath(os.path.join(SKILLS_DIR, '..', 'gaps'))
os.makedirs(OUTPUT_DIR, exist_ok=True)

for fname in os.listdir(SKILLS_DIR):
    if not fname.endswith('.json'):
        continue

    skills_path = os.path.join(SKILLS_DIR, fname)
    with open(skills_path, 'r', encoding='utf-8') as f:
        found_skills = json.load(f).get("skills", [])

    # Compute missing skills
    missing = [s for s in REQUIRED_SKILLS if s not in found_skills]

    # Sort missing by descending demand
    missing_sorted = sorted(missing, key=lambda s: DEMAND_RANK.get(s, 0), reverse=True)

    # Save gap report
    report = {
        "resume": fname.replace('.json', '.txt'),
        "found_skills": found_skills,
        "missing_skills": missing_sorted
    }
    out_path = os.path.join(OUTPUT_DIR, fname)
    with open(out_path, 'w', encoding='utf-8') as out:
        json.dump(report, out, indent=2)

    print(f"{fname}: {len(found_skills)} found, {len(missing_sorted)} missing → {missing_sorted}")
