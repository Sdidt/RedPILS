from reddit_retriever.crawler import Crawler
from text_process.spacy_ner import NER
from text_process.tokenizer import TFIDF_tokenizer
from text_process.translitlator import Translitlator

from utils.constants import keywords, solr_var
from reddit_retriever.solr_interface import solr_ingest


#--------------------solr init--------------------#
data_ingest = solr_ingest(solr_var["solr_url"],solr_var['collection_name'],solr_var['headers'])
data_ingest.delete_collection(solr_var['collection_name'])
data_ingest.create_collection(solr_var['collection_name'],solr_var['schema'])
data_ingest.delete_data(solr_var['collection_name'])
#-------------------------------------------------#

#--------------------keyword extract--------------------#
keywords = set(keywords)
old_keywords = keywords.copy()
crawler = Crawler(output_filename="test100")
# Uncomment below to test
crawler.keyword_crawl(keywords, 2, 1, data_ingest)
search_data = data_ingest.query_data(solr_var['params'],solr_var['collection_name'])
print(search_data)
# docs = crawler.get_all_docs()
# print(len(docs))
# ner = NER()
# # Uncomment to test translation; will not work at our scale since API request limit is hit
# # translitlator = Translitlator()
# # docs = translitlator.translate(list(docs.values()))
# #-------------------------------------------------#

# #--------------------Keyword preprocess--------------------#
# for comment in docs.values():
#     # print(comment)
#     new_keywords = ner.get_useful_keywords(comment)
#     keywords = keywords.union(new_keywords)
#     # print("Keywords: {}".format(new_keywords))

# # print("ALL Keywords: {}".format(keywords))
# #-------------------------------------------------#

# #--------------------TFIDF tokenizer--------------------#
# tokenizer = TFIDF_tokenizer(docs, search_space=keywords.difference(old_keywords))
# tf_idf_score_dict, tf_score_dict, idf_score_dict = tokenizer.get_tf_idf_score()


# result = tokenizer.get_top_n(tf_idf_score_dict,5)
# print(old_keywords)

# print("5 most important keywords: ")
# for keyword, score in result.items():
#     print("{}: {}".format(keyword, score))
# #-------------------------------------------------#

# #--------------------Dynamic Crawler--------------------#
# # Uncomment below to test dynamic crawling
# # crawler.keyword_crawl(result, 2, 1)
# #-------------------------------------------------#
