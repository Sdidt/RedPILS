from dotenv import load_dotenv
import os
import sys
import json
import re
import datetime
import random
import wordcloud
import matplotlib.pyplot as plt

import pandas as pd
import plotly.express as px

load_dotenv()
print(os.environ.get("SYS_PATH"))
sys.path.append(os.environ.get("SYS_PATH"))

from reddit_retriever.solr_interface import solr_ingest
from utils.constants import solr_var

def load_stopwords():
    with open('stopwords_nltk.txt','r') as st:
        st_content = st.read()
        stopwords = set(st_content.split())
        print(len(stopwords))
    return(stopwords)

def process_query(query):
    operators = [" AND ", " OR ", " NOT "]
    words=query.split()
    
    print(query)
    processed_query=query
    for op in operators:
        regex_pattern = re.compile(re.escape(op), re.IGNORECASE)
        processed_query = regex_pattern.sub(op, processed_query)
    for word in words:
        if word.upper() not in ["AND", "OR", "NOT", ")", "(", "~", "*"] and len(word)>=7 and '~' not in word:
            processed_query= processed_query.replace(word, word+"~3")
        elif word.upper() not in ["AND", "OR", "NOT", ")", "(", "~", "*"] and len(word)>=5 and '~' not in word:
            processed_query= processed_query.replace(word, word+"~2")
        
    return processed_query
    
def search_db(query, K=10, d1="*", d2="*", intitle=False):
    intitle = intitle == "true"
    data_ingest = solr_ingest(solr_var["solr_url"],solr_var['data_collection_name'],solr_var['headers'])
    time_elapsed, search_results = data_ingest.phrase_query(solr_var['data_collection_name'], query, 5, 10, 20, 40, d1, d2, intitle,K)
    num_results=len(search_results)
    
    search_results = [{
        "score": doc["score"],
        "comment": doc["comment"],
        "reddit_score": doc["reddit_score"],
        "url": "https://www.reddit.com" + doc["url"],
        #replace labels and scores with actual labels and scores
        "political_leaning": doc["political_leaning"],
        "polarity_score": doc["polarity"]
    } for doc in search_results]
    
    # [print("Score: {}\nComment: {}\nURL: {}".format(doc["score"], doc["comment"], doc["url"])) for doc in search_results]
    return time_elapsed, num_results, search_results

def polarity_filter_results(search_results, polarity):
    if polarity.lower()=="all":
        return search_results
    
    filtered_results=[]
    if polarity.lower()=="left":
        polarity_key=-1
    elif polarity.lower()=="right":
        polarity_key=1
    else:
        polarity_key=0
    if len(search_results)!=0:
        for item in search_results:
            if item["political_leaning"]==polarity_key:
                filtered_results.append(item)
    return filtered_results
    

def avg_scores(search_results):
    reddit_avg=0
    score_avg=0
    polarity_avg=0
    if len(search_results)!=0:
        for item in search_results:
            print(item)
            reddit_avg+=item["reddit_score"]
            score_avg+=item["score"]
            polarity_avg+=item["political_leaning"]
        reddit_avg/=len(search_results)
        score_avg/=len(search_results)
        polarity_avg/=len(search_results)
        
    return reddit_avg, score_avg, polarity_avg

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
    
def generate_wordclouds(search_results):
    # comments=[]
    if len(search_results)!=0:
        text = ' '.join(item['comment'] for item in search_results)
        # for item in search_results:
        #     comments.append(item['comment'])
    
    # text = ' '.join(comments)
    stopwords = load_stopwords()
    # background_color='lightgrey',
    fig_wordcloud = wordcloud.WordCloud(stopwords=stopwords,
                    colormap='RdBu', width=800, height=600, collocations=False).generate(text)
    
    return fig_wordcloud
    
    # plt.figure(figsize=(10,7), frameon=True)
    # plt.imshow(fig_wordcloud)  
    # plt.axis('off')
    # plt.title(title, fontsize=20 )
    # plt.show()

def generate_geo_df():
    map_df=pd.read_csv('flask_app/outputs/map_data.csv')
    for i,term in enumerate(map_df["state"]):
        term=term.replace("&", "")
        term=term.replace(" Pradesh", "")
        term=process_query(term)
        # term.replace("Uttar Pradesh", "UP")
        time_elapsed, num_results, search_results=search_db(term)
        
        print(term, num_results)
        reddit_avg, score_avg, polarity_avg= avg_scores(search_results)
        map_df.loc[i, 'num_results'] = num_results
        map_df.loc[i, 'reddit_score'] = reddit_avg
        map_df.loc[i, 'polarity'] = polarity_avg
        map_df.loc[i, 'score'] =score_avg
        
    map_df.to_csv("flask_app/outputs/map_data.csv", index=False)   
    print(map_df)
    
def generate_time_df(query="*"):
    time_df=pd.read_csv('flask_app/outputs/time_data.csv')
    print(time_df)
    for i in range(len(time_df)):
        term=process_query(query)
        d1, d2=process_date(None, str(time_df['sd'][i]), str(time_df['ed'][i]))
        time_elapsed, num_results, search_results=search_db(term, d1=d1, d2=d2)
        
        print(term, num_results)
        reddit_avg, score_avg, polarity_avg= avg_scores(search_results)
        time_df.loc[i, 'num_results'] = num_results
        time_df.loc[i, 'reddit_score'] = reddit_avg
        time_df.loc[i, 'polarity'] = polarity_avg
    if query=="*":
        query="all"
    time_df.to_csv("flask_app/outputs/time_data_"+query+".csv", index=False)   
    # print(time_df)
    return(time_df)
    

def generate_geoplot(key="num_results", colormap="Reds"):
    map_df=pd.read_csv('flask_app/outputs/map_data.csv')
    with open("flask_app/outputs/india_states.geojson") as f:
        states = json.load(f)
    if key=="reddit_score" or key=="polarity":
        mid=0
        colormap="RdBu_r"
    else:
        mid=None
    
    
    fig = px.choropleth_mapbox(
    map_df,
    geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
    featureidkey='properties.ST_NM',
    locations='state',
    color=key,
    mapbox_style = 'carto-positron',
    opacity=0.85,
    center = dict(lat=22.5, lon=80),
    zoom=3.6,
    color_continuous_midpoint=mid,
    hover_data=["num_results","reddit_score", "score",  "polarity"],
    template="plotly_dark",
    color_continuous_scale=colormap
    )
    
    # fig.update_geos(fitbounds="locations", visible=False)
    # fig.update_layout(width=1000, height=1000, autosize=False, margin=dict(
    #             l=0,
    #             r=0,
    #             b=0,
    #             t=0,
    #             pad=0,
    #             autoexpand=True
    #         ))
    fig.show()
    return fig