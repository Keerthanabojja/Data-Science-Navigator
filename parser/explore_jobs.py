import os
import glob
import pandas as pd

# 1) Locate the jobs folder (relative to this script)
jobs_dir = os.path.abspath(os.path.join(os.getcwd(), '..', 'data', 'jobs'))
print("Looking in:", jobs_dir)

# 2) Find any CSV files there
csv_paths = glob.glob(os.path.join(jobs_dir, '*.csv'))
print("CSV files found:", csv_paths)

if not csv_paths:
    raise FileNotFoundError(f"No CSV files found in {jobs_dir}")

# 3) Pick the first one automatically
csv_path = csv_paths[0]
print("Using CSV:", csv_path)

# 4) Load it
df = pd.read_csv(csv_path)

# 5) Inspect
print("\nShape:", df.shape)
print("\nColumns:\n", df.columns.tolist())
print("\nFirst 5 rows:\n", df.head())

# 6) Optional stats
if 'description' in df.columns:
    lengths = df['description'].dropna().str.len()
    print("\nDescription length stats:\n", lengths.describe())

if 'title' in df.columns:
    print("\nTop 10 titles:\n", df['title'].value_counts().head(10))

