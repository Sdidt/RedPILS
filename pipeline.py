from text_process.spacy_ner import NER
from text_process.tokenizer import TFIDF_tokenizer
from text_process.translitlator import Translitlator
from utils.constants import keywords
from reddit_retriever.crawler import Crawler


class Pipeline:
    def __init__(self, output_filename, keyword_limit, submission_limit, keywords: set) -> None:
        self.crawler = Crawler(output_filename)
        self.NER = NER()
        self.TFIDF = TFIDF_tokenizer()
        self.translator = Translitlator()
        self.latest_level = 0
        self.keywords = {self.latest_level: set(keywords)}
        self.all_keywords = set(keywords)
        self.keyword_limit = keyword_limit
        self.submission_limit = submission_limit
    
    def crawl(self):
        # expansive crawl function; it uses the latest extracted keywords to crawl more data
        self.crawler.keyword_crawl(self.keywords[self.latest_level], self.keyword_limit, self.submission_limit)

    def get_imp_keywords(self, n):
        print(self.keywords)
        docs = self.crawler.get_all_docs()
        self.latest_level += 1
        self.keywords[self.latest_level] = set()
        for comment in docs.values():
            new_keywords = self.NER.get_useful_keywords(comment)
            self.keywords[self.latest_level] = self.keywords[self.latest_level].union(new_keywords)
        self.TFIDF.ingest(docs, search_space=self.keywords[self.latest_level])
        tf_idf_score_dict, tf_score_dict, idf_score_dict = self.TFIDF.get_tf_idf_score()
        print(tf_idf_score_dict)
        result = set((self.TFIDF.get_top_n(tf_idf_score_dict, n, self.all_keywords)).keys())
        self.keywords[self.latest_level] = result
        self.all_keywords = self.all_keywords.union(result)

if __name__ == "__main__":
    output_filename = "test7"
    keyword_limit = 1
    submission_limit = 1
    pipeline = Pipeline(output_filename, keyword_limit, submission_limit, keywords)
    num_imp_keys = 2
    while sum(len(val) for val in pipeline.keywords.values()) < 10:
        pipeline.get_imp_keywords(num_imp_keys)
        pipeline.crawl()
