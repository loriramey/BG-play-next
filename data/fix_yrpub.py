import pandas as pd
import os

# Ensure output directory exists
os.makedirs("../data/processed", exist_ok=True)

# Load your existing parquet
df = pd.read_parquet("/data/processed/gamedata.parquet")

# Coerce to numeric, replace invalid or negative years with 0
df["yearpublished"] = pd.to_numeric(df["yearpublished"], errors="coerce").fillna(0).astype(int)
df.loc[df["yearpublished"] < 1900, "yearpublished"] = 0  # Custom rule

# Save back to parquet, overwriting the old file
df.to_parquet(".../data/processed/gamedata.parquet", index=False)
print("✅ yearpublished cleaned and parquet file updated!")

# Verify the changes
print("📊 Summary of yearpublished column:")
print(df["yearpublished"].describe())
print("\n📌 Unique nonzero years (first 20):", sorted(df["yearpublished"].unique()[df["yearpublished"].unique() > 0])[:20])
print("✅ All years below 1900 should now be set to 0")