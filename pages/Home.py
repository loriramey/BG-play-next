"""
page_title: Game Recommendations
"""

#This is the home page and also the main recommendation engine page
import streamlit as st
import numpy as np
import logging
from src.helper_funct import sanitize_input, find_closest_name, filter_games
from src.recommendation import get_rec_by_name
from src.external_file_download import download_large_file_with_progress
import os
import pandas as pd

# Determine the base directory (project root)
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)

gamedata_path = os.path.join(project_root, "data", "raw", "gamedata.csv")
matrix_path = os.path.join(project_root, "data", "matrices", "cosine_similarity_mech_heavy.npy")

#remote URL for large CS matrix file
remote_matrix_url = "https://truenamegames.com/matrices/cosine_similarity_mech_heavy.npy"

#preload the large data files
if "gamedata" not in st.session_state:
    st.session_state["gamedata"] = pd.read_csv(gamedata_path)
if "cosine_sim_primary" not in st.session_state:
    if not os.path.exists(matrix_path):
        st.info("Matrix file note found locally, downloading it...")
        download_large_file_with_progress(remote_matrix_url, matrix_path)
    st.session_state["cosine_sim_primary"] = np.load(matrix_path)

def display_welcome():
    """Display the title and welcome message."""
    st.title("Play Next")
    st.header("Find your next favorite Board Game!")
    st.write("Enter a title to search for similar games.")
    st.write("Set filters using the options on the left.")

    if st.sidebar.button("Restart App"):
        st.session_state.clear()
        st.rerun()

def get_user_input():
    """Get and sanitize user input from a text field."""
    raw_input = st.text_input("Enter a board game name:")
    # Call your external sanitize function
    return sanitize_input(raw_input) if raw_input else None


def show_filter_sidebar():
    """Display filtering options in the sidebar and return the filter values as a dict."""

    st.sidebar.header("Filter your Results:")
    min_players = st.sidebar.number_input("Min Players", min_value=1, value=1)
    max_players = st.sidebar.number_input("Max Players", min_value=1, value=8)
    max_playtime = st.sidebar.number_input("Max Playtime (minutes)", min_value=5, value=200)
    min_avg = st.sidebar.slider("Minimum User Rating", min_value=1.0, max_value=10.0, value=5.0, step=0.1)
    min_weight = st.sidebar.slider("Average Weight (Complexity", min_value=1.0, max_value=5.0, value=1.0, step=0.1)
    min_year = st.sidebar.number_input("Minimum Publication Year", min_value=1900, value=1970)
    return {
        "min_players": min_players,
        "max_players": max_players,
        "max_playtime": max_playtime,
        "min_avg": min_avg,
        "min_weight": min_weight,
        "min_year": min_year
    }

def display_results(recommended_games):
    """Display the recommendation results as expandable sections."""
    logging.info(f"After filtering: {len(recommended_games)} games remaining")  #FOR DEBUG
    for i, row in recommended_games.head(25).iterrows():
        with st.expander(f"{row['name']}"):
            # Show a thumbnail if available
            if pd.notna(row["thumbnail"]):
                st.image(row["thumbnail"], width=100)

            #catch any NaN data before printing to view
            # Use inline conditionals to replace NaN values with "N/A"
            year = int(row['yearpublished']) if pd.notna(row['yearpublished']) else "N/A"
            min_players = row['minplayers'] if pd.notna(row['minplayers']) else "N/A"
            max_players = row['maxplayers'] if pd.notna(row['maxplayers']) else "N/A"
            playtime = row['playingtime'] if pd.notna(row['playingtime']) else "N/A"
            rating = row['average'] if pd.notna(row['average']) else "N/A"
            weight = row['averageweight'] if pd.notna(row['averageweight']) else "N/A"
            similarity = f"{row['similarity']:.2f}" if pd.notna(row['similarity']) else "N/A"
            description = row['description_clean'] if pd.notna(row['description_clean']) else "N/A"

            #write results to screen
            st.write(f"**Year Published:** {year}")
            st.write(f"**Min / Max Players:** {min_players} - {max_players}")
            st.write(f"**Expected Playtime:** {playtime} minutes")
            st.write(f"**Average User Rating (out of 10):** {rating}")
            st.write(f"**Complexity Weight (out of 5):** {weight}")
            st.write(f"**Similarity Score:** {similarity}")
            st.write(f"**Description:** {description}")


def home_page():
    """Main function to drive the Home page."""
    display_welcome()
    user_input = get_user_input()   #this incorporates sanitization function

    if user_input:
        # fuzzy search & offer 8 options based on title
        candidates = find_closest_name(user_input, auto_select=False)
        options = [f"{c['name']} ({round(c['score'], 1)}%)" for c in candidates]
        selected_option = st.selectbox("Select the game you meant:", options)   #have user confirm game to look up
        selected_game = selected_option.split(" (")[0]           #Extract game name from this format
        st.write("You selected", selected_game)

        # Button to trigger recommendation engine; store result in session_state
        if st.button("Get Recommendations") or "recommendations" not in st.session_state:
            try:
                recs = get_rec_by_name(selected_game, auto_select=False)
                st.session_state["recommendations"] = recs
                st.session_state["selected_game"] = selected_game
                logging.info(f"Recommendations computed for {selected_game}")
            except Exception as e:
                logging.error(f"Error computing recommendations: {e}")
                st.error("There was an error computing recommendations. Please try again.")

        #Always show the filter sidebar to allow dynamic adjustments.
        filters = show_filter_sidebar()

        if "recommendations" in st.session_state:
            # Apply filtering to the recommendations
            filtered_recs = filter_games(st.session_state["recommendations"], filters)
            st.subheader(f"Recommendations for {st.session_state['selected_game']}")
            st.write("Please click on a title to expand it and see more information.")
            display_results(filtered_recs)


if __name__ == "__main__":
    home_page()
