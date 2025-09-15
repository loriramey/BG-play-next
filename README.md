# Play Next

**Play Next** is a Streamlit-based board game recommendation engine that uses data from BoardGameGeek (BGG) to help users find their next favorite board game. It leverages a cosine similarity engine, fuzzy matching for game titles, and interactive data visualizations to provide personalized recommendations and insights into the game data.

## Features

- **Game Recommendations:**  
  Enter a board game title and get a list of similar games based on a precomputed cosine similarity matrix.
- **Fuzzy Search:**  
  Provides a dropdown of candidate games to ensure accurate title selection.
- **Interactive Visualizations:**  
  Explore data on Bayesian user ratings, playtime, game weight, and more through interactive charts.
- **Filtering:**  
  Adjust filters such as player count, playtime, rating, and publication year to refine recommendations.
- **Multipage Navigation:**  
  The app is organized into multiple pages (Home, Data Info, About) using Streamlit’s multipage functionality.

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/loriramey/BG-play-next.git
   cd BG-play-next
   
2. **Set up the virtual environment**

    `python -m venv venv
    source venv/bin/activate   # On Windows: venv\Scripts\activate
    pip install --upgrade pip
    pip install -r requirements.txt`

3. **Optional: Set up Git LFS for large files:**
If you aren't already using Git Large File Service (LFS), install and run:

    `git lfs install
    git lfs track "data/raw/*.*"
    git lfs track "data/processed/*.*"`


## Usage
**VERSION 2.0***

### Local Testing
**Run the app locally with Streamlit:**

    'streamlit run streamlit_app.py

This will start the app in your default web browser at http://localhost:8501.

## Deployment
You can deploy the app using Streamlit Cloud:

* Push your latest changes to GitHub.
* Go to Streamlit Cloud and create a new app by linking your repository.
* Configure any environment variables if needed and deploy.

## Project Structure
BG-play-next/  
├── streamlit_app.py                # Main entry point for the multipage Streamlit app  
├── requirements.txt                # Project dependencies  
├── .streamlit/  
│   └── config.toml                 # Streamlit configuration settings  
├── data/  
│   ├── raw/                        # Original CSV files (e.g., gamedata.csv, BGGtop300.csv)  
│   ├── processed/                  # Preprocessed data files  
│   └── matrices/                   # Precomputed cosine similarity matrices (tracked with Git LFS)  
├── pages/                          # Standalone pages for the multipage app  
│   ├── __init__.py  
│   ├── Home.py                     # Home page: recommendations & filters  
│   ├── DataViz.py                  # Data Info page: interactive visualizations  
│   └── About.py                    # About page: project details and credits  
└── src/                            # Core modules for app logic  
    ├── recommendation.py           # Recommendation engine code  
    ├── helper_funct.py             # Fuzzy search, sanitization, and other helper functions  
    ├── filters.py                  # Filtering functions for recommendation results  
    └── interactive_viz.py          # Functions to generate interactive visualizations  

### Configuration
The .streamlit/config.toml file contains all basic config settings for Streamlit.
Modify as needed.

### License
This project is open source. Please see the MIT License information in the sidebar.  

## Acknowledgements
* Data sourced from BoardGameGeek via their public API, obtained through Kaggle as a public data set.
* Kaggle [source](https://www.kaggle.com/datasets/jvanelteren/boardgamegeek-reviews?select=games_detailed_info2025.csv)
* Built using Streamlit and Python via PyCharm IDE
