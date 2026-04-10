
# Import required libraries
import pandas as pd
import matplotlib.pyplot as plt
import os

# ------------------------------------
# Task 1 — Load Data and Setup
# ------------------------------------

# Load analysed dataset from Task 3
df = pd.read_csv("data/trends_analysed.csv")

# Create outputs folder if it does not exist
if not os.path.exists("outputs"):
    os.makedirs("outputs")

# ------------------------------------
# Chart 1 — Top 10 Stories by Score
# ------------------------------------

# Sort stories by score and select top 10
top_stories = df.sort_values(by="score", ascending=False).head(10)

# Shorten long titles (max 50 characters)
titles = []
for title in top_stories["title"]:
    if len(title) > 50:
        titles.append(title[:50] + "...")
    else:
        titles.append(title)

scores = top_stories["score"]

plt.figure(figsize=(8,6))
plt.barh(titles, scores)

plt.xlabel("Score")
plt.ylabel("Story Title")
plt.title("Top 10 Stories by Score")

plt.gca().invert_yaxis()

plt.tight_layout()
plt.savefig("outputs/chart1_top_stories.png")
plt.close()

# ------------------------------------
# Chart 2 — Stories per Category
# ------------------------------------

category_counts = df["category"].value_counts()

plt.figure(figsize=(8,6))
plt.bar(category_counts.index, category_counts.values)

plt.xlabel("Category")
plt.ylabel("Number of Stories")
plt.title("Stories per Category")

plt.tight_layout()
plt.savefig("outputs/chart2_categories.png")
plt.close()

# ------------------------------------
# Chart 3 — Score vs Comments
# ------------------------------------

popular = df[df["is_popular"] == True]
not_popular = df[df["is_popular"] == False]

plt.figure(figsize=(8,6))

plt.scatter(popular["score"], popular["num_comments"], label="Popular")
plt.scatter(not_popular["score"], not_popular["num_comments"], label="Not Popular")

plt.xlabel("Score")
plt.ylabel("Number of Comments")
plt.title("Score vs Comments")

plt.legend()

plt.tight_layout()
plt.savefig("outputs/chart3_scatter.png")
plt.close()

# ------------------------------------
# Bonus — Combined Dashboard
# ------------------------------------

fig, axes = plt.subplots(1, 3, figsize=(18,6))

# Chart 1 inside dashboard
axes[0].barh(titles, scores)
axes[0].set_title("Top Stories")
axes[0].set_xlabel("Score")
axes[0].invert_yaxis()

# Chart 2 inside dashboard
axes[1].bar(category_counts.index, category_counts.values)
axes[1].set_title("Stories per Category")
axes[1].set_xlabel("Category")
axes[1].set_ylabel("Count")

# Chart 3 inside dashboard
axes[2].scatter(popular["score"], popular["num_comments"], label="Popular")
axes[2].scatter(not_popular["score"], not_popular["num_comments"], label="Not Popular")
axes[2].set_title("Score vs Comments")
axes[2].set_xlabel("Score")
axes[2].set_ylabel("Comments")
axes[2].legend()

plt.suptitle("TrendPulse Dashboard")

plt.tight_layout()
plt.savefig("outputs/dashboard.png")
plt.close()

print("Charts saved in outputs/ folder")