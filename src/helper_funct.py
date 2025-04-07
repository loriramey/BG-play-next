import streamlit as st
import pandas as pd
import re
import logging
from rapidfuzz import process, fuzz

#HELPER FUNCTION to improve caching and loading of a parquet file
@st.cache_data
def load_parquet_file(path):
    return pd.read_parquet(path)

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
        if "gamedata" not in st.session_state:
            st.session_state["gamedata"] = load_parquet_file("data/processed/gamedata.parquet")
            logging.info("Loaded gamedata.parquet into session_state in helper_funct")
        gamedata_df = st.session_state["gamedata"]
        st.session_state["game_index"] = {name: idx for idx, name in enumerate(gamedata_df['name'])}
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
          - min_avg (float or None)
          - min_weight(float or None)
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

# HELPER FUNCTION: retrieve the full row of data for any game by game id
def get_game_data(game_id: int) -> pd.Series:
    """
    Return the game data row from the gamedata DataFrame in session_state for the given game ID.
    """
    if "gamedata" not in st.session_state:
        st.session_state["gamedata"] = pd.read_parquet("data/processed/gamedata.parquet")
        logging.info("Loaded gamedata.parquet into session_state in get_game_data")

    gamedata_df = st.session_state["gamedata"]
    result = gamedata_df[gamedata_df['id'] == game_id]
    if result.empty:
        raise ValueError("Game ID not found in gamedata.")
    return result.iloc[0]
