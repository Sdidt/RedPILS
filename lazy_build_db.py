from utils.constants import keywords, solr_var
from utils.helpers import *
from reddit_retriever.solr_interface import solr_ingest

import pandas as pd

def read_preds():
    df = pd.read_csv('full_6k_preds.csv', header=0)
    labels = df.applymap(str).groupby('comment_id')["predicted_label"].apply(float).to_dict()
    scores = df.applymap(str).groupby('comment_id')["predicted_score"].apply(float).to_dict()
    # print(labels)
    # print(scores)
    print(len(labels))
    print(len(scores))
    return labels, scores

def retain_all_except_id_version(list_data, labels, scores, mode="data"):
    results = []
    if mode == "data":
        for doc in list_data:
            if doc["comment_id"] in labels:
                results.append(
                    {
                        k: v for k, v in doc.items() if k not in ["id", "_version_"]
                    } | {
                        "polarity": scores[doc["comment_id"]],
                        "political_leaning": labels[doc["comment_id"]]
                    })
            else:
                results.append(
                    {
                        k: v for k, v in doc.items() if k not in ["id", "_version_"]
                    } | {
                        "polarity": 0.0,
                        "political_leaning": 0.0
                    })
    else:
        results = [
            {
                k: v for k, v in doc.items() if k not in ["id", "_version_"]
            }
            for doc in list_data
        ]
    return results

labels, scores = read_preds()

#--------------------solr init - comments data--------------------#
data_ingest = solr_ingest(solr_var["solr_url"],solr_var['data_collection_name'],solr_var['headers'])
# data_ingest.upload_configset(solr_var["configset_zip_path"], solr_var["configset_name"], "true")
# data_ingest.define_schema(solr_var['data_collection_name'], solr_var['data_schema'])
data_ingest.delete_collection(solr_var['data_collection_name'])
data_ingest.create_collection(solr_var['data_collection_name'], solr_var['data_schema'], solr_var['data_unique_key'], solr_var['filtered_text_type'])
# data_ingest.replace_schema(solr_var['data_collection_name'], solr_var['data_schema'])
data_ingest.delete_data(solr_var['data_collection_name'])
data = read_json("crawled_corpus")
data = retain_all_except_id_version(data, labels, scores)
# print(data[0])
data_ingest.push_data(solr_var["data_collection_name"], data)
# #-------------------------------------------------#


keyword_ingest = solr_ingest(solr_var["solr_url"],solr_var['keyword_collection_name'],solr_var['headers'])
keyword_ingest.delete_collection(solr_var['keyword_collection_name'])
keyword_ingest.create_collection(solr_var['keyword_collection_name'],solr_var['keyword_schema'],solr_var['keyword_unique_key'])
keyword_ingest.delete_data(solr_var['keyword_collection_name'])
keywords = read_json("keywords")
keywords = retain_all_except_id_version(keywords, labels, scores, mode="keyword")
keyword_ingest.push_data(solr_var['keyword_collection_name'], keywords)
# #-------------------------------------------------#
