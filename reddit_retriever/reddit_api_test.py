from dotenv import load_dotenv
import os
import praw
load_dotenv()

client_id = os.environ.get("CLIENT_ID")
client_secret = os.environ.get("CLIENT_SECRET")
user_agent = os.environ.get("USER_AGENT")
username = os.environ.get("REDDIT_USERNAME")
password = os.environ.get("REDDIT_PASSWORD")

reddit = praw.Reddit(
    client_id = client_id,
    client_secret = client_secret,
    user_agent = user_agent,
    username = username,
    password = password
)

for flair in reddit.subreddit("india").flair(limit=None):
    print("Flair: {}".format(flair))
    # try:
    #     print("Title: {}".format(submission.title))
    #     print("Link Flair text: {}".format(submission.link_flair_text))
    #     print("Link Flair Template ID: {}".format(submission.link_flair_template_id))
    #     print("Author Flair Text: {}".format(submission.author_flair_text))
    # except:
    #     pass

    