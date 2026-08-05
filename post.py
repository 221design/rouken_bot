import os
import requests
from requests_oauthlib import OAuth1

# GitHub Secretsから読み込む
API_KEY = os.environ["X_API_KEY"]
API_SECRET = os.environ["X_API_SECRET"]
ACCESS_TOKEN = os.environ["X_ACCESS_TOKEN"]
ACCESS_TOKEN_SECRET = os.environ["X_ACCESS_TOKEN_SECRET"]

POSTS_FILE = "posts.txt"
PROGRESS_FILE = "progress.txt"

def load_posts():
    with open(POSTS_FILE, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def load_progress():
    if not os.path.exists(PROGRESS_FILE):
        return 0
    with open(PROGRESS_FILE, "r") as f:
        return int(f.read().strip() or 0)

def save_progress(index):
    with open(PROGRESS_FILE, "w") as f:
        f.write(str(index))

def post_to_x(text):
    text = text.replace("\\n", "\n")
    url = "https://api.twitter.com/2/tweets"
    auth = OAuth1(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    res = requests.post(url, auth=auth, json={"text": text})
    res.raise_for_status()
    print("投稿成功:", res.json())

def main():
    posts = load_posts()
    index = load_progress()

    if index >= len(posts):
        index = 0

    post_to_x(posts[index])
    save_progress(index + 1)

if __name__ == "__main__":
    main()
