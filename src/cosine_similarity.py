import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import pickle
from scipy.sparse import hstack, vstack


#helper function to handle the pkl dictionary files
def load_tfidf_matrix(file_path, df):
    """
    Load a TF-IDF object from file_path. If it is a dictionary,
    rebuild a sparse matrix using the order of game IDs in df.
    """
    with open(file_path, "rb") as f:
        obj = pickle.load(f)
    # If the loaded object is a dict, convert it into a sparse matrix
    if isinstance(obj, dict):
        # Ensure that every game_id from df is in the dictionary.
        # Order the vectors according to df['id']
        tfidf_list = [obj[game_id] for game_id in df['id']]
        return vstack(tfidf_list)
    else:
        return obj

def compute_cosine_similarity(data_file, output_file, tfidf_files):
    """
    Compute and save a weighted cosine similarity matrix for a given dataset.

    Parameters:
    - data_file (str): Path to the dataset CSV file
    - output_file (str): Path to save the cosine similarity matrix (.npy)
    - tfidf_files (dict): Dictionary of TF-IDF .pkl paths:
        {
            'tags': path,
            'categories': path,
            'mechanics': path
        }

    Returns:
    - cosine_sim (np.ndarray): Cosine similarity matrix
    """

    #load all necessary files and put data in usable form for this function
    print(f"🔄 Loading data from: {data_file}")
    df = pd.read_csv(data_file)

    print("🔄 Loading precomputed TF-IDF vectors...")
    tfidf_tags_matrix = load_tfidf_matrix(tfidf_files['tags'], df)
    tfidf_categories_matrix = load_tfidf_matrix(tfidf_files['categories'], df)
    tfidf_mechanics_matrix = load_tfidf_matrix(tfidf_files['mechanics'], df)

    # Confirm shapes match dataset size
    expected_rows = df.shape[0]
    assert tfidf_tags_matrix.shape[0] == expected_rows, "Mismatch in TF-IDF tags row count"
    assert tfidf_categories_matrix.shape[0] == expected_rows, "Mismatch in TF-IDF categories row count"
    assert tfidf_mechanics_matrix.shape[0] == expected_rows, "Mismatch in TF-IDF mechanics row count"

    # Ensure scaled numeric columns exist and are numeric
    df['maxplayers_scaled'] = pd.to_numeric(df['maxplayers_scaled'], errors='coerce').fillna(0)
    df['playingtime_scaled'] = pd.to_numeric(df['playingtime_scaled'], errors='coerce').fillna(0)
    df['averageweight_scaled'] = pd.to_numeric(df['averageweight_scaled'], errors='coerce').fillna(0)

    # Expand numeric vectors to match TF-IDF sparse matrix format
    max_players_scaled = np.expand_dims(df['maxplayers_scaled'].values, axis=1)
    playtime_scaled = np.expand_dims(df['playingtime_scaled'].values, axis=1)
    avg_weight_scaled = np.expand_dims(df['averageweight_scaled'].values, axis=1)

    # Set weights for each ingredient in the model ("recipe" for game rec engine)
    WEIGHT_TAGS = 0.05
    WEIGHT_CATEGORIES = 0.35
    WEIGHT_MECHANICS = 0.35
    WEIGHT_MAXPLAYERS = 0.00
    WEIGHT_PLAYTIME = 0.05
    WEIGHT_AVGWEIGHT = 0.20
    #WEIGHT_TFIDF = WEIGHT_TAGS + WEIGHT_CATEGORIES + WEIGHT_MECHANICS

    # Construct full feature matrix with appropriate weights
    print("🧠Combining weighted features for similarity computation...")
    feature_matrix = hstack([
        tfidf_tags_matrix * WEIGHT_TAGS,
        tfidf_categories_matrix * WEIGHT_CATEGORIES,
        tfidf_mechanics_matrix * WEIGHT_MECHANICS,
        max_players_scaled * WEIGHT_MAXPLAYERS,
        playtime_scaled * WEIGHT_PLAYTIME,
        avg_weight_scaled * WEIGHT_AVGWEIGHT
    ])

    # Compute cosine similarity
    print("⚡ Computing cosine similarity...")
    cosine_sim = cosine_similarity(feature_matrix, feature_matrix)

    # Save as numpy array for faster lookup
    np.save(output_file, cosine_sim)
    print(f"✅ Cosine similarity matrix saved: {output_file}")
    print(f"🟢 Matrix Shape: {cosine_sim.shape}")

    return cosine_sim


#to run this function:
if __name__ == "__main__":
    data_file = "/Users/loriramey/PycharmProjects/BGapp/data/gamedata_sorted.csv"
    output_file = "/Users/loriramey/PycharmProjects/BGapp/data/cosine_similarity_cat_heavy.npy"
    tfidf_files = {
        "tags": "/Users/loriramey/PycharmProjects/BGapp/models/tfidf_tags.pkl",
        "categories": "/Users/loriramey/PycharmProjects/BGapp/models/tfidf_categories.pkl",
        "mechanics": "/Users/loriramey/PycharmProjects/BGapp/models/tfidf_mechanics.pkl"
    }

    compute_cosine_similarity(data_file, output_file, tfidf_files)