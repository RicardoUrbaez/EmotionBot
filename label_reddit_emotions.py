import json
import pandas as pd
from src.emotion_classifier import classify_emotion

# Step 1: Load posts
with open("data/reddit_posts.json", "r", encoding="utf-8") as f:
    posts = json.load(f)

# Step 2: Analyze emotions
emotion_data = []
for post in posts:
    scores = classify_emotion(post["selftext"])
    record = {
        "id": post["id"],
        "text": post["selftext"],
        "top_emotion": scores[0]['label']
    }

    # Add all 27 emotion scores
    for emotion in scores:
        record[emotion["label"]] = round(emotion["score"], 3)

    emotion_data.append(record)

# Step 3: Save to CSV
df = pd.DataFrame(emotion_data)
df.to_csv("data/reddit_emotions.csv", index=False)

print("✅ Done! Saved labeled data to data/reddit_emotions.csv")