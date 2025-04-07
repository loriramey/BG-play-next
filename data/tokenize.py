import pandas as pd
import ast

def clean_and_tokenize_list_column(col):
    return col.apply(
        lambda lst: " ".join(
            token.strip().replace(" ", "_").replace("__", "_")
            for token in ast.literal_eval(lst) if isinstance(token, str)
        ) if pd.notna(lst) else ""
    )

df = pd.read_csv(".../data/raw/BGGtop300.csv")

df["tags_str"] = clean_and_tokenize_list_column(df["tags"])
df["mechanics_str"] = clean_and_tokenize_list_column(df["mech_list"])
df["categories_str"] = clean_and_tokenize_list_column(df["category_list"])

df.to_csv(".../data/raw/BGGtop300.csv", index=False)
print("✅ Tokenization complete and file saved.")