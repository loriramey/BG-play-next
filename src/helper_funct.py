import streamlit as st
import numpy as np
import pandas as pd
import re
import logging
from rapidfuzz import process, fuzz

'''
# Define file paths
GAMEDATA_FILE = "/Users/loriramey/PycharmProjects/BGPlayNext/data/raw/gamedata.csv"
COSINE_SIM_MECH_FILE = "/Users/loriramey/PycharmProjects/BGPlayNext/data/matrices/cosine_similarity_mech_heavy.npy"
COSINE_SIM_ORIG_FILE = "/Users/loriramey/PycharmProjects/BGPlayNext/data/matrices/cosine_similarity_origmix.npy"

# Load gamedata.csv once and assume its order matches the CS matrix
df = pd.read_csv(GAMEDATA_FILE)

# Create an ID-to-index mapping assuming the CS matrix rows correspond to the order of the CSV
game_index = {name: idx for idx, name in enumerate(df['name'])}  # For fuzzy matching
id_to_index = {game_id: idx for idx, game_id in enumerate(df['id'])}

#HELPER FUNCTION: retrieve the similarity score for any pair of games from .npy
def get_similarity(game_id1: int, game_id2: int) -> float:
    """
    Return the cosine similarity between two games based on their IDs
    using the precomputed CS matrix.
    """
    if game_id1 not in id_to_index or game_id2 not in id_to_index:
        raise ValueError("One or both game IDs not found in the dataset.")
    idx1 = id_to_index[game_id1]
    idx2 = id_to_index[game_id2]
    return COSINE_SIM_MECH_FILE[idx1, idx2]

#HELPER FUNCTION: retrieve the full row of data for any game by game id
def get_game_data(game_id: int) -> pd.Series:
    """
    Return the game data row from gamedata.csv for the given game ID.
    """
    if game_id not in id_to_index:
        raise ValueError("Game ID not found in the dataset.")
    # This assumes that 'id' uniquely identifies a game in df.
    return df.loc[df['id'] == game_id].iloc[0]
'''

#HELPER FUNCTION --make sure user input isn't a hack-attack; limit to normal text
def sanitize_input(user_input):
    """
    Allow only letters, numbers, spaces, hyphens, commas, and periods.
    """
    allowed = re.compile(r'[^a-zA-Z0-9\s\-,.]')
    sanitized = allowed.sub('', user_input)
    return sanitized.strip()


# FUNCTION: Use fuzzy matching on game name to handle user input
def find_closest_name(user_input, auto_select=False):
    """
    Use fuzzy matching on the provided game name to return candidate matches.
    Checks to ensure expensive large data files are loaded to session state first

    Parameters:
      - user_input (str): The raw input from the user.
      - auto_select (bool): If True, return only the best match; otherwise, return a list of candidates.

    Returns:
      - If auto_select is True: the best matching game name (str).
      - Otherwise: a list of tuples of the form (game_name, score, index), which can be used in a UI dropdown.
    """
    sanitized = sanitize_input(user_input)

    # Ensure that gamedata and game_index are loaded in session state.
    if "game_index" not in st.session_state:
        # Load gamedata if needed
        if "gamedata" not in st.session_state:
            st.session_state["gamedata"] = pd.read_csv("data/raw/gamedata.csv")
            logging.info("Loaded gamedata.csv into session_state in helper_funct")
        df = st.session_state["gamedata"]
        st.session_state["game_index"] = {name: idx for idx, name in enumerate(df['name'])}
        logging.info("Computed game_index in helper_funct")

    game_index = st.session_state["game_index"]
    choices = list(map(str, game_index.keys()))
    matches = process.extract(sanitized, choices, scorer=fuzz.WRatio, limit=10)
    logging.info("found list of matches: {}".format(matches))

    if auto_select:
        return matches[0][0]  # Automatically choose the highest-confidence match

    # Convert the tuple output into a list of dictionaries for clarity in the UI.
    candidate_list = [{"name": match, "score": score} for match, score, _ in matches]
    return candidate_list



# FUNCTION: Extract root game title for searching and filtering (to avoid duplicates)
def get_root_title(title):
    return title.split(':')[0].split('(')[0].strip().lower()



def filter_games(game_list, filters):
    """
    Filter the recommended games DataFrame based on various criteria.

    Parameters:
      game_list (pd.DataFrame): DataFrame of recommended games.
      filters (dict): A dictionary with keys:
          - min_players (int or None)
          - max_players (int or None)
          - max_playtime (int or None)
          - min_bayesavg (float or None)
          - min_year (int or None)

    Returns:
      pd.DataFrame: The filtered DataFrame.
    """
    df = game_list.copy()

    # Ensure 'yearpublished' is numeric, drop NaNs, and convert to int
    numeric_columns = ['minplayers', 'maxplayers', 'playingtime', 'average', 'averageweight', 'yearpublished']
    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Apply filters if they are provided
    if filters.get('min_players') is not None:
        df = df[df['minplayers'] >= filters['min_players']]
        logging.info(f"Filtered by min_players: {filters['min_players']}, remaining: {len(df)}")

    if filters.get('max_players') is not None:
        df = df[df['maxplayers'] <= filters['max_players']]
        logging.info(f"Filtered by max_players: {filters['max_players']}, remaining: {len(df)}")

    if filters.get('max_playtime') is not None:
        df = df[df['playingtime'] <= filters['max_playtime']]
        logging.info(f"Filtered by max_playtime: {filters['max_playtime']}, remaining: {len(df)}")

    if filters.get('min_avg') is not None:
        df = df[df['average'] >= filters['min_avg']]
        logging.info(f"Filtered by min_avg: {filters['min_avg']}, remaining: {len(df)}")

    if filters.get("min_weight") is not None:
        df = df[df['averageweight'] >= filters['min_weight']]
        logging.info(f"Filtered by averageweight: {filters['min_weight']}, remaining: {len(df)}")

    if filters.get('min_year') is not None:
        df = df[df['yearpublished'] >= filters['min_year']]
        logging.info(f"Filtered by min_year: {filters['min_year']}, remaining: {len(df)}")

    return df

