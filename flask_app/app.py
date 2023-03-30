from flask_cors import CORS
from flask import Flask, request, url_for, jsonify
from dotenv import load_dotenv
import os
import sys
import json
import re

load_dotenv()
print(os.environ.get("SYS_PATH"))
sys.path.append(os.environ.get("SYS_PATH"))

from reddit_retriever.solr_interface import solr_ingest
from utils.constants import solr_var

app = Flask(__name__)
CORS(app)
cors = CORS(app, resources={r"/*": {"origins":["*","http://localhost:8000"]}})

#---------------------------------------------- TEST -------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/')
def hello():
    return "Hello World! This is a test app"

top_kr=[{'comment': "Rahul Gandhi can never be Savarkar", 'url': "https://example.com"}, {'comment': "Pappu is UNFORTUNATELY an MP", 'url': "https://example.com"}, {'comment': "Congress should get rid of Gandhis", 'url': "https://example.com"}, {'comment': "Democracy is not a family Business", 'url': "https://example.com"}, {'comment': "Pappu becomes a joke again", 'url': "https://example.com"}]
top_kl=[{'comment': "Death of Democracy", 'url': "https://example.com"}, {'comment': "BJP silencing critics. bad sign for democracy", 'url': "https://example.com"}, {'comment': "Rahul arrest is dirty hindutwa politics", 'url': "https://example.com"}, {'comment': "Modi diverting attention from Adani Scam", 'url': "https://example.com"}, {'comment': "Rahul arrest will backfire on Modi", 'url': "https://example.com"}]

@app.route('/dummy_chart', methods=["GET"])
def dummy():
    args = request.args
    query = args.get("query")
    if request.method=='GET':
        if query == "BJP" or query == "Right" or query=="Pappu":
            response =  jsonify({"query":query, "topk":top_kr})
        elif query == "Left" or query == "Rahul" or query=="Democracy":
            response = jsonify({"query":query, "topk":top_kl})
        response = jsonify({"query":query, "topk":top_kr})

        response.headers.add("Access-Control-Allow-Origin", "*")
        return response

@app.route('/dummy_charts2d', methods=["GET"])
def dummy_chart():
    """dummy api for testing charts

    Returns:
        json-four lists:  X and Y fields for numeric data. X and Y fields for categorical data. Combined both into a single call for now since its a dummy api. Will sort out the exact data once i have all real data.
    """
    args = request.args
    query = args.get("query")
    if request.method=='GET':
        response=jsonify({ "x-val-num-fieldname": [5, 10, 15, 20, 25], "y-val-num-fieldname": [50, 100, 150, 200, 250], "x-val-cat-fieldname": ["left", "left-lean", "neutral", "right-lean", "right"], "y-val-cat-fieldname": [50, 100, 150, 200, 250]})

        response.headers.add("Access-Control-Allow-Origin", "*")
        return response

#----------------------------------------------- Helpers------------------------------------------------------------------------------

def process_query(query):
    operators = [" AND ", " OR ", " NOT "]
    processed_query=query
    for op in operators:
        regex_pattern = re.compile(re.escape(op), re.IGNORECASE)
        processed_query = regex_pattern.sub(op, processed_query)
    return processed_query
    
def search_db(query, d1="*", d2="*"):
    data_ingest = solr_ingest(solr_var["solr_url"],solr_var['data_collection_name'],solr_var['headers'])
    search_results = data_ingest.phrase_query(solr_var['data_collection_name'], query, 5, 10, 20, 40, d1, d2,10)
    search_results = [{
        "score": doc["score"],
        "comment": doc["comment"],
        "reddit_score": doc["reddit_score"],
        "url": "https://www.reddit.com" + doc["url"]
    } for doc in search_results]
    # [print("Score: {}\nComment: {}\nURL: {}".format(doc["score"], doc["comment"], doc["url"])) for doc in search_results]
    return search_results

def avg_scores(search_results):
    print(search_results)
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
    return "*", "*"


#---------------------------------------------- APIs -------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/backend/click_counter', methods=["POST"])
def click_counter():
    """
    ideally pass in the comment object that has been clicked. The score will get incremented internally.
    """
    if request.method=='POST':
        body = request.json
        comment = body["comment"]
        click_score=click_score+1 
        return "click successfully updated"
    return "Error"


@app.route('/query', methods=["POST", "GET"])
def query():
    """query function
    
    input: query (str)
           timeframe - in months (int)
    

    Returns:
        json: query
              topk: top k search results in a dict (comment, url, score, reddit_score)
              avg_score: avg score for this query
              avg_reddit_score: avg_reddit score for this query        
    """
    if request.method=='POST':
        body = request.json
        query=body["query"]
        if body["timeframe"]:
            timeframe=body["timeframe"]
        else: 
            timeframe=None
    elif request.method=='GET':
        args = request.args
        query = args.get("query")
        try:
            timeframe=args.get("timeframe")
        except:
            timeframe=None
            
    
    query=process_query(query)
    d1, d2=process_date(timeframe)
    search_results=search_db(query, d1, d2)
    reddit_avg, score_avg=avg_scores(search_results)
    response = jsonify({"query":query, "topk":search_results, "avg_reddit_score":reddit_avg, "avg_score":score_avg})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

if __name__ == "__main__":
   app.run(debug=True)
   