from reddit_retriever.crawler import Crawler
from text_process.spacy_ner import NER
from text_process.tokenizer import TFIDF_tokenizer

crawler = Crawler(output_filename="dynamic_test")
crawler.crawl_data()
docs = crawler.get_all_docs()
# print(docs)
ner = NER()
keywords = set()

for comment in docs.values():
    # print(comment)
    new_keywords = ner.get_useful_keywords(comment)
    keywords = keywords.union(new_keywords)
    print("Keywords: {}".format(new_keywords))

print("ALL Keywords: {}".format(keywords))

tokenizer = TFIDF_tokenizer(docs, search_space=keywords)
tf_idf_score_dict = tokenizer.get_tf_idf_score()
result = tokenizer.get_top_n(tf_idf_score_dict,20)

print("20 most important keywords: ")
for keyword in result:
    print(keyword)

crawler.keyword_crawl(keywords)
