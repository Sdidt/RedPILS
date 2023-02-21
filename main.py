from reddit_retriever.crawler import Crawler
from text_process.spacy_ner import NER
from text_process.tokenizer import TFIDF_tokenizer

from utils.constants import keywords

keywords = set(keywords)
old_keywords = keywords.copy()
crawler = Crawler(output_filename="test99")
# crawler.crawl_data(1,1)

## uncomment
# crawler.keyword_crawl(keywords,3, 1)
docs = crawler.get_all_docs()
# print(docs[list(docs.keys())[0]])
print(len(docs))
ner = NER()
# keywords = set()

for comment in docs.values():
    # print(comment)
    new_keywords = ner.get_useful_keywords(comment)
    keywords = keywords.union(new_keywords)
    # print("Keywords: {}".format(new_keywords))

# print("ALL Keywords: {}".format(keywords))

tokenizer = TFIDF_tokenizer(docs, search_space=keywords.difference(old_keywords))
tf_idf_score_dict, tf_score_dict, idf_score_dict = tokenizer.get_tf_idf_score()
print(dict(sorted(tf_idf_score_dict.items(), key = lambda x: x[1], reverse=True)))

result = tokenizer.get_top_n(tf_idf_score_dict,5)

print("5 most important keywords: ")
for keyword in result:
    print(keyword)

crawler.keyword_crawl(result, 3, 1)
