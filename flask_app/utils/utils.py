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
        print(stopwords)
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
        if word.upper() not in ["AND", "OR", "NOT", ")", "(", "~"] and len(word)>=7 and '~' not in word:
            processed_query= processed_query.replace(word, word+"~3")
        elif word.upper() not in ["AND", "OR", "NOT", ")", "(", "~"] and len(word)>=5 and '~' not in word:
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
        #replace label with actual label
        "political_leaning": random.choice([-2, -1, 0, 1, 2])
    } for doc in search_results]
    
    # [print("Score: {}\nComment: {}\nURL: {}".format(doc["score"], doc["comment"], doc["url"])) for doc in search_results]
    return time_elapsed, num_results, search_results

def avg_scores(search_results):
    reddit_avg=0
    score_avg=0
    polarity_avg=0
    if len(search_results)!=0:
        for item in search_results:
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
    comments=[]
    if len(search_results)!=0:
        for item in search_results:
            comments.append(item['comment'])
    
    text = ' '.join(comments)
    stopwords = load_stopwords()
    fig_wordcloud = wordcloud.WordCloud(stopwords=stopwords,background_color='lightgrey',
                    colormap='viridis', width=800, height=600, collocations=False).generate(text)
    
    return fig_wordcloud
    
    # plt.figure(figsize=(10,7), frameon=True)
    # plt.imshow(fig_wordcloud)  
    # plt.axis('off')
    # plt.title(title, fontsize=20 )
    # plt.show()

def generate_df():
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
    

def generate_geoplot(key="num_results", colormap="Reds"):
    map_df=pd.read_csv('flask_app/outputs/map_data.csv')
    with open("flask_app/outputs/india_states.geojson") as f:
        states = json.load(f)
    fig = px.choropleth(
    map_df,
    geojson=states,
    featureidkey='properties.ST_NM',
    locations='state',
    color=key,
    color_continuous_scale=colormap
    )
    
    fig.update_geos(fitbounds="locations", visible=False)
    # fig.show()
    return fig