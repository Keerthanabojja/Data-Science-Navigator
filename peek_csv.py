import pandas as pd
import os

# Adjust this path if your folder name has spaces
csv_path = os.path.join('data', 'cvs', 'UpdatedResumeDataSet.csv')

# Load just the first few rows
df = pd.read_csv(csv_path)

# 1) Print all column names
print("Columns in CSV:")
print(df.columns.tolist(), "\n")

# 2) Print the first 3 rows so you can see sample data
print("First 3 rows:")
print(df.head(3))
