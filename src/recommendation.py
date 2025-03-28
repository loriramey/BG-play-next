import numpy as np
import pandas as pd
from helper_funct import print_game_info, find_closest_name, get_root_title

GAMEDATA_FILE = "/Users/loriramey/PycharmProjects/BGPlayNext/data/raw/gamedata.csv"
COSINE_SIM_MECH_FILE =
COSINE_SIM_ORIG_FILE =

# Load master data and cosine similarity matrix
df = pd.read_csv(GAMEDATA_FILE)
cosine_sim_primary = np.load(COSINE_SIM_MECH_FILE)  # Precomputed cosine similarity matrix
cosine_sim_fallback = np.load(COSINE_SIM_ORIG_FILE) #procomputed using "looser" recipe
game_index = {name: idx for idx, name in enumerate(df['name'])}  # For fuzzy matching

# Ensure 'yearpublished' is numeric, drop NaNs, and convert to int
df['yearpublished'] = pd.to_numeric(df['yearpublished'], errors='coerce')
df = df.dropna(subset=['yearpublished'])
df['yearpublished'] = df['yearpublished'].astype(int)


# FUNCTION: Find "similar" games given a user input game, applying various filters
def get_rec_by_name(game_name, min_players=None, max_players=None,
                    max_time=None, min_rating=None, min_year=None, auto_select=False):

    game_name = find_closest_name(game_name, auto_select=auto_select)
    print(f"Matched game: {game_name}")
    print_game_info(game_name)  # Assumes print_game_info is available in the current scope
    if not game_name:
        return "Game not found. Try entering the name again."

    # Get index and compute similarity scores
    game_idx = game_index[game_name]
    sim_scores = list(enumerate(cosine_sim_primary[game_idx]))
    #print(f"Raw similarity scores for {game_name}: {sim_scores[:10]}")
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:26]  # Top 20 matches (exclude self)
    #print(f"Sorted similarity scores: {sim_scores[:5]}")

    # Build a dictionary for mapping similarity scores
    similarity_dict = {i[0]: i[1] for i in sim_scores}
    valid_indices = [i[0] for i in sim_scores if i[0] in df.index]
    if not valid_indices:
        return "No valid recommendations found."

    sim_game_names = df.loc[valid_indices, 'name'].str.strip().str.lower().tolist()
    #print(f"Top matches for {game_name}: {sim_game_names[:10]}")
    #print(f"🧐 Checking sim_game_names: {sim_game_names}")

    # Prepare DataFrame for filtering: work with lowercase names for matching
    df['name_lower'] = df['name'].str.lower()
    sim_game_names_lower = [name.lower() for name in sim_game_names]
    recommended_games = df[df['name_lower'].isin(sim_game_names_lower)].copy()
    #print(f"🔍 Before filtering: {len(recommended_games)} games found")  #DEBUG

    # Remove duplicate series using drop_duplicates while preserving original index
    recommended_games = recommended_games.drop_duplicates(subset='name_lower', keep='first')
    #print(f"🎯 After dropping clones: {len(recommended_games)} games remaining")

    # Apply user filters
    if min_players:
        recommended_games = recommended_games[recommended_games['minplayers'] >= min_players]
    if max_players:
        recommended_games = recommended_games[recommended_games['maxplayers'] <= max_players]
    if max_time:
        recommended_games = recommended_games[recommended_games['playingtime'] <= max_time]
    if min_rating:
        recommended_games = recommended_games[recommended_games['average'] >= min_rating]
    if min_year:
        recommended_games = recommended_games[recommended_games['yearpublished'] >= min_year]
    print(f"🎯 After filtering: {len(recommended_games)} games remaining")

    # IMPORTANT: Restrict the recommended_games to only those rows whose index is in similarity_dict keys
    recommended_games = recommended_games[recommended_games.index.isin(similarity_dict.keys())]
    #print("Indices after restricting:", recommended_games.index.tolist())

    # Map similarity scores using the DataFrame's index
    recommended_games["similarity"] = recommended_games.index.map(similarity_dict)
    recommended_games = recommended_games.sort_values(by="similarity", ascending=False)

    return recommended_games[['name', 'description', 'thumbnail', 'yearpublished',
                'category_list', 'mech_list', 'tags', 'Board Game Rank', 'tags_str',
                'categories_str', 'mechanics_str', 'minplayers', 'maxplayers', 'playingtime',
                'average', 'averageweight', 'similarity']]


# For debugging purposes: a separate function to test filtering and mapping
def get_rec_by_name_debug_filtered(game_name, auto_select=False, max_time=None):
    recs = get_rec_by_name(game_name, auto_select=auto_select, max_time=max_time)
    print("Final debug DataFrame:")
    print(recs[['name', 'playingtime', 'similarity']])
    return recs

if __name__ == "__main__":
    # Quick test with debug function
    #print_game_info("Star Wars: Rebellion")
    debug_recs = get_rec_by_name_debug_filtered("Power Grid", auto_select=True, max_time=130)
    print("\nReturned recommendations:")
    print(debug_recs)