import pandas as pd

# Load your dataset (replace filename with your file)
df = pd.read_csv("googleplaystore.csv")

# Print column names
print("Columns in dataset:", df.columns)

# Optional: see first 5 rows
print(df.head())
