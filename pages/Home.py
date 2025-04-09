"""
page_title: Game Recommendations
"""

#This is the home page and also the main recommendation engine page
import streamlit as st
import logging
import os
import pandas as pd
from src.helper_funct import sanitize_input, find_closest_name, filter_games, load_parquet_file
from src.recommendation import get_rec_by_name

# Determine the base directory (project root)
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)

#data file paths / load key files
gamedata_path = os.path.join(project_root, "data", "processed", "gamedata.parquet")
parquet_dir = os.path.join(project_root, "data", "processed")
top300_path = os.path.join(project_root, "data", "raw", "BGGtop300.csv")

if "gamedata" not in st.session_state:
    st.session_state["gamedata"] = load_parquet_file(gamedata_path)
if "top300" not in st.session_state:
    st.session_state["top300"] = pd.read_csv(top300_path)
if "rec_mech" not in st.session_state:
    st.session_state["rec_mech"] = load_parquet_file(os.path.join(parquet_dir, "top50_mech_heavy.parquet"))
if "rec_cat" not in st.session_state:
    st.session_state["rec_cat"] = load_parquet_file(os.path.join(parquet_dir, "top50_cat_heavy.parquet"))
if "rec_mixed" not in st.session_state:
    st.session_state["rec_mixed"] = load_parquet_file(os.path.join(parquet_dir, "top50_mixed.parquet"))

def display_welcome():
    """Display the title and welcome message."""
    st.title("Play Next")
    st.header("Find your next favorite Board Game!")
    st.write("Enter a game title to search for similar games. Confirm which title is correct then click Get Recommendations below.")
    st.write("Set filters using the options on the left after initial results load. These filters update your results automatically.")
    st.write("Customize your recommendation by picking a focus for similarities.")

    if st.sidebar.button("Reset for New Search"):
        st.session_state.clear()
        st.rerun()

def get_user_input():
    """
    Display a radio button and text input for the user to enter a game title and choose a recommendation mode.

    Returns:
        tuple: A tuple containing the sanitized game title input (str) and the selected match mode (str).
               Match mode will be one of 'mech', 'cat', or 'mixed' corresponding to mechanics, theme, or blended focus.
    """
    st.subheader("Choose how you want to match games:")
    match_mode_display = st.radio(
        "Recommendation Mode",
        options=["Match a Blend of Characteristics", "Match Game Mechanics", "Match Game Theme"],
        index=0,
        help="Choose whether to prioritize game mechanics, theme, or a broad mix when finding similar games."
    )
    mode_map = {
        "Match a Blend of Characteristics": "mixed",
        "Match Game Mechanics": "mech",
        "Match Game Theme": "cat"
    }
    st.write("Click GET RECOMMENDATIONS below if you switch between modes")
    raw_input = st.text_input("Enter a board game name:")
    # Call your external sanitize function
    sanitized_input = sanitize_input(raw_input) if raw_input else None
    match_mode = mode_map[match_mode_display]
    return sanitized_input, match_mode


def show_filter_sidebar():
    """
    Display sidebar widgets allowing the user to filter game recommendations based on game attributes.

    Returns:
        dict: Dictionary containing user-specified filter values for:
              min_players, max_players, max_playtime, min_avg, min_weight, and min_year.
    """
    st.sidebar.header("Filter your Results:")
    min_players = st.sidebar.number_input("Min Players", min_value=1, max_value=2,value=1)
    max_players = st.sidebar.number_input("Max Players", min_value=1, value=12)
    max_playtime = st.sidebar.number_input("Max Playtime (minutes)", min_value=5, value=220)
    min_avg = st.sidebar.slider("Minimum User Rating", min_value=1.0, max_value=10.0, value=5.0, step=0.1)
    min_weight = st.sidebar.slider("Average Weight (complexity)", min_value=1.0, max_value=5.0, value=1.0, step=0.1)
    min_year = st.sidebar.number_input("Minimum Publication Year", min_value=1900, value=1970)
    return {
        "min_players": min_players,
        "max_players": max_players,
        "max_playtime": max_playtime,
        "min_avg": min_avg,
        "min_weight": min_weight,
        "min_year": min_year
    }

    # Show the original game as the first expandable block
    selected_df = st.session_state["gamedata"]
    selected_game_row = selected_df[selected_df["name"] == st.session_state["selected_game"]].iloc[0]
    with st.expander(f"{selected_game_row['name']} (Selected Game)"):
        if pd.notna(selected_game_row["thumbnail"]):
            st.image(selected_game_row["thumbnail"], width=100)
    
        year = int(selected_game_row['yearpublished']) if pd.notna(selected_game_row['yearpublished']) else "N/A"
        min_players = selected_game_row['minplayers'] if pd.notna(selected_game_row['minplayers']) else "N/A"
        max_players = selected_game_row['maxplayers'] if pd.notna(selected_game_row['maxplayers']) else "N/A"
        playtime = selected_game_row['playingtime'] if pd.notna(selected_game_row['playingtime']) else "N/A"
        rating = round(selected_game_row['average'], 2) if pd.notna(selected_game_row['average']) else "N/A"
        weight = roudn(selected_game_row['averageweight'], 2) if pd.notna(selected_game_row['averageweight']) else "N/A"
        description = selected_game_row['description_clean'] if pd.notna(selected_game_row['description_clean']) else "N/A"
    
        st.write(f"**Year Published:** {year}")
        st.write(f"**Min / Max Players:** {min_players} - {max_players}")
        st.write(f"**Expected Playtime:** {playtime} minutes")
        st.write(f"**Average User Rating (out of 10):** {rating}")
        st.write(f"**Complexity Weight (out of 5):** {weight}")
        st.write(f"**Description:** {description}")



def display_results(recommended_games):
    """
    Render the top recommended games in expandable UI sections with game details and images.

    Args:
        recommended_games (pd.DataFrame): DataFrame containing filtered and ranked board game recommendations.
    """
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
            rating = round(row['average'], 2) if pd.notna(row['average']) else "N/A"
            weight = round(row['averageweight'], 2) if pd.notna(row['averageweight']) else "N/A"
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
    """
    Main controller for the Home page. Manages game title input, game selection,
    recommendation generation, filtering, and display of results.
    """
    display_welcome()
    user_input, match_mode = get_user_input()   #this incorporates sanitization function

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
                recs = get_rec_by_name(selected_game, match_mode=match_mode, auto_select=False)
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

