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
cors = CORS(app, resources={r"/*": {"origins":"*"}})

#---------------------------------------------- TEST -------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/')
def hello():
    return "Hello World! This is a test app"

top_kr=[{'comment': "Rahul Gandhi can never be Savarkar", 'url': "https://example.com"}, {'comment': "Pappu is UNFORTUNATELY an MP", 'url': "https://example.com"}, {'comment': "Congress should get rid of Gandhis", 'url': "https://example.com"}, {'comment': "Democracy is not a family Business", 'url': "https://example.com"}, {'comment': "Pappu becomes a joke again", 'url': "https://example.com"}]
top_kl=[{'comment': "Death of Democracy", 'url': "https://example.com"}, {'comment': "BJP silencing critics. bad sign for democracy", 'url': "https://example.com"}, {'comment': "Rahul arrest is dirty hindutwa politics", 'url': "https://example.com"}, {'comment': "Modi diverting attention from Adani Scam", 'url': "https://example.com"}, {'comment': "Rahul arrest will backfire on Modi", 'url': "https://example.com"}]



@app.route('/dummy_query', methods=["GET"])
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

#----------------------------------------------- Helpers------------------------------------------------------------------------------

def process_query(query):
    operators = [" AND ", " OR ", " NOT "]
    processed_query=query
    for op in operators:
        regex_pattern = re.compile(re.escape(op), re.IGNORECASE)
        processed_query = regex_pattern.sub(op, processed_query)
    return processed_query
    
def search_db(query):
    data_ingest = solr_ingest(solr_var["solr_url"],solr_var['data_collection_name'],solr_var['headers'])
    search_results = data_ingest.phrase_query(solr_var['data_collection_name'], query, 5, 10, 20, 40, 10)
    search_results = [{
        "score": doc["score"],
        "comment": doc["comment"],
        "url": "https://www.reddit.com" + doc["url"]
    } for doc in search_results]
    [print("Score: {}\nComment: {}\nURL: {}".format(doc["score"], doc["comment"], doc["url"])) for doc in search_results]
    return search_results
    
#---------------------------------------------- APIs -------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/query', methods=["POST", "GET"])
def query():

    if request.method=='POST':
        body = request.json
        # print(body)
        query=body["query"]
    elif request.method=='GET':
        args = request.args
        query = args.get("query")
    print(query)
    query=process_query(query)
    print(query)
    search_results=search_db(query)
    response = jsonify({"query":query, "topk":search_results})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

if __name__ == "__main__":
   app.run(debug=True)