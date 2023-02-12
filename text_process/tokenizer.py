import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize 
from nltk import tokenize
from operator import itemgetter
import math
stop_words = set(stopwords.words('english'))

class TFIDF_tokenizer():
    def __init__(self,doc) -> None:
        self.doc = doc
        self.total_word_length = 0
        self.total_words = 0
        self.total_sentences = 0
        self.total_sent_len = 0
        self.tf_score = {}
        self.idf_score = {}
        self.tf_idf_score = {}

    def get_words(self):
        self.total_words = self.doc.split()
        self.total_word_length = len(self.total_words)
        return self.total_word_length
    
    def tokenize_sent(self):
        self.total_sentences = tokenize.sent_tokenize(self.doc)
        self.total_sent_len = len(self.total_sentences)
        return self.total_sent_len

    def check_sent(self, word, sentences): 
        final = [all([w in x for w in word]) for x in sentences] 
        sent_len = [sentences[i] for i in range(0, len(final)) if final[i]]
        return int(len(sent_len))
    
    def get_tf_score(self):
        for each_word in self.total_words:
            each_word = each_word.replace('.','')
            if each_word not in stop_words:
                if each_word in self.tf_score:
                    self.tf_score[each_word] += 1
                else:
                    self.tf_score[each_word] = 1

        # Dividing by total_word_length for each dictionary element
        self.tf_score.update((x, y/int(self.total_word_length)) for x, y in self.tf_score.items())
        return self.tf_score

    def get_idf_score(self):
        self.idf_score = {}
        for each_word in self.total_words:
            each_word = each_word.replace('.','')
            if each_word not in stop_words:
                if each_word in self.idf_score:
                    self.idf_score[each_word] = self.check_sent(each_word, self.total_sentences)
                else:
                    self.idf_score[each_word] = 1

        # Performing a log and divide
        self.idf_score.update((x, math.log(int(self.total_sent_len)/y)) for x, y in self.idf_score.items())

        return self.idf_score

    def get_tf_idf_score(self):

        # process text
        word_len = self.get_words()
        sent_len = self.tokenize_sent()

        # create tf_score dict
        tf_score_dict = self.get_tf_score()

        # create idf_score_dict
        idf_score_dict = self.get_idf_score()

        self.tf_idf_score = {key: self.tf_score[key] * self.idf_score.get(key, 0) for key in self.tf_score.keys()}
        return self.tf_idf_score

    def get_top_n(self, dict_elem, n):
        result = dict(sorted(dict_elem.items(), key = itemgetter(1), reverse = True)[:n]) 
        return result

if __name__ == '__main__':
    doc = """I am a graduate. I want to learn Python. 
        I like learning Python. Python is easy. Python is interesting. 
        Learning increases thinking. Everyone should invest time in learning"""

    tokenizer = TFIDF_tokenizer(doc)
    tf_idf_score_dict = tokenizer.get_tf_idf_score()
    result = tokenizer.get_top_n(tf_idf_score_dict,10)
    print(result)