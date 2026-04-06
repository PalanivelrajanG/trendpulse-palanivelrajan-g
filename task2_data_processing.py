# Task 2 — TrendPulse Data Processing
# -----------------------------------
# Logic of this script:
# 1. Load the JSON file created in Task 1 into a Pandas DataFrame.
# 2. Clean the dataset:
#       - Remove duplicate stories based on post_id
#       - Remove rows with missing post_id, title, or score
#       - Convert score and num_comments to integers
#       - Remove stories with score < 5
#       - Remove extra whitespace from titles
# 3. Save the cleaned data to CSV.
# 4. Print summary information including stories per category.

import pandas as pd
import os
import glob


def main():

    # ------------------------------
    # Step 1 — Find the JSON file
    # ------------------------------

    json_files = glob.glob("data/trends_*.json")

    if not json_files:
        print("No JSON file found in data/ folder.")
        return

    # Take the most recent file
    json_file = sorted(json_files)[-1]

    # ------------------------------
    # Step 2 — Load JSON into DataFrame
    # ------------------------------

    df = pd.read_json(json_file)

    print("Loaded", len(df), "stories from", json_file)

    # ------------------------------
    # Step 3 — Remove duplicates
    # ------------------------------

    df = df.drop_duplicates(subset="post_id")

    print("After removing duplicates:", len(df))

    # ------------------------------
    # Step 4 — Remove missing values
    # ------------------------------

    df = df.dropna(subset=["post_id", "title", "score"])

    print("After removing nulls:", len(df))

    # ------------------------------
    # Step 5 — Fix data types
    # ------------------------------

    df["score"] = df["score"].astype(int)
    df["num_comments"] = df["num_comments"].astype(int)

    # ------------------------------
    # Step 6 — Remove low-quality stories
    # ------------------------------

    df = df[df["score"] >= 5]

    print("After removing low scores:", len(df))

    # ------------------------------
    # Step 7 — Clean whitespace in titles
    # ------------------------------

    df["title"] = df["title"].str.strip()

    # ------------------------------
    # Step 8 — Save cleaned CSV
    # ------------------------------

    output_file = "data/trends_clean.csv"

    df.to_csv(output_file, index=False)

    print("Saved", len(df), "rows to", output_file)

    # ------------------------------
    # Step 9 — Print category summary
    # ------------------------------

    print("\nStories per category:")

    category_counts = df["category"].value_counts()

    for category, count in category_counts.items():
        print(" ", category, " ", count)


if __name__ == "__main__":
    main()