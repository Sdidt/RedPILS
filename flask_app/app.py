from flask_cors import CORS
from flask import Flask, request, url_for, jsonify
from dotenv import load_dotenv
import os
import sys
import json

load_dotenv()
sys.path.append(os.environ.get("SYS_PATH"))

from reddit_retriever.solr_interface import solr_ingest
from utils.constants import solr_var

app = Flask(__name__)
CORS(app)
cors = CORS(app, resources={r"/*": {"origins":"*"}})


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

@app.route('/query', methods=["POST"])
def query():
    args = request.args
    query = args.get("query")
    if request.method=='POST':
        body = request.json
        data_ingest = solr_ingest(solr_var["solr_url"],solr_var['data_collection_name'],solr_var['headers'])
        search_results = data_ingest.phrase_query(solr_var['data_collection_name'], body["query"], 5, 10, 20, 40, 10)
        search_results = [{
            "score": doc["score"],
            "comment": doc["comment"],
            "url": "https://www.reddit.com" + doc["url"]
        } for doc in search_results]
        [print("Score: {}\nComment: {}\nURL: {}".format(doc["score"], doc["comment"], doc["url"])) for doc in search_results]
        response = jsonify({"query":query, "topk":search_results})
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response

if __name__ == "__main__":
   app.run(debug=True)