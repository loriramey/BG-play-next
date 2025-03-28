#This is the home page and also the main recommendation engine page

import streamlit as st
from src.helper_funct import sanitize_input, find_closest_name
from src.recommendation import get_rec_by_name

def display_welcome():
    """Display the title and welcome message."""
    st.title("Play Next - find your next Board Game!")
    st.write("Welcome! Use the controls below to search for and filter games.")

def get_user_input():
    """Get and sanitize user input from a text field."""
    raw_input = st.text_input("Enter a board game name:")
    # Call your external sanitize function
    return sanitize_input(raw_input) if raw_input else None

def perform_fuzzy_search(user_input):
    """Perform a rapid fuzzy search on the sanitized input and return a confirmed game selection."""
    # Stub: Implement fuzzy search and user confirmation
    # e.g., candidate_game = fuzzy_search_game(user_input)
    # confirmation step with st.selectbox or st.radio
    pass

def get_filters():
    """Retrieve filter settings from the user (min players, max players, max playtime, Bayesian rating, publication year)."""
    filters = {
        "min_players": st.number_input("Minimum Players", min_value=1, step=1),
        "max_players": st.number_input("Maximum Players", min_value=1, step=1),
        "max_playtime": st.number_input("Maximum Playtime", min_value=1, step=1),
        "min_bayesaverage": st.slider("Minimum Bayesian Rating", min_value=1.0, max_value=10.0, value=1.0, step=0.1),
        "publication_year": st.number_input("Publication Year (Min)", min_value=1800, step=1)
    }
    return filters

def display_recommendations(results):
    """Display recommendation results in the main page area."""
    # Stub: Render results using st.write, st.table, or other display functions
    pass

def home_page():
    """Main function to drive the Home page."""
    display_welcome()
    user_input = get_user_input()
    if user_input:
        confirmed_game = perform_fuzzy_search(user_input)
        filters = get_filters()
        recommendations = run_recommendation_engine(confirmed_game, filters)
        display_recommendations(recommendations)

if __name__ == "__main__":
    home_page()
