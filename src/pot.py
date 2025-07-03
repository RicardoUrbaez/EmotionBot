import os
import json
import praw
from dotenv import load_dotenv
from transformers import pipeline
from datetime import datetime

# Load environment variables
load_dotenv()

reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    username=os.getenv("REDDIT_USERNAME"),
    password=os.getenv("REDDIT_PASSWORD"),
    user_agent=os.getenv("REDDIT_USER_AGENT"),
)

# Load the zero-shot classifier from Hugging Face
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# Define the 27 emotions

emotions = [
    "admiration", "amusement", "anger", "annoyance", "approval", "caring", "confusion",
    "curiosity", "desire", "disappointment", "disapproval", "disgust", "embarrassment",
    "excitement", "fear", "gratitude", "grief", "joy", "love", "nervousness", "optimism",
    "pride", "realization", "relief", "remorse", "sadness", "surprise", "SuicideWatch", "shock", "going downhill"
]

# Collect posts from a subreddit
subreddit_name = "mentalhealth"
subreddit = reddit.subreddit(subreddit_name)

data = []

print(f"Collecting posts from r/{subreddit_name}...")

for post in subreddit.hot(limit=30):
    result = classifier(post.title, emotions, multi_label=True)
    
    data.append({
        "id": post.id,
        "title": post.title,
        "author": str(post.author),
        "score": post.score,
        "upvote_ratio": post.upvote_ratio,
        "num_comments": post.num_comments,
        "created_utc": post.created_utc,
        "emotions": result["labels"],
        "scores": result["scores"],
        "timestamp": datetime.now().isoformat()
    })

# Save to JSON file
os.makedirs("data", exist_ok=True)
with open("data/emotion_data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print("Saved data to data/emotion_data.json")

for e in emotions:
    print(f" - {e['label']}: {e['score']:.2f}")