from dotenv import load_dotenv
import os
import praw
load_dotenv()

client_id = os.environ.get("CLIENT_ID")
client_secret = os.environ.get("CLIENT_SECRET")
user_agent = os.environ.get("USER_AGENT")

reddit = praw.Reddit(
    client_id = client_id,
    client_secret = client_secret,
    user_agent = user_agent
)

for submission in reddit.subreddit("india").top():
    print(submission.title)