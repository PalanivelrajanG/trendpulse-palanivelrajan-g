# Task 1 — TrendPulse Data Collection
# -----------------------------------
# Logic:
# 1. Fetch top story IDs from HackerNews
# 2. Fetch details for each story
# 3. Categorize stories using keywords
# 4. Collect max 25 stories per category
# 5. Save results as JSON inside data/ folder

import requests
import json
import os
import time
from datetime import datetime

# API URLs
TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"

headers = {"User-Agent": "TrendPulse/1.0"}

# Categories and keywords
categories = {
    "technology": ["ai", "software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["nfl", "nba", "fifa", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "nasa", "genome"],
    "entertainment": ["movie", "film", "music", "netflix", "game", "book", "show", "award", "streaming"]
}

MAX_PER_CATEGORY = 25


def get_top_story_ids():
    """
    Fetch top story IDs
    """
    try:
        response = requests.get(TOP_STORIES_URL, headers=headers, timeout=10)

        if response.status_code == 200:
            story_ids = response.json()
            return story_ids[:200]
        else:
            print("Failed to fetch top stories:", response.status_code)
            return []

    except Exception as e:
        print("Error fetching top stories:", e)
        return []


def get_story_details(story_id):
    """
    Fetch details for a single story
    """
    try:
        url = ITEM_URL.format(story_id)

        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            return response.json()
        else:
            print("Failed to fetch story:", story_id)
            return None

    except Exception as e:
        print("Error fetching story:", story_id, e)
        return None


def categorize_title(title):
    """
    Categorize title based on keywords
    """
    title_lower = title.lower()

    for category, keywords in categories.items():
        for word in keywords:
            if word in title_lower:
                return category

    return None


def main():

    print("Fetching top story IDs...")

    story_ids = get_top_story_ids()

    if not story_ids:
        print("No stories found.")
        return

    collected_stories = []

    category_count = {
        "technology": 0,
        "worldnews": 0,
        "sports": 0,
        "science": 0,
        "entertainment": 0
    }

    for story_id in story_ids:

        print("Checking story:", story_id)

        story = get_story_details(story_id)

        if story is None:
            continue

        title = story.get("title")

        if not title:
            continue

        category = categorize_title(title)

        if category is None:
            continue

        if category_count[category] >= MAX_PER_CATEGORY:
            continue

        record = {
            "post_id": story.get("id"),
            "title": title,
            "category": category,
            "score": story.get("score", 0),
            "num_comments": story.get("descendants", 0),
            "author": story.get("by"),
            "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        collected_stories.append(record)

        category_count[category] = category_count[category] + 1

        # stop if all categories reach 25
        if all(count >= MAX_PER_CATEGORY for count in category_count.values()):
            break

    # sleep 2 seconds per category (requirement)
    for cat in categories:
        time.sleep(2)

    # create data folder
    if not os.path.exists("data"):
        os.makedirs("data")

    filename = "data/trends_" + datetime.now().strftime("%Y%m%d") + ".json"

    try:
        with open(filename, "w") as file:
            json.dump(collected_stories, file, indent=4)

        print("Collected", len(collected_stories), "stories.")
        print("Saved to", filename)

    except Exception as e:
        print("Error saving file:", e)


if __name__ == "__main__":
    main()