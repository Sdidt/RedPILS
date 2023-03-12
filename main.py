
from text_process.spacy_ner import NER
from text_process.tokenizer import TFIDF_tokenizer
from text_process.translitlator import Translitlator

from utils.constants import keywords, solr_var
from utils.helpers import *
from reddit_retriever.solr_interface import solr_ingest
from reddit_retriever.crawler import Crawler


#--------------------solr init - comments data--------------------#
data_ingest = solr_ingest(solr_var["solr_url"],solr_var['data_collection_name'],solr_var['headers'])
data_ingest.delete_collection(solr_var['data_collection_name'])
data_ingest.create_collection(solr_var['data_collection_name'],solr_var['data_schema'],solr_var['data_unique_key'])
data_ingest.delete_data(solr_var['data_collection_name'])
#-------------------------------------------------#

#--------------------solr init - keywords data--------------------#
latest_level = 0
keywords = {latest_level: set(keywords)}
all_keywords = set(keywords[latest_level])
crawler = Crawler(output_filename="solr_integration_test")
# Uncomment below to test
crawler.keyword_crawl(keywords[latest_level], 1, 1, data_ingest)
keywords_dict = []
for key in keywords[latest_level]:
    keywords_dict.append({'keyword':key})

keyword_ingest = solr_ingest(solr_var["solr_url"],solr_var['keyword_collection_name'],solr_var['headers'])
keyword_ingest.delete_collection(solr_var['keyword_collection_name'])
keyword_ingest.create_collection(solr_var['keyword_collection_name'],solr_var['keyword_schema'],solr_var['keyword_unique_key'])
keyword_ingest.delete_data(solr_var['keyword_collection_name'])
keyword_ingest.push_data(solr_var['keyword_collection_name'],keywords_dict)
# #-------------------------------------------------#

# #--------------------keyword extract--------------------#
crawler = Crawler(output_filename="solr_integration_test")
# # Uncomment below to test
crawler.keyword_crawl(keywords[latest_level], 5, 1, data_ingest)
# get all documents stored in solr database
# search_data = data_ingest.query_data(solr_var['params'],solr_var['data_collection_name'])
search_data = data_ingest.query_data({'q':'*:*','rows':1000000},solr_var['data_collection_name'])
# store_json(search_data,'search_data')
docs = crawler.get_all_docs()
print(len(docs))
ner = NER()
# # Uncomment to test translation; will not work at our scale since API request limit is hit
# # translitlator = Translitlator()
# # docs = translitlator.translate(list(docs.values()))
# #-------------------------------------------------#

# #--------------------Keyword preprocess--------------------#
latest_level += 1
keywords[latest_level] = set()
for comment in docs.values():
    # print(comment)
    new_keywords = ner.get_useful_keywords(comment)
    keywords[latest_level] = keywords[latest_level].union(new_keywords)
    # print("Keywords: {}".format(new_keywords))

print("ALL Keywords: {}".format(keywords))
# #-------------------------------------------------#

# #--------------------TFIDF tokenizer--------------------#
tokenizer = TFIDF_tokenizer(docs, search_space=keywords[latest_level])
tf_idf_score_dict, tf_score_dict, idf_score_dict = tokenizer.get_tf_idf_score()


result = tokenizer.get_top_n(tf_idf_score_dict, 2, all_keywords)

print("2 most important keywords: ")
for keyword, score in result.items():
    print("{}: {}".format(keyword, score))
    if({'keyword':keyword} not in keywords_dict):
        keywords_dict.append({'keyword':keyword})
store_json(keywords_dict,"keywords_data")
keyword_ingest.push_data(solr_var['keyword_collection_name'],keywords_dict)
# #-------------------------------------------------#

# #--------------------Dynamic Crawler--------------------#
# # Uncomment below to test dynamic crawling
crawler.keyword_crawl(result, 5, 1, data_ingest)
# #-------------------------------------------------#
