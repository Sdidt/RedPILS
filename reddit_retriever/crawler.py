from dotenv import load_dotenv
import os
import sys
import praw
import pickle
from pprint import pprint
from collections import defaultdict
import pysolr
load_dotenv()
sys.path.append(os.environ.get("SYS_PATH"))

from constants import subreddits
from models.comment import Comment

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

        # self.solr = pysolr.Solr('http://localhost:8983/solr/', always_commit=True)
        # self.solr_health_check()
        # self.solr_add_document({
        #     "id": "doc_1",
        #     "title": "A test document"
        # })
    
    # def solr_health_check(self):
    #     res = self.solr.ping()
    #     print(res)
    
    # def solr_add_document(self, doc):
    #     self.solr.add([doc])

    def crawl_data(self):
        sub_data = defaultdict(lambda: {})
        for subreddit in subreddits.keys():
            print("==========SUBREDDIT {}==========".format(subreddit))
            sub_data[subreddit] = []
            sub = self.reddit.subreddit(subreddit)
            for submission in sub.controversial(limit=3):
                print("==========SUBMISSION {}==========".format(submission.id))
                print("TITLE: {}".format(submission.title.encode('utf-8')))
                submission.comments.replace_more(limit=3)
                print(vars(submission.comments))
                comments = submission.comments.list()
                # comments = [comment.body.encode('utf-8') for comment in submission.comments.list()]
                comments = self.filter_comments(comments)
                sub_data[sub.id][submission.id] = {
                    "title": submission.title,
                    "comments": [Comment(
                        id=comment.id, 
                        comment=comment.body.encode('utf-8'),
                        timestamp=comment.created_utc,
                        url=comment.permalink,
                        score=comment.score,
                        redditor_id=comment.author.id
                     ) for comment in comments] # the RHS in this list can later be traversed in a BFS manner to retrieve all the comments preserving tree structure
                }
                # self.store_raw_data(dict(sub_data))
                # self.store_data(dict(sub_data))
    

    def filter_comments(self, comments):
        filtered_comments = [comment for comment in comments if (comment != b'[removed]' and comment != b'[deleted]' and (len(comment.split(b" ")) >= 15))]
        return filtered_comments

    def store_raw_data(self, sub_data):
        with open("outputs/raw_output.txt", "w", encoding='utf-8') as f:
            pprint(sub_data, f)

    def store_data(self, sub_data):
        isExist = os.path.exists('./outputs')
        if not isExist:
            os.makedirs('./outputs')

        with open("outputs/sub_filtered_output.txt", "wb") as f:
            pickle.dump(sub_data, f)

    def append_data(self, comments):
        with open("outputs/filtered_output.txt", "ab") as f:
            pickle.dump(comments, f)

if __name__ == "__main__":
    crawler = Crawler()
    # crawler.crawl_data()