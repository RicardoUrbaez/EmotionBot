import os
import praw
from dotenv import load_dotenv
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Load environment variables from .env
load_dotenv()

# Reddit API credentials
client_id = os.getenv("REDDIT_CLIENT_ID")
client_secret = os.getenv("REDDIT_CLIENT_SECRET")
username = os.getenv("REDDIT_USERNAME")
password = os.getenv("REDDIT_PASSWORD")
user_agent = os.getenv("REDDIT_USER_AGENT")

# Validate credentials
if not all([client_id, client_secret, username, password, user_agent]):
    logging.error("❌ Missing Reddit API credentials in the .env file.")
    raise ValueError("Ensure all required environment variables are set.")

# Config
subreddit_name = os.getenv("TARGET_SUBREDDIT", "all")
post_limit = int(os.getenv("POST_LIMIT", 100))

# Output folder
OUTPUT_DIR = "./data"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Initialize Reddit client
try:
    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        username=username,
        password=password,
        user_agent=user_agent
    )
    logging.info("✅ Successfully connected to Reddit API.")
except Exception as e:
    logging.error(f"❌ Failed to connect to Reddit: {e}")
    raise

def collect_reddit_posts():
    """
    Collects posts from a target subreddit and saves them to data/reddit_posts.json.
    """
    try:
        subreddit = reddit.subreddit(subreddit_name)
        posts = []

        logging.info(f"🔍 Collecting {post_limit} posts from r/{subreddit_name}...")

        for post in subreddit.hot(limit=post_limit):
            posts.append({
                "id": post.id,
                "title": post.title,
                "selftext": post.selftext,
                "score": post.score,
                "url": post.url,
                "created_utc": post.created_utc,
                "num_comments": post.num_comments,
                "subreddit": post.subreddit.display_name
            })

        output_path = os.path.join(OUTPUT_DIR, "reddit_posts.json")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(posts, f, indent=2)

        logging.info(f"✅ Saved {len(posts)} posts to {output_path}")
    except Exception as e:
        logging.error(f"❌ Error collecting posts: {e}")
        raise

# Run directly (optional)
if __name__ == "__main__":
    try:
        collect_reddit_posts()
    except Exception as e:
        logging.error(f"❌ Script failed: {e}")
