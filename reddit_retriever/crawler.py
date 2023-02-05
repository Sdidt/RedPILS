from dotenv import load_dotenv
import os
import sys
import praw
import pickle
load_dotenv()
sys.path.append(r"C:\Users\Siddharth\Desktop\NTU COURSE STUFF\Y4S2\CE4034\Project")

from constants import subreddits, keywords

class Crawler:
    def __init__(self) -> None:
        self.client_id = os.environ.get("CLIENT_ID")
        self.client_secret = os.environ.get("CLIENT_SECRET")
        self.user_agent = os.environ.get("USER_AGENT")

        self.reddit = praw.Reddit(
            client_id = self.client_id,
            client_secret = self.client_secret,
            user_agent = self.user_agent
        )
    
    def crawl_data(self):
        sub_data = {}
        for subreddit in subreddits.keys():
            print("==========SUBREDDIT {}==========".format(subreddit))
            sub_data[subreddit] = []
            sub = self.reddit.subreddit(subreddit)
            for keyword in keywords:
                for submission in sub.search(keyword, limit=5):
                    print("==========SUBMISSION {}==========".format(submission.id))
                    print("TITLE: {}".format(submission.title.encode('utf-8')))
                    submission.comments.replace_more(limit=5)
                    comments = [comment.body.encode('utf-8') for comment in submission.comments.list()]
                    comments = self.filter_comments(comments)
                    sub_data[subreddit].extend(comments)
        self.store_data(sub_data)
                    # for comment in submission.comments.list(): # list function of CommentForest gets all comments as well as replies
                    #     print(comment.body.encode('utf-8'))
            # for submission in self.reddit.subreddit(subreddit).controversial(limit=5):
            #     print("==========SUBMISSION {}==========".format(submission.id))
            #     print("TITLE: {}".format(submission.title.encode('utf-8')))
            #     submission.comments.replace_more(limit=5)
            #     for comment in submission.comments.list(): # list function of CommentForest gets all comments as well as replies
            #         print(comment.body.encode('utf-8'))
    
    def filter_comments(self, comments):
        filtered_comments = [comment for comment in comments if (comment != b'[removed]' and (len(comment.split(b" ")) >= 15))]
        return filtered_comments

    def store_data(self, sub_data):
        with open("outputs/sub_filtered_output.txt", "wb") as f:
            pickle.dump(sub_data, f)

    def append_data(self, comments):
        with open("outputs/filtered_output.txt", "ab") as f:
            pickle.dump(comments, f)

if __name__ == "__main__":
    crawler = Crawler()
    crawler.crawl_data()