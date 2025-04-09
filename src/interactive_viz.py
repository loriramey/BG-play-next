#This code runs the interactive data visualizations part of DataViz

import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def load_dataset(dataset_name: str) -> pd.DataFrame:
    """Load dataset by name, with fallback loading if session cache is missing."""
    if dataset_name == "Top 300 Games":
        if "top300" not in st.session_state:
            st.session_state["top300"] = pd.read_csv("data/raw/BGGtop300.csv")
        return st.session_state["top300"]
    else:
        if "gamedata" not in st.session_state:
            st.session_state["gamedata"] = pd.read_parquet("data/processed/gamedata.parquet")
        return st.session_state["gamedata"]


def display_interactive_charts():
    """Display interactive visualizations (e.g., Plotly charts) on the page."""
    st.header("Interactive Data Visualizations")

    # Let the user choose which dataset to use
    dataset_option = st.selectbox("Choose Dataset:",
                                  options=["Top 300 Games", "Full Dataset"],
                                  key="dataset_option")
    df = load_dataset(dataset_option)

    # Ensure key columns are numeric
    for col in ["average", "playingtime", "averageweight", "BGGrank"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Let the user choose which correlation to display

    chart_option = st.selectbox("Select chart to display:",
                                options=["Average Game Rating vs Playtime",
                                         "Average Game Rating vs BGG Rank",
                                         "Average Game Rating vs Game Weight"],
                                key="chart_option")

    if chart_option == "Average Game Rating vs Playtime":
        x_col = "playingtime"
        x_label = "Playtime (in minutes)"
    elif chart_option == "Average Game Rating vs BGG Rank":
        x_col = "BGGrank"
        x_label = "Board Game Geek Ranking"
    elif chart_option == "Average Game Rating vs Game Weight":
        x_col = "averageweight"
        x_label = "Game Weight (scale 1-5)"
    else:
        x_col = "playingtime"
        x_label = "Playtime (in minutes)"

    # Allow the user to adjust the x-axis range
    x_min = float(df[x_col].min())
    x_max = float(df[x_col].max())
    x_range = st.slider(f"Select {x_label} range:", min_value=x_min, max_value=x_max, value=(x_min, x_max))

    # Filter the DataFrame based on the selected range
    df_filtered = df[(df[x_col] >= x_range[0]) & (df[x_col] <= x_range[1])]

    # Create a scatter plot using Plotly Express
    fig = px.scatter(
        df_filtered,
        x=x_col,
        y="average",
        labels={x_col: x_label, "bayesaverage": "Bayesian Rating (1-10)"},
        title=f"Correlation: Bayesian Rating vs {x_label}"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Data Definitions")
    st.markdown("""
            The above visualizations use a Bayesian corrected **average game review** by users, as provided by the BoardGameGeek API.
             A Bayesian rating has been statistically adjusted to moderate the way games with fewer than 1,000 user ratings can be disproportionately
             influenced by 1's or 10's in their reviews. As a game receives more reviews to reach that threshold of a thousand reviews (or many more), 
             the Bayes average approaches the simple average of all reviews. For games with fewer reviews, the Bayesian average tends to pull the raw 
             average more toward the middle (a 5-6) rather than the extremes.
            \n\n  The **BGG rank** metric refers to the value BoardGameGeek assigns to every game in its database based on its own
             internal measures. You are likely familiar with their lists like "Top 50 Games" which use this measure.
            \n\n  The **weight** of a game is measured by players on a scale of 1-5, where higher ratings represent
             higher complexity of mechanics. A lower weight means the game is likely simpler to understand and easy to pick up and play,
             or a good fit for younger players. 
            \n\n  The database tracks **playing time** which is an average length of a game in minutes. This number has been modified for my app
             from what is originally output from the API to deal with extreme outlier game campaigns with lengths of greater than 6 hours. 
             This data set will not report playing time longer than 720 minutes, but individual game pages from BGG.com will show the actual times.
    """)
