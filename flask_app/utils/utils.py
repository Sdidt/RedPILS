from dotenv import load_dotenv
import os
import sys
import json
import re
import datetime
import random

load_dotenv()
print(os.environ.get("SYS_PATH"))
sys.path.append(os.environ.get("SYS_PATH"))

from reddit_retriever.solr_interface import solr_ingest
from utils.constants import solr_var

def process_query(query):
    operators = [" AND ", " OR ", " NOT "]
    words=query.split()
    
    print(query)
    processed_query=query
    for op in operators:
        regex_pattern = re.compile(re.escape(op), re.IGNORECASE)
        processed_query = regex_pattern.sub(op, processed_query)
    for word in words:
        if word.upper() not in ["AND", "OR", "NOT", ")", "(", "~"]:
            processed_query= processed_query.replace(word, word+"~3")
    return processed_query
    
def search_db(query, K=10, d1="*", d2="*", intitle=""):
    data_ingest = solr_ingest(solr_var["solr_url"],solr_var['data_collection_name'],solr_var['headers'])
    time_elapsed, search_results = data_ingest.phrase_query(solr_var['data_collection_name'], query, 5, 10, 20, 40, d1, d2, intitle,K)
    num_results=len(search_results)
    search_results=search_results[:K]
    search_results = [{
        "score": doc["score"],
        "comment": doc["comment"],
        "reddit_score": doc["reddit_score"],
        "url": "https://www.reddit.com" + doc["url"],
        #replace label with actual label
        "political_leaning": random.choice(["-2", "-1", "0", "1", "2"])
    } for doc in search_results]
    # [print("Score: {}\nComment: {}\nURL: {}".format(doc["score"], doc["comment"], doc["url"])) for doc in search_results]
    return time_elapsed, num_results, search_results

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

def process_date(timeframe=None, sd=None, ed=None):
    print(sd, ed, timeframe)
    if timeframe==None and sd==None:
        return "*", "*"
    elif sd!=None:
        dt1 = datetime.datetime.strptime(sd, '%d%m%Y')
        dt2 = datetime.datetime.strptime(ed, '%d%m%Y')
        return dt1.strftime("%Y-%m-%dT%H:%M:%SZ"), dt2.strftime("%Y-%m-%dT%H:%M:%SZ")
    else:
        current_time = datetime.datetime.utcnow()
        past_time = current_time - datetime.timedelta(days=int(timeframe)*30)
        return past_time.strftime("%Y-%m-%dT%H:%M:%SZ"), current_time.strftime("%Y-%m-%dT%H:%M:%SZ")