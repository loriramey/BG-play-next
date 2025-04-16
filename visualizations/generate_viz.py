import pandas as pd
import matplotlib.pyplot as plt
import logging
import re

GAMEDATA_FILE = "/Users/loriramey/PycharmProjects/BGPlayNext/data/raw/gamedata.csv"
# Load master data and cosine similarity matrix
df = pd.read_csv(GAMEDATA_FILE)

# --- Descriptive Statistics & Basic Reports ---
def print_basic_stats(df, cols_to_print=None):
    """
    Print basic descriptive statistics about the dataset.

    Parameters:
        data (DataFrame): The full dataset.
        cols_to_print (list, optional): List of column names to include in the descriptive summary.
                                         If None, the summary for all columns is printed.
    """
    print("\n--- Basic Statistics ---")
    print(f"Total games in dataset: {len(df)}")

    # Check for expected columns and print their stats if available.
    if 'bayesaverage' in df.columns:
        print(f"Average rating [Bayes] (1-10): {df['bayesaverage'].mean():.2f}")
    if 'averageweight' in df.columns:
        print(f"Average complexity weight (1-5): {df['averageweight'].mean():.2f}")

    # Print descriptive summary for specified columns (or all columns if not specified)
    if cols_to_print is not None:
        summary = df[cols_to_print].describe(include='all')
    else:
        summary = df.describe(include='all')

    print("\nDescriptive Summary:")
    print(summary)


# --- Static Visualizations using Matplotlib ----
def plot_bayes_rating_distribution(df, output_file="avg_user_rating_distribution.png"):
    """
    Generates a histogram of the bayesaverage column and saves it as an image file.

    Parameters:
        df (pandas.DataFrame):  game data containing a 'bayesaverage' column.
        output_file (str): Filename to save the plot image (PNG by default).
    """
    # Ensure bayesaverage is numeric, drop rows where it's NaN
    df['bayesaverage'] = pd.to_numeric(df['bayesaverage'], errors='coerce')
    df_clean = df.dropna(subset=['bayesaverage'])

    plt.figure(figsize=(8, 6))
    plt.hist(df_clean['bayesaverage'], bins=20, edgecolor='black', range=(1, 10))
    plt.title("Distribution of Bayesian Average User Ratings")
    plt.xlabel("Bayesian Rating (scale 1-10)")
    plt.ylabel("Frequency")
    plt.tight_layout()

    plt.savefig(output_file)
    plt.close()
    print(f"Histogram saved to {output_file}")


def plot_average_rating_distribution(df, output_file="avg_user_rating_distribution.png"):
    """
    Generates a histogram of the unweighted average column and saves it as an image file.

    Parameters:
        df (pandas.DataFrame):  game data containing a 'average' column.
        output_file (str): Filename to save the plot image (PNG by default).
    """
    # Ensure bayesaverage is numeric, drop rows where it's NaN
    df['average'] = pd.to_numeric(df['average'], errors='coerce')
    df_clean = df.dropna(subset=['average'])

    plt.figure(figsize=(8, 6))
    plt.hist(df_clean['average'], bins=20, edgecolor='black', range=(1, 10))
    plt.title("Distribution of Average User Ratings")
    plt.xlabel("Average User Rating (1-10)")
    plt.ylabel("Frequency")
    plt.tight_layout()

    plt.savefig(output_file)
    plt.close()
    print(f"Histogram saved to {output_file}")


def plot_games_per_year(df):
    """
    Generate and save visualizations of the number of games published per year and the average Bayesian rating per year,
    filtering the data to only include games from 1970 until now.
    (Note: Negative values representing BC years are automatically excluded.)
    """
    if 'yearpublished' not in df.columns:
        print("Column 'yearpublished' not found in data.")
        return

    # Clean the 'yearpublished' column to ensure it's numeric
    df['yearpublished'] = pd.to_numeric(df['yearpublished'], errors='coerce')

    # Filter the data for games from 1970 onward (this will exclude negative values)
    filtered_data = df[df['yearpublished'] >= 1970].copy()

    # Count games per year and sort by year
    year_counts = filtered_data['yearpublished'].value_counts().sort_index()

    # Plot and save the games-per-year bar chart
    plt.figure(figsize=(10, 6))
    plt.bar(year_counts.index, year_counts.values)
    plt.title("Games Published per Year (1970-Present)")
    plt.xlabel("Year Published")
    plt.ylabel("Number of Games")
    plt.tight_layout()
    plt.savefig("games_per_year.png")
    plt.close()
    print("Games per year plot saved as games_per_year.png.")

    # Use the Bayesian average for computing yearly averages
    if 'bayesaverage' in filtered_data.columns:
        # Calculate average Bayesian rating per year
        avg_rating_per_year = filtered_data.groupby('yearpublished')['bayesaverage'].mean().reset_index()
        avg_rating_per_year.rename(columns={'bayesaverage': 'average_bayesaverage'}, inplace=True)

        # Save the average Bayesian rating data as a CSV
        avg_rating_per_year.to_csv("average_bayesaverage_per_year.csv", index=False)
        print("Average Bayesian rating per year exported to average_bayesaverage_per_year.csv.")

        # Plot and save the average Bayesian rating per year line chart
        plt.figure(figsize=(10, 6))
        plt.plot(avg_rating_per_year['yearpublished'], avg_rating_per_year['average_bayesaverage'], marker='o')
        plt.title("Average Bayesian Game Rating per Year (1970-Present)")
        plt.xlabel("Year Published")
        plt.ylabel("Average Bayesian Rating")
        plt.tight_layout()
        plt.savefig("average_bayesaverage_per_year.png")
        plt.close()
        print("Average Bayesian rating per year plot saved as average_bayesaverage_per_year.png.")
    else:
        print("Column 'bayesaverage' not found in data; skipping average rating computation.")


if __name__ == "__main__":
    # Load your game data; adjust the path as needed
    df = pd.read_csv("/Users/loriramey/PycharmProjects/BGPlayNext/data/raw/gamedata.csv")
    plot_bayes_rating_distribution(df)
    plot_average_rating_distribution(df)