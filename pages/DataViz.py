"""
page_title: Data Visuals
"""


#Allow users to explore the data and visualize certain interactions

import streamlit as st
from src.interactive_viz import display_interactive_charts

def display_info():
    st.title("Data Overview")
    st.markdown("""
            **Play Next** runs on data obtained through a public Kaggle dataset (read more on the About page)
             which was originally pulled from BoardGameGeek.com's public API in early 2025. The data set
             contains 25,700 games after cleaning to remove entries missing information in major fields. 
             
             \n\n  You can explore the data via the visuals and interactive controls below.
    """)

def display_static_visuals():
    """Display static visual assets (e.g., PNG images) on the page."""
    st.header("Data Visualizations: Static Visuals")

    st.subheader("Games Published Each Year Since 1980")
    st.write("Note the scale for the left axis is hundreds")
    st.image("visualizations/games_per_year.png", caption="Games Per Year, in Hundreds")
    st.markdown("""---""")

    st.subheader("Distribution of Ratings in the Data Set")
    st.write("Here's how the average ratings are distributed across the data set.")
    st.image("visualizations/avg_user_rating_distribution.png", caption="Distribution of Ratings in the Data Set")
    st.write("These ratings are a raw average of user reviews.")
    st.markdown("""---""")

    st.subheader("Average Bayesian Rating per Publication Year since 1980")
    st.write("Here is the average Bayesian rating of games for each year since 1980.")
    st.image("visualizations/average_bayesaverage_per_year.png", caption="Average Rating for Each Year")
    st.markdown("""---""")

def dataviz_page():
    """Main function for the Data Visualization page."""
    display_info()
    display_static_visuals()
    display_interactive_charts()


if __name__ == "__main__":
    dataviz_page()
