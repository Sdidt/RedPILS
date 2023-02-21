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
    def __init__(self, output_filename) -> None:
        self.output_filename = output_filename
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

    def process_submission(self, submission):
        print("==========SUBMISSION {}==========".format(submission.id))
        print("TITLE: {}".format(submission.title.encode('utf-8')))
        submission.comments.replace_more(limit=1)
        comments = submission.comments.list()
        submission_id = submission.id
        # comments = [comment.body.encode('utf-8') for comment in submission.comments.list()]
        comments = self.filter_comments(comments)
        list_data = [
            Comment(
                submission_id=submission_id,
                submission_title=submission.title.encode('utf-8'), 
                id=comment.id, 
                comment=comment.body.encode('utf-8'),
                timestamp=comment.created_utc,
                url=comment.permalink,
                score=comment.score,
                redditor_id=comment.author.id if hasattr(comment, 'author') and hasattr(comment.author, 'id') else -1
                ) for comment in comments # the RHS in this list can later be traversed in a BFS manner to retrieve all the comments preserving tree structure
        ]
        # dict_data = {
        #     "title": submission.title.encode('utf-8'),
        #     "comments": [Comment(
        #         id=comment.id, 
        #         comment=comment.body.encode('utf-8'),
        #         timestamp=comment.created_utc,
        #         url=comment.permalink,
        #         score=comment.score,
        #         redditor_id=comment.author.id if hasattr(comment, 'author') and hasattr(comment.author, 'id') else -1
        #         ) for comment in comments] # the RHS in this list can later be traversed in a BFS manner to retrieve all the comments preserving tree structure
        # }
        return list_data

    def crawl_data(self):
        sub_data = defaultdict(lambda: {})
        for subreddit in subreddits.keys():
            print("==========SUBREDDIT {}==========".format(subreddit))
            sub_data[subreddit] = {}
            sub = self.reddit.subreddit(subreddit)
            for submission in sub.controversial(limit=10):
                sub_data[subreddit][submission.id] = self.process_submission(submission)
                # self.store_raw_data(dict(sub_data))
                self.store_data(dict(sub_data))
    
    def keyword_crawl(self, dynamic_keywords):
        sub_data = self.read_data()
        if sub_data == {}:
            print("Initializing sub data")
            sub_data = {subreddit: {} for subreddit in subreddits.keys()}
        for subreddit in subreddits.keys():
            print("==========SUBREDDIT {}==========".format(subreddit))
            sub = self.reddit.subreddit(subreddit)
            for keyword in dynamic_keywords:
                for submission in sub.search('flair: "Politics"+{}'.format(keyword), limit=3):
                    if submission.id not in sub_data[subreddit]:
                        sub_data[subreddit][submission.id] = self.process_submission(submission)
                        # self.store_raw_data(dict(sub_data))
                        self.store_data(dict(sub_data))

    def filter_comments(self, comments):
        filtered_comments = [comment for comment in comments if (comment.body.encode('utf-8') != b'[removed]' and comment.body.encode('utf-8') != b'[deleted]' and (len(comment.body.encode('utf-8').split(b" ")) >= 30))]
        return filtered_comments

    def store_raw_data(self, sub_data):
        with open("outputs/{}_raw.txt".format(self.output_filename), "w", encoding='utf-8') as f:
            pprint(sub_data, f)

    def store_data(self, sub_data):
        isExist = os.path.exists('./outputs')
        if not isExist:
            os.makedirs('./outputs')

        with open("outputs/{}.txt".format(self.output_filename), "wb") as f:
            pickle.dump(sub_data, f)

    def read_data(self):
        try:
            print("File exists!")
            with open("outputs/{}.txt".format(self.output_filename), "rb") as f:
                sub_data = pickle.load(f)
        except: 
            sub_data = {}
        return sub_data

    def append_data(self, comments):
        with open("outputs/{}.txt".format(self.output_filename), "ab") as f:
            pickle.dump(comments, f)
        
    def get_all_docs(self):
        sub_data = self.read_data()
        docs = {}
        for key in sub_data.keys():
            data = sub_data[key]
            if (data == []): # this exists due to my poor coding; should be removed later
                continue
            for value in data.values():
                # print({comment.id: comment.comment for comment in value["comments"]})
                docs |= {comment.id: comment.comment.decode("utf-8") for comment in value["comments"]}
        return docs

if __name__ == "__main__":
    crawler = Crawler()
    # crawler.crawl_data()