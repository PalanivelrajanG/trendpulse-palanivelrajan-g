# Name: Arun Ganesh
# File: task3_analysis.py
# Project: TrendPulse - What's Actually Trending Right Now
# Task: Analyse cleaned trend data using Pandas and NumPy

import pandas as pd
import numpy as np

# -------------------------------
# Task 1 — Load and Explore Data
# -------------------------------

# Load the cleaned CSV created in Task 2
df = pd.read_csv("data/trends_clean.csv")

# Print shape of dataset
print("Loaded data:", df.shape)

# Print first 5 rows
print("\nFirst 5 rows:")
print(df.head())

# Calculate averages
avg_score = df["score"].mean()
avg_comments = df["num_comments"].mean()

print("\nAverage score   :", round(avg_score, 2))
print("Average comments:", round(avg_comments, 2))


# ----------------------------------
# Task 2 — Basic Analysis with NumPy
# ----------------------------------

print("\n--- NumPy Stats ---")

# Convert columns to NumPy arrays
scores = df["score"].to_numpy()
comments = df["num_comments"].to_numpy()

# Mean, median, std deviation
mean_score = np.mean(scores)
median_score = np.median(scores)
std_score = np.std(scores)

print("Mean score   :", round(mean_score, 2))
print("Median score :", round(median_score, 2))
print("Std deviation:", round(std_score, 2))

# Max and Min score
print("Max score    :", np.max(scores))
print("Min score    :", np.min(scores))

# Category with most stories
category_counts = df["category"].value_counts()
top_category = category_counts.idxmax()
top_count = category_counts.max()

print("\nMost stories in:", top_category, "(" + str(top_count) + " stories)")

# Story with most comments
max_comments_index = np.argmax(comments)

top_story_title = df.loc[max_comments_index, "title"]
top_story_comments = df.loc[max_comments_index, "num_comments"]

print("\nMost commented story:", '"' + str(top_story_title) + '"',
      "—", top_story_comments, "comments")


# ----------------------------------
# Task 3 — Add New Columns
# ----------------------------------

# Engagement formula: num_comments / (score + 1)
df["engagement"] = df["num_comments"] / (df["score"] + 1)

# is_popular column: True if score > average score
df["is_popular"] = df["score"] > avg_score


# -------------------------------
# Task 4 — Save Updated Dataset
# -------------------------------

df.to_csv("data/trends_analysed.csv", index=False)

print("\nSaved to data/trends_analysed.csv")