import streamlit as st
import pandas as pd
import logging
from src.helper_funct import trim_franchise_clones

# FUNCTION: Find "similar" games given a user input game, applying various filters
@st.cache_data(show_spinner="Computing recommendations...")
def get_rec_by_name(game_name: str, match_mode: str = "mech", auto_select: bool = False) -> pd.DataFrame:
    """
    Given a board game name and a match mode, return a DataFrame of recommended games.

    Parameters:
    - game_name (str): The game title to base recommendations on.
    - match_mode (str): One of ['mech', 'cat', 'mixed'], selects which similarity matrix to use.
    - auto_select (bool): Reserved for future use / debugging.

    Returns:
    - pd.DataFrame: A filtered, sorted recommendation table.
    """

    # Load main game data from session (assumes it was preloaded elsewhere)
    df = st.session_state["gamedata"]

    #identify related game from user input (already fuzzy matched and sanitized)
    # Normalize title for matching
    df["name_lower"] = df["name"].str.lower().str.strip()
    game_name_lower = game_name.lower().strip()

    # Find matching game row (assume exact match from fuzzy logic earlier)
    game_row = df[df["name_lower"] == game_name_lower]
    if game_row.empty:
        raise ValueError(f"Game '{game_name}' not found in dataset.")

    game_id = game_row["id"].values[0]

    # Load the correct top-50 parquet based on match mode
    recipe_paths = {
        "mech": "data/processed/top50_mech_heavy.parquet",
        "cat": "data/processed/top50_cat_heavy.parquet",
        "mixed": "data/processed/top50_mixed.parquet"
    }
    if match_mode not in recipe_paths:
        raise ValueError(f"Invalid match mode: {match_mode}")

    sim_df = pd.read_parquet(recipe_paths[match_mode])

    # Filter to only rows where 'source_game_id' matches the game we're recommending from
    matches = sim_df[sim_df["base_game_id"] == game_id]

    # Join similarity scores with full game metadata
    merged = matches.merge(df, left_on="similar_game_id", right_on="id", how="inner")

    # Rename column
    merged["similarity"] = merged["similarity_score"]  # rename for legacy compatibility

    # Reduce the number of "clones" to 4
    recommendations = trim_franchise_clones(merged, max_per_series=4)

    # Filter and return selected columns
    return recommendations[[
        'name', 'description_clean', 'thumbnail', 'image', 'yearpublished',
        'category_list', 'mech_list', 'tags', 'BGGrank', 'tags_str',
        'categories_str', 'mechanics_str', 'minplayers', 'maxplayers', 'playingtime',
        'average', 'bayesaverage', 'averageweight', 'similarity'
    ]].sort_values(by="similarity", ascending=False)
