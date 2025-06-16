# data_utilities.py
# One-off ETL helpers for building and cleaning the board game dataset

import pandas as pd
import re


def parse_family_field(raw: str) -> dict:
    """
    Parse boardgamefamily into:
      - series_names         (list[str])    # all “Series: …” values
      - game_tags            (list[str])    # all “Game: …” values
      - is_digital           (bool)
      - digital_platforms    (list[str])    # e.g. ["Tabletopia","TTS"] or ["Other"]
      - is_crowdfunded       (bool)
      - crowdfund_platforms  (list[str])    # platform names or ["Other"]
      - family_meta          (list[str])    # raw parts for later mining
    """
    parts = [p.strip() for p in raw.split(";") if p.strip()]
    out = {
        "series_names": [],
        "game_tags": [],
        "is_digital": False,
        "digital_platforms": [],
        "is_crowdfunded": False,
        "crowdfund_platforms": [],
        "family_meta": parts
    }

    for p in parts:
        low = p.lower()

        # Series tags (can occur multiple times)
        if low.startswith("series:"):
            val = p.split("Series:", 1)[1].strip()
            if val and val not in out["series_names"]:
                out["series_names"].append(val)

        # Game tags (can occur multiple times)
        elif low.startswith("game:"):
            val = p.split("Game:", 1)[1].strip()
            if val and val not in out["game_tags"]:
                out["game_tags"].append(val)

        # Digital implementations
        elif low.startswith("digital implementation"):
            out["is_digital"] = True
            tail = p.split(":", 1)[1].strip() if ":" in p else ""
            if tail:
                if tail not in out["digital_platforms"]:
                    out["digital_platforms"].append(tail)
            else:
                if "Other" not in out["digital_platforms"]:
                    out["digital_platforms"].append("Other")

        # Crowdfunding
        elif low.startswith("crowdfunding:") or low == "crowdfunding":
            out["is_crowdfunded"] = True
            tail = p.split("Crowdfunding:", 1)[1].strip() if ":" in p else ""
            if tail:
                if tail not in out["crowdfund_platforms"]:
                    out["crowdfund_platforms"].append(tail)
            else:
                if "Other" not in out["crowdfund_platforms"]:
                    out["crowdfund_platforms"].append("Other")

    return out


def unwrap_family_column(df: pd.DataFrame, raw_col: str = "boardgamefamily") -> pd.DataFrame:
    """Add parsed family columns to the DataFrame."""
    parsed = (
        df[raw_col]
        .fillna("")
        .apply(parse_family_field)
        .apply(pd.Series)
    )
    return pd.concat([df, parsed], axis=1)


def build_clean_dataset():
    """Load raw CSV, unwrap boardgamefamily, and write cleaned Parquet."""
    df = pd.read_csv("data/raw/gamedata.csv")
    df = unwrap_family_column(df, raw_col="boardgamefamily")
    df.to_parquet("data/processed/gamedata.parquet", index=False)


if __name__ == "__main__":
    # Run the ETL and then validate a few columns
    build_clean_dataset()
    df_clean = pd.read_parquet("data/processed/gamedata.parquet")
    # Quick sanity check
    print(df_clean[[
        "series_names", "game_tags",
        "is_digital", "digital_platforms",
        "is_crowdfunded", "crowdfund_platforms"
    ]].head())
