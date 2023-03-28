from text_process.spacy_ner import NER
from text_process.tokenizer import TFIDF_tokenizer
from text_process.translitlator import Translitlator

from utils.constants import keywords, solr_var
from utils.helpers import *
from reddit_retriever.solr_interface import solr_ingest
from reddit_retriever.crawler import Crawler

from operator import itemgetter


def get_top_n(dict_elem, n, existing_keywords) -> dict:
    sorted_dict = dict(sorted(dict_elem.items(), key = itemgetter(1), reverse = True)) 
    result = {}
    counter = 0
    for k, v in sorted_dict.items():
        # avoid duplicate keywords
        if k not in existing_keywords:
            result[k] = v
            counter += 1
            if counter == n:
                break
    return result

#--------------------solr init - comments data--------------------#
# data_ingest = solr_ingest(solr_var["solr_url"],solr_var['data_collection_name'],solr_var['headers'])
# data_ingest.define_schema(solr_var['data_collection_name'], solr_var['data_schema'])
# data_ingest.delete_collection(solr_var['data_collection_name'])
# data_ingest.create_collection(solr_var['data_collection_name'], solr_var['data_schema'], solr_var['data_unique_key'], solr_var['filtered_text_type'])
# data_ingest.delete_data(solr_var['data_collection_name'])
#-------------------------------------------------#

#--------------------solr init - keywords data--------------------#
# latest_level = 0
# keywords = {latest_level: set([keyword.lower() for keyword in keywords])}
# all_keywords = set(keywords[latest_level])
# crawler = Crawler(output_filename="solr_integration_test")
# # Uncomment below to test
# crawler.keyword_crawl(keywords[latest_level], 30, 1, data_ingest)
# keywords_dict = []
# for key in keywords[latest_level]:
#     keywords_dict.append({'keyword':key})

keyword_ingest = solr_ingest(solr_var["solr_url"],solr_var['keyword_collection_name'],solr_var['headers'])
keyword_data = keyword_ingest.query_data({'q':'*:*','rows':1000000},solr_var['keyword_collection_name'])
store_json(keyword_data, "keywords")
# keyword_ingest.delete_collection(solr_var['keyword_collection_name'])
# keyword_ingest.create_collection(solr_var['keyword_collection_name'],solr_var['keyword_schema'],solr_var['keyword_unique_key'], solr_var['filtered_text_type'])
# keyword_ingest.delete_data(solr_var['keyword_collection_name'])
# keyword_ingest.push_data(solr_var['keyword_collection_name'],keywords_dict)
# #-------------------------------------------------#

#--------------------keyword extract--------------------#
# crawler = Crawler(output_filename="solr_integration_test")
# search_data = data_ingest.query_data({'q':'*:*','rows':1000000},solr_var['data_collection_name'])
# store_json(search_data, "backup_before_reindex")
# ner = NER()

#--------------------Translation--------------------#
# Uncomment to test translation; will not work at our scale since API request limit is hit
# translitlator = Translitlator()
# docs = translitlator.translate(list(docs.values()))
#-------------------------------------------------#

# looks like tagger may not be very useful for NER
#--------------------Tagger Setup--------------------#
# data_ingest.add_new_field_type(solr_var["data_collection_name"], solr_var["tag_field_type"])
# data_ingest.add_new_field_type(solr_var["data_collection_name"], solr_var["filtered_text_type"])
# data_ingest.update_existing_field_type(solr_var["data_collection_name"], solr_var["filtered_text_type"])
# data_ingest.define_schema(solr_var["data_collection_name"], solr_var["tag_field"])
# data_ingest.add_new_copy_field(solr_var["data_collection_name"], solr_var["copy_tag_field"])
# data_ingest.add_new_request_handler(solr_var["data_collection_name"], solr_var["tag_request_handler"])



#--------------------Keyword preprocess--------------------#
# latest_level += 1
# keywords[latest_level] = set()
# for comment in search_data:
#     # print(comment)
#     new_keywords = ner.get_useful_keywords(comment["comment"])
#     keywords[latest_level] = keywords[latest_level].union(new_keywords)
#     print("Keywords: {}".format(new_keywords))

# print("ALL Keywords: {}".format(keywords))
#-------------------------------------------------#

#--------------------TFIDF tokenizer--------------------#
# tokenizer = TFIDF_tokenizer(docs, search_space=keywords[latest_level])
# tf_idf_score_dict, tf_score_dict, idf_score_dict = tokenizer.get_tf_idf_score()
# tf_idf_score_dict = {}
# for keyword in keywords[latest_level]:
#     tf_idf_score_dict[keyword] = data_ingest.compute_avg_tf_idf(keyword, solr_var["data_collection_name"])

# num_keywords = 5
# result = get_top_n(tf_idf_score_dict, num_keywords, all_keywords)

# keywords_dict = []
# print(f"{num_keywords} most important keywords: ")
# for keyword, score in result.items():
#     print("{}: {}".format(keyword, score))
#     if({'keyword':keyword} not in keywords_dict):
#         keywords_dict.append({'keyword':keyword})
# store_json(keywords_dict,"keywords_data")
# keyword_ingest.push_data(solr_var['keyword_collection_name'],keywords_dict)
#-------------------------------------------------#

#--------------------Dynamic Crawler--------------------#
# Uncomment below to test dynamic crawling
# crawler.keyword_crawl(list(result.keys()), 50, 1, data_ingest)
#-------------------------------------------------#
