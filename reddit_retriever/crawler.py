from __future__ import annotations  # required for older python versions before 3.9
from dotenv import load_dotenv
import os
import sys
import praw
from collections import defaultdict
load_dotenv()
sys.path.append(os.environ.get("SYS_PATH"))

from utils.constants import subreddits, solr_var
from utils.helpers import *
from models.comment import Comment
from reddit_retriever.solr_interface import solr_ingest

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

    def process_submission(self, submission, sub, comment_limit) -> list[Comment]:
        print("==========SUBMISSION {}==========".format(submission.id))
        print("TITLE: {}".format(submission.title.encode('utf-8')))
        submission.comments.replace_more(limit=comment_limit)
        comments = submission.comments.list()
        submission_id = submission.id
        # comments = [comment.body.encode('utf-8') for comment in submission.comments.list()]
        comments = self.filter_comments(comments)
        # list_data = [
        #     Comment(
        #         submission_id=submission_id,
        #         submission_title=submission.title.encode('utf-8'), 
        #         subreddit_id=sub.id,
        #         subreddit_name=sub.name,
        #         id=comment.id, 
        #         comment=comment.body.encode('utf-8'),
        #         timestamp=comment.created_utc,
        #         url=comment.permalink,
        #         score=comment.score,
        #         redditor_id=comment.author.id if hasattr(comment, 'author') and hasattr(comment.author, 'id') else -1
        #         ) for comment in comments 
        # ]
        list_data = []
        for comment in comments:
            dict_obj = {'submission_id':submission_id,
                        'submission_title':submission.title,
                        'subreddit_id':sub.id,
                        'subreddit_name':sub.name,
                        'comment_id':comment.id,
                        'comment':comment.body,
                        'timestamp':convert_to_datetime(comment.created_utc),
                        'url':comment.permalink,
                        'score':comment.score,
                        "redditor_id":comment.author.id if hasattr(comment, 'author') and hasattr(comment.author, 'id') else -1}
            list_data.append(dict_obj)
        # Alternative:
        # dict_data = {
        #     "title": submission.title.encode('utf-8'),
        #     "comments": [Comment(
        #         id=comment.id, 
        #         comment=comment.body.encode('utf-8'),
        #         timestamp=comment.created_utc,
        #         url=comment.permalink,
        #         score=comment.score,
        #         redditor_id=comment.author.id if hasattr(comment, 'author') and hasattr(comment.author, 'id') else -1
        #         ) for comment in comments] 
        # }
        return list_data

    def crawl_data(self,crawl_limit,submission_limit):
        sub_data = defaultdict(lambda: {})
        for subreddit in subreddits.keys():
            print("==========SUBREDDIT {}==========".format(subreddit))
            sub = self.reddit.subreddit(subreddit)
            for submission in sub.controversial(limit=crawl_limit):
                sub_data[subreddit][submission.id] = self.process_submission(submission,submission_limit)
                # self.store_raw_data(dict(sub_data))
                # the following 2 lines are for testing purposes; in the future they will be replaced by a call to add the documents to solr directly
                # store_json(sub_data)
                store_data(sub_data)
    
    def keyword_crawl(self, dynamic_keywords, keyword_limit, submission_limit, data_ingest: solr_ingest):
        sub_data: list[Comment] = read_data(self.output_filename)
        for subreddit in subreddits.keys():
            print("==========SUBREDDIT {}==========".format(subreddit))
            sub = self.reddit.subreddit(subreddit)
            for keyword in dynamic_keywords:
                for submission in sub.search('flair: "Politics"+{}'.format(keyword), limit=keyword_limit):
                    # relies on overloaded __eq__
                    # if submission.id not in sub_data:
                    if not data_ingest.check_submission_exists(solr_var['data_collection_name'], submission.id):
                        submission_result = self.process_submission(submission, sub, submission_limit)
                        sub_data.extend(submission_result)
                        print("extracted data")
                        # self.store_raw_data(dict(sub_data))
                        # the following 2 lines are for testing purposes; in the future they will be replaced by a call to add the documents to solr directly
                        # json_sub_data = process_json(sub_data)
                        # print("processed data as json")
                        data_ingest.push_data(solr_var['data_collection_name'],submission_result)
                        print("pushed data")
                        store_json(sub_data, self.output_filename)
                        store_data(sub_data, self.output_filename)
                        print("storing data")

    def filter_comments(self, comments):
        # filtered_comments = [comment for comment in comments if (comment.body.encode('utf-8') != b'[removed]' and comment.body.encode('utf-8') != b'[deleted]' and (len(comment.body.encode('utf-8').split(b" ")) >= 30))]
        filtered_comments = [comment for comment in comments if (comment.body.encode('utf-8') != b'[removed]' and comment.body.encode('utf-8') != b'[deleted]' and (len(comment.body.encode('utf-8').split(b" ")) >= 30))]
        return filtered_comments
    
    def get_all_docs(self):
        # in the future; read from solr; ideally, this function should not even be here. When dynamic crawling begins, just need to call that function with keywords, and documents are added one by one into solr so no need to read data b4 writing
        sub_data = read_data(self.output_filename)
        docs = {}
        for comment in sub_data:
            # docs[comment['comment_id']] = comment['comment'].decode("utf-8")
            docs[comment['comment_id']] = comment['comment']
        return docs

if __name__ == "__main__":
    crawler = Crawler()
    # crawler.crawl_data()