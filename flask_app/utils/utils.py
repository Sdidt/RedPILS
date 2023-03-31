from dotenv import load_dotenv
import os
import sys
import json
import re
import datetime

load_dotenv()
print(os.environ.get("SYS_PATH"))
sys.path.append(os.environ.get("SYS_PATH"))

from reddit_retriever.solr_interface import solr_ingest
from utils.constants import solr_var

def process_query(query):
    operators = [" AND ", " OR ", " NOT "]
    processed_query=query
    for op in operators:
        regex_pattern = re.compile(re.escape(op), re.IGNORECASE)
        processed_query = regex_pattern.sub(op, processed_query)
    return processed_query
    
def search_db(query, K=10, d1="*", d2="*", intitle=""):
    data_ingest = solr_ingest(solr_var["solr_url"],solr_var['data_collection_name'],solr_var['headers'])
    time_elapsed, search_results = data_ingest.phrase_query(solr_var['data_collection_name'], query, 5, 10, 20, 40, d2, d1,K)
    search_results = [{
        "score": doc["score"],
        "comment": doc["comment"],
        "reddit_score": doc["reddit_score"],
        "url": "https://www.reddit.com" + doc["url"]
    } for doc in search_results]
    # [print("Score: {}\nComment: {}\nURL: {}".format(doc["score"], doc["comment"], doc["url"])) for doc in search_results]
    return time_elapsed, search_results

def avg_scores(search_results):
    reddit_avg=0
    score_avg=0
    if len(search_results)!=0:
        for item in search_results:
            reddit_avg+=item["reddit_score"]
            score_avg+=item["score"]
        reddit_avg/=len(search_results)
        score_avg/=len(search_results)
        
    return reddit_avg, score_avg

def process_date(timeframe=None):
    if timeframe==None:
        return "*", "*"
    # return "*", "*"
    current_time = datetime.datetime.utcnow()
    past_time = current_time - datetime.timedelta(days=int(timeframe)*30)
    return current_time.strftime("%Y-%m-%dT%H:%M:%SZ"), past_time.strftime("%Y-%m-%dT%H:%M:%SZ")