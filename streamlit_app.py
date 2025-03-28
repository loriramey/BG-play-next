import streamlit as st
import logging
from pages import Home, About, DataViz

# --- Logging Setup ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)
logging.info("Streamlit app started.")


# --- Navigation Setup ---
def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Select a page:", ["Game Recommendations", "Explore Data", "About"])

    if page == "Game Recommendations":
        Home.home_page()
    elif page == "Explore Data":
        DataViz.dataviz_page()
    elif page == "About":
        About.about_page()



if __name__ == "__main__":
    main()