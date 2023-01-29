from dotenv import load_dotenv
import os
import sys
import praw
load_dotenv()
sys.path.append(r"C:\Users\Siddharth\Desktop\NTU COURSE STUFF\Y4S2\CE4034\Project")

from constants import subreddits

client_id = os.environ.get("CLIENT_ID")
client_secret = os.environ.get("CLIENT_SECRET")
user_agent = os.environ.get("USER_AGENT")

reddit = praw.Reddit(
    client_id = client_id,
    client_secret = client_secret,
    user_agent = user_agent
)

for subreddit in subreddits.keys():
    print("==========SUBREDDIT {}==========".format(subreddit))
    for submission in reddit.subreddit(subreddit).controversial(limit=10):
        print("==========SUBMISSION {}==========".format(submission.id))
        print("TITLE: {}".format(submission.title.encode('utf-8')))
        submission.comments.replace_more(limit=None)
        for comment in submission.comments.list(): # list function of CommentForest gets all comments as well as replies
            print(comment.body.encode('utf-8'))