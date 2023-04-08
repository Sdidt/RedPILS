from flask_cors import CORS
from flask import Flask, request, url_for, jsonify, send_file
from dotenv import load_dotenv
import os
import sys
import wordcloud
import matplotlib.pyplot as plt
import plotly
import plotly.express as px
import pandas as pd

load_dotenv()
print(os.environ.get("SYS_PATH"))
sys.path.append(os.environ.get("SYS_PATH"))

from flask_app.utils.utils import avg_scores, search_db, process_date, process_query, generate_wordclouds,generate_df, generate_geoplot

app = Flask(__name__)
CORS(app)
cors = CORS(app, resources={r"/*": {"origins":["*","http://localhost:8000"]}})

#---------------------------------------------- TEST -------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/')
def hello():
    # generate_df()
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

@app.route('/api/geoplot', methods=["GET"])
def map_plot():
    """
    /api/geoplot?key=num_results&colormap=Reds
    key: num_results, reddit_score, score, polarity
    colormap: Plotly color_continuous_scale field
    Returns:
        graphJSON object
    """
    if request.method=='GET':
        args = request.args
        try:
            key=args.get("key")
        except:
            key="num_results"
        try:
            colormap=args.get("colormap")
        except:
            colormap="Reds"
    fig=generate_geoplot(key=key, colormap=colormap)
    # fig.show()
    graphJSON = plotly.io.to_json(fig, pretty=True)
    return graphJSON

@app.route('/api/query_wordcloud', methods=["GET"])
def query_wordcloud():
    """Params same as query

    Returns:
        _type_: _description_
    """
    #if request is of type GET
    if request.method=='GET':
        args = request.args
        query = args.get("query")
        try:
            region=args.get("region")
        except:
            region=None
        try:
            intitle=args.get("intitle")
        except:
            intitle=False
        try:
            timeframe=args.get("timeframe")
        except:
            timeframe=None
        try:
            K=int(args.get("k"))
        except:
            K=10
        try:
            sd=args.get("from")
            ed=args.get("to")
        except:
            sd=None
            ed=None
    
    
    if region!=None and region!="":      
        query=query+" AND ( "+ region+" )"
    query=process_query(query)
    d1, d2=process_date(timeframe, sd, ed)
    print(d1, d2)
    
    time_elapsed, num_results, search_results=search_db(query, K, d1, d2, intitle)
    search_results=search_results[:K]
    fig_wordcloud=generate_wordclouds(search_results)
    plt.figure(figsize=(10,7))
    plt.imshow(fig_wordcloud)  
    plt.axis('off')
    # plt.title(title, fontsize=20 )
    plt.savefig("flask_app/outputs/query_wordcloud.png", bbox_inches='tight')
    return send_file("outputs/query_wordcloud.png")
    
    

@app.route('/query', methods=["POST", "GET"])
def query():
    """query function
    
    input: query (str)
           timeframe - in months (int)
           region - str
    

    Returns:
        json: query
              topk: top k search results in a dict (comment, url, score, reddit_score)
              avg_score: avg score for this query
              avg_reddit_score: avg_reddit score for this query        
    """
    #If Request is of type POST
    if request.method=='POST':
        body = request.json
        query=body["query"]
        if body["region"]:
            region=body["region"]
        else:
            region=None         
        if body["timeframe"]:
            timeframe=body["timeframe"]
        else: 
            timeframe=None
        if body["k"]:
            K=body["k"]
        else: 
            K=10
        if body["intitle"]:
            intitle=body["intitle"]
        else: 
            intitle=False
        if body["from"] and body["to"]:
            sd=body["from"]
            ed=body["to"]
        else: 
            sd=None
            ed=None
    
    
    #if request is of type GET
    elif request.method=='GET':
        args = request.args
        query = args.get("query")
        try:
            region=args.get("region")
        except:
            region=None
        try:
            intitle=args.get("intitle")
        except:
            intitle=False
        try:
            timeframe=args.get("timeframe")
        except:
            timeframe=None
        try:
            K=int(args.get("k"))
        except:
            K=10
        try:
            sd=args.get("from")
            ed=args.get("to")
        except:
            sd=None
            ed=None
    
    
    if region!=None and region!="":      
        query=query+" AND ( "+ region+" )"
    query=process_query(query)
    d1, d2=process_date(timeframe, sd, ed)
    print(d1, d2)
    
    time_elapsed, num_results, search_results=search_db(query, K, d1, d2, intitle)
    search_results=search_results[:K]
    reddit_avg, score_avg, polarity_avg=avg_scores(search_results)
    
    response = jsonify({"search_time":time_elapsed, "query":query, "topk":search_results, "avg_reddit_score":reddit_avg, "avg_score":score_avg, "avg_polarity":polarity_avg, "num_results":num_results})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

if __name__ == "__main__":
   app.run(debug=True)
   