import os
import spacy

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")

# Folder with the text files
INPUT_DIR = os.path.join(os.getcwd(), '..', 'data', 'cvs', 'text_csv')
# Output folder for entity JSON
OUTPUT_DIR = os.path.join(INPUT_DIR, '..', 'entities')
os.makedirs(OUTPUT_DIR, exist_ok=True)

for fname in os.listdir(INPUT_DIR):
    if not fname.lower().endswith('.txt'):
        continue

    txt_path = os.path.join(INPUT_DIR, fname)
    doc = nlp(open(txt_path, 'r', encoding='utf-8').read())

    entities = []
    for ent in doc.ents:
        entities.append({
            "text": ent.text,
            "label": ent.label_
        })

    out_path = os.path.join(OUTPUT_DIR, fname.replace('.txt', '.json'))
    with open(out_path, 'w', encoding='utf-8') as f:
        import json
        json.dump(entities, f, indent=2)

    print(f"Extracted {len(entities)} entities from {fname}")
