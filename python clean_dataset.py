import pandas as pd

# Load dataset
df = pd.read_csv("googleplaystore.csv")

# Keep only columns we need
df = df[['App', 'Reviews', 'Rating']]

# Drop rows with missing Reviews
df = df[df['Reviews'].notnull()]

# convert Rating to numeric
df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')
df = df[df['Rating'].notnull()]

print("Dataset preview:")
print(df.head())
print("\nApps available:", df['App'].nunique())

# Using Ratings

def rating_to_sentiment(rating):
    if rating >= 4:
        return "Positive"
    elif rating == 3:
        return "Neutral"
    else:
        return "Negative"

df['Sentiment'] = df['Rating'].apply(rating_to_sentiment)

df.to_csv("googleplay_cleaned.csv", index=False)
print("Saved cleaned file -> googleplay_cleaned.csv")

