import pandas as pd
import matplotlib.pyplot as plt
import logging

GAMEDATA_FILE = "/Users/loriramey/PycharmProjects/BGPlayNext/data/raw/gamedata.csv"

# Load master data and cosine similarity matrix
df = pd.read_csv(GAMEDATA_FILE)

def plot_bayes_rating_distribution(df, output_file="avg_user_rating_distribution.png"):
    """
    Generates a histogram of the bayesaverage column and saves it as an image file.

    Parameters:
        df (pandas.DataFrame): Your game data containing a 'bayesaverage' column.
        output_file (str): Filename to save the plot image (PNG by default).
    """
    # Ensure bayesaverage is numeric, drop rows where it's NaN
    df['bayesaverage'] = pd.to_numeric(df['bayesaverage'], errors='coerce')
    df_clean = df.dropna(subset=['bayesaverage'])

    plt.figure(figsize=(8, 6))
    plt.hist(df_clean['bayesaverage'], bins=20, edgecolor='black', range=(1, 10))
    plt.title("Distribution of Bayesian User Ratings")
    plt.xlabel("Bayesian Rating (1-10)")
    plt.ylabel("Frequency")
    plt.tight_layout()

    plt.savefig(output_file)
    plt.close()
    print(f"Histogram saved to {output_file}")

def plot_average_rating_distribution(df, output_file="avg_user_rating_distribution.png"):
    """
    Generates a histogram of the bayesaverage column and saves it as an image file.

    Parameters:
        df (pandas.DataFrame): Your game data containing a 'bayesaverage' column.
        output_file (str): Filename to save the plot image (PNG by default).
    """
    # Ensure bayesaverage is numeric, drop rows where it's NaN
    df['average'] = pd.to_numeric(df['average'], errors='coerce')
    df_clean = df.dropna(subset=['average'])

    plt.figure(figsize=(8, 6))
    plt.hist(df_clean['average'], bins=20, edgecolor='black', range=(1, 10))
    plt.title("Distribution of Average Unweighted User Ratings")
    plt.xlabel("Average User Rating (1-10)")
    plt.ylabel("Frequency")
    plt.tight_layout()

    plt.savefig(output_file)
    plt.close()
    print(f"Histogram saved to {output_file}")

if __name__ == "__main__":
    # Load your game data; adjust the path as needed
    df = pd.read_csv("/Users/loriramey/PycharmProjects/BGPlayNext/data/raw/gamedata.csv")
    plot_bayes_rating_distribution(df)
    plot_average_rating_distribution(df)