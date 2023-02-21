from reddit_retriever.crawler import Crawler
from text_process.spacy_ner import NER
from text_process.tokenizer import TFIDF_tokenizer
from text_process.translitlator import Translitlator

from utils.constants import keywords

keywords = set(keywords)
old_keywords = keywords.copy()
crawler = Crawler(output_filename="test99")
# Uncomment below to test
# crawler.keyword_crawl(keywords, 2, 1)
docs = crawler.get_all_docs()
print(len(docs))
ner = NER()
# Uncomment to test translation; will not work at our scale since API request limit is hit
# translitlator = Translitlator()
# docs = translitlator.translate(list(docs.values()))

for comment in docs.values():
    # print(comment)
    
    new_keywords = ner.get_useful_keywords(comment)
    keywords = keywords.union(new_keywords)
    # print("Keywords: {}".format(new_keywords))

# print("ALL Keywords: {}".format(keywords))

tokenizer = TFIDF_tokenizer(docs, search_space=keywords.difference(old_keywords))
tf_idf_score_dict, tf_score_dict, idf_score_dict = tokenizer.get_tf_idf_score()


result = tokenizer.get_top_n(tf_idf_score_dict,5)
print(old_keywords)

print("5 most important keywords: ")
for keyword, score in result.items():
    print("{}: {}".format(keyword, score))

# Uncomment below to test dynamic crawling
# crawler.keyword_crawl(result, 2, 1)
