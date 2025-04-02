"""
page_title: About the Project
"""

# rest of your code...


#This page displays information about the creator and the project
import streamlit as st

def show_about_info():
    """Display project, file, and license information."""
    st.title("About Play Next")
    st.header("About the Project")
    st.markdown("""
            **Play Next** is a board game recommendation app designed to help you discover your next favorite game.

            \n\n  It leverages data from BoardGameGeek and incorporates a custom recommendation engine. 
            \nThe app is built with Python and Streamlit, making it easy to interact with and visualize data.
            \nThe recommendation engine uses a cosine similarity matrix constructed from data about each game, 
             including the game's listed mechanics, game category information, and other key metrics. 
             
            \n\n  You can explore the data for yourself in the Data Visualization tab on the left. There are 25,700 games
             in the database that drives this app. Game data includes the average BGG rating for the game, its BGG rank, description information,
             and lists of characteristics such as minimum and maximum player counts, typical play time, category and mechanics tags, and more.
             
            \n\n  This app represents the output of my capstone project to complete a B.S. in Computer Science from Western Governors University. 
            \n I hope to continue improving the app's recommendation engine and features as I grow my coding skills.
        """)
    st.markdown("""---""")

    st.subheader("About the Data and License")
    st.markdown("""
            The base game data files come from a public dataset on [Kaggle](https://www.kaggle.com/datasets/jvanelteren/boardgamegeek-reviews?select=games_detailed_info2025.csv),
             obtained through the BoardGameGeek.com API under their [license](https://boardgamegeek.com/wiki/page/XML_API_Terms_of_Use), 
             used within the scope of their terms of use.
             \n\n  This app is published under the terms of an [MIT license](https://opensource.org/licenses/mit). I would appreciate being credited
             if you find this app useful and link to it. Thanks!
             \n\n  Last updated: Spring 2025
        """)
    st.image("visualizations/BGGlogo.png.webp")
    st.markdown("""---""")

    st.subheader("About the Creator")
    st.write("I'm a passionate board game enthusiast, developer, researcher, and educator located in the United States.")
    st.image("visualizations/creator_headshot.jpg", caption="App Creator", width = 100)


def about_page():
    """Main function for the About page."""
    show_about_info()


if __name__ == "__main__":
    about_page()
