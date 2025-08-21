import os
import json

# List of skills to look for (lowercase)
SKILLS = [
    "python", "sql", "excel", "tableau", "power bi",
    "spark", "hadoop", "sas", "r", "tensorflow",
    "pandas", "numpy", "scikit-learn", "aws", "azure"
]

# Folders
INPUT_DIR  = os.path.join(os.getcwd(), '..', 'data', 'cvs', 'text_csv')
ENTITIES_DIR = os.path.join(os.getcwd(), '..', 'data', 'cvs', 'entities')
OUTPUT_DIR = os.path.join(os.getcwd(), '..', 'data', 'cvs', 'skills')
os.makedirs(OUTPUT_DIR, exist_ok=True)

# For each resume text file
for fname in os.listdir(INPUT_DIR):
    if not fname.lower().endswith('.txt'):
        continue

    txt_path = os.path.join(INPUT_DIR, fname)
    text = open(txt_path, 'r', encoding='utf-8').read().lower()

    found = [skill for skill in SKILLS if skill in text]

    # Save results as JSON
    out_path = os.path.join(OUTPUT_DIR, fname.replace('.txt', '.json'))
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump({"skills": found}, f, indent=2)

    print(f"{fname}: found {len(found)} skills → {found}")
