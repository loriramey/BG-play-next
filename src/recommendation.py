import streamlit as st
import numpy as np
import pandas as pd
import logging

'''
GAMEDATA_FILE = "/Users/loriramey/PycharmProjects/BGPlayNext/data/raw/gamedata.csv"
COSINE_SIM_MECH_FILE = "/Users/loriramey/PycharmProjects/BGPlayNext/data/matrices/cosine_similarity_mech_heavy.npy"
COSINE_SIM_ORIG_FILE = "/Users/loriramey/PycharmProjects/BGPlayNext/data/matrices/cosine_similarity_origmix.npy"

# Load master data and cosine similarity matrix
df = pd.read_csv(GAMEDATA_FILE)
cosine_sim_primary = np.load(COSINE_SIM_MECH_FILE)  # Precomputed cosine similarity matrix
cosine_sim_fallback = np.load(COSINE_SIM_ORIG_FILE) #procomputed using "looser" recipe
game_index = {name: idx for idx, name in enumerate(df['name'])}  # For fuzzy matching

# Ensure 'yearpublished' is numeric, drop NaNs, and convert to int
df['yearpublished'] = pd.to_numeric(df['yearpublished'], errors='coerce')
df = df.dropna(subset=['yearpublished'])
df['yearpublished'] = df['yearpublished'].astype(int)
'''

# FUNCTION: Find "similar" games given a user input game, applying various filters
def get_rec_by_name(game_name, auto_select=False):
    """
    Compute recommendations for a given game name using the cosine similarity matrix.
    Fuzzy search on game name is handled before this function runs
    This function now uses st.session_state to load gamedata and the cosine similarity matrix.
    """
    # Load gamedata if not already loaded
    if "gamedata" not in st.session_state:
        st.session_state["gamedata"] = pd.read_csv("data/raw/gamedata.csv")
        logging.info("Loaded gamedata.csv into session_state")
    df = st.session_state["gamedata"]

    # Load the primary cosine similarity matrix if not already loaded
    if "cosine_sim_primary" not in st.session_state:
        st.session_state["cosine_sim_primary"] = np.load("data/matrices/cosine_similarity_mech_heavy.npy")
        logging.info("Loaded cosine_similarity_mech_heavy.npy into session_state")
    cosine_sim_primary = st.session_state["cosine_sim_primary"]

    # Ensure the game_index exists in session_state
    if "game_index" not in st.session_state:
        st.session_state["game_index"] = {name: idx for idx, name in enumerate(df['name'])}
        logging.info("Computed game_index from gamedata")
    game_index = st.session_state["game_index"]


    # Get index and compute similarity scores
    game_idx = game_index[game_name]
    if game_idx is None:
        raise ValueError("Game not found in dataset.")

    sim_scores = list(enumerate(cosine_sim_primary[game_idx]))
    logging.info(f"Raw similarity scores for {game_name}: {sim_scores[:10]}")
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:26]  # Top 20 matches (exclude self)
    logging.info(f"Sorted similarity scores: {sim_scores[:5]}")

    # Build a dictionary for mapping similarity scores
    similarity_dict = {i[0]: i[1] for i in sim_scores}
    valid_indices = [i[0] for i in sim_scores if i[0] in df.index]
    if not valid_indices:
        raise ValueError("No valid recommendations found")

    sim_game_names = df.loc[valid_indices, 'name'].str.strip().str.lower().tolist()
    logging.info(f"Top matches for {game_name}: {sim_game_names[:10]}")

    # Prepare DataFrame for filtering: work with lowercase names for matching
    df['name_lower'] = df['name'].str.lower()
    sim_game_names_lower = [name.lower() for name in sim_game_names]
    recommended_games = df[df['name_lower'].isin(sim_game_names_lower)].copy()
    logging.info(f"Before filtering: {len(recommended_games)} games found")  #DEBUG

    # Remove duplicate series using drop_duplicates while preserving original index
    recommended_games = recommended_games.drop_duplicates(subset='name_lower', keep='first')
    logging.info(f"After dropping clones: {len(recommended_games)} games remaining")

    # IMPORTANT: Restrict the recommended_games to only those rows whose index is in similarity_dict keys
    recommended_games = recommended_games[recommended_games.index.isin(similarity_dict.keys())]
    logging.info("Indices after restricting: %s", recommended_games.index.tolist())

    # Map similarity scores using the DataFrame's index
    recommended_games["similarity"] = recommended_games.index.map(similarity_dict)
    recommended_games = recommended_games.sort_values(by="similarity", ascending=False)

    return recommended_games[['name', 'description_clean', 'thumbnail', 'image', 'yearpublished',
                'category_list', 'mech_list', 'tags', 'BGGrank', 'tags_str',
                'categories_str', 'mechanics_str', 'minplayers', 'maxplayers', 'playingtime',
                'average', 'bayesaverage', 'averageweight', 'similarity']]


'''
# For debugging purposes: a separate function to test filtering and mapping
def get_rec_by_name_debug_filtered(game_name, auto_select=False, max_time=None):
    recs = get_rec_by_name(game_name, auto_select=auto_select, max_time=max_time)
    logging.debug("Final debug DataFrame:")
    logging.debug(recs[['name', 'playingtime', 'similarity']])
    return recs
'''

