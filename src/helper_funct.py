import numpy as np
import pandas as pd
import re
from rapidfuzz import process, fuzz


# Define file paths
GAMEDATA_FILE = "/Users/loriramey/PycharmProjects/BGapp/data/gamedata_sorted_cleaned.csv"
COSINE_SIM_FILE = "/Users/loriramey/PycharmProjects/BGapp/data/cosine_similarity_weighted.npy"

# Load gamedata.csv once and assume its order matches the CS matrix
df = pd.read_csv(GAMEDATA_FILE)

# Create an ID-to-index mapping assuming the CS matrix rows correspond to the order of the CSV
id_to_index = {game_id: idx for idx, game_id in enumerate(df['id'])}

# Load the precomputed cosine similarity matrix
cs_matrix = np.load(COSINE_SIM_FILE)


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
    return cs_matrix[idx1, idx2]


#HELPER FUNCTION: retrieve the full row of data for any game by game id
def get_game_data(game_id: int) -> pd.Series:
    """
    Return the game data row from gamedata.csv for the given game ID.
    """
    if game_id not in id_to_index:
        raise ValueError("Game ID not found in the dataset.")
    # This assumes that 'id' uniquely identifies a game in df.
    return df.loc[df['id'] == game_id].iloc[0]


#HELPER FUNCTION --make sure user input isn't a hack-attack; limit to normal text
def sanitize_input(user_input):
    """
    Allow only letters, numbers, spaces, hyphens, commas, and periods.
    """
    allowed = re.compile(r'[^a-zA-Z0-9\s\-,.]')
    sanitized = allowed.sub('', user_input)
    return sanitized.strip()


#HELPER FUNCTION to print a quick summary of recommended info
def print_recommendations_summary(recs_df):
    """
    Print a compact summary for each recommended game:
      name / min players / max players / playingtime / average / average weight / tags / cats / mechs
    """
    for _, row in recs_df.iterrows():
        print(f"{row['name']} / Players: {row['minplayers']}-{row['maxplayers']} / "
              f"Playtime: {row['playingtime']} min / Rating: {row['average']:.2f}⭐ / "
              f"Avg Weight: {row['averageweight']} / Tags: {row['tags']} / "
              f"Category: {row['categories_str']} /  Mechanics: {row['mechanics_str']}"
        )


#FUNCTION for pulling and printing a single game's information
def print_game_info(game_name):
    df_sorted = pd.read_csv("/Users/loriramey/PycharmProjects/BGapp/data/gamedata_sorted.csv")

    # Filter the DataFrame for the game name (case insensitive)
    game_row = df_sorted[df_sorted['name'].str.lower() == game_name.lower()]
    if game_row.empty:
        print(f"Game '{game_name}' not found in gamedata_sorted.csv.")
        return
    # Get the first match (if there are duplicates)
    row = game_row.iloc[0]

    # Format and print the desired information:
    print(f"{row['id']}. {row['name']} ({row['yearpublished']}) - {row['average']:.2f}⭐")
    print(f"   Players: {row['minplayers']} - {row['maxplayers']}, Playtime: {row['playingtime']} min")
    print(f"   Tags: {row['tags']}")
    print(f"   Categories: {row['category_list']}")
    print(f"   Mechanics: {row['mech_list']}")
    print(f"   Average Weight: {row['averageweight']}")
    # Use description_clean if it exists; otherwise fallback to description:
    desc = row.get('description_clean', row.get('description', 'No description available'))
    print(f"   Description: {desc[:250]}...\n")



# FUNCTION: Use fuzzy matching on game name to handle user input
def find_closest_name(user_input, auto_select=False):
    matches = process.extract(user_input, game_index.keys(), scorer=fuzz.WRatio, limit=10)
    if auto_select:
        return matches[0][0]  # Automatically choose the highest-confidence match
    print("\nDid you mean:")
    for idx, (match, score, _) in enumerate(matches):
        print(f"{idx+1}. {match} ({round(score, 1)}%)")
    choice = input("Enter number to select or press Enter to choose best match: ")
    if choice.isdigit() and 1 <= int(choice) <= len(matches):
        return matches[int(choice) - 1][0]
    return matches[0][0]


# FUNCTION: Extract root game title for searching and filtering (to avoid duplicates)
def get_root_title(title):
    return title.split(':')[0].split('(')[0].strip().lower()
