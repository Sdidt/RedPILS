from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk import tokenize
from operator import itemgetter
import math
stop_words = set(stopwords.words('english'))

class TFIDF_tokenizer():
    def __init__(self,docs) -> None:
        self.docs = docs
        self.total_docs_len = len(self.docs)
        self.total_word_length = 0
        self.total_words = []
        self.total_sentences = 0
        self.total_sent_len = 0
        self.tf_score = {}
        self.idf_score = {}
        self.tf_idf_score = {}
        self.lemmatizer = WordNetLemmatizer()

    def get_words(self):
        for doc in self.docs.values():
            self.total_words.extend(doc.split())
        self.total_word_length = len(self.total_words)
        return self.total_word_length
    
    def tokenize_sent(self):
        self.total_sentences = tokenize.sent_tokenize(self.docs)
        self.total_sent_len = len(self.total_sentences)
        return self.total_sent_len

    def check_sent(self, word, sentences): 
        final = [all([w in x for w in word]) for x in sentences] 
        sent_len = [sentences[i] for i in range(0, len(final)) if final[i]]
        return int(len(sent_len))
    
    def check_doc(self, word, doc_words):
        final = [all([w in x for w in word]) for x in doc_words]
        doc_len = [doc_words[i] for i in range(0, len(final)) if final[i]]
        return int(len(doc_len))

    def lemmatize_word(self, word):
        return self.lemmatizer.lemmatize(word)

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
                    self.idf_score[each_word] = self.check_doc(each_word, list(self.docs.values()))
                else:
                    self.idf_score[each_word] = 1

        # Performing a log and divide
        self.idf_score.update((x, math.log(int(self.total_docs_len)/y)) for x, y in self.idf_score.items())

        return self.idf_score

    def get_tf_idf_score(self):

        # process text
        word_len = self.get_words()
        # sent_len = self.tokenize_sent()

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
    doc = {
        "doc1": """Hindu supremacy is the talibanisation of India.""",
        "doc2": """People don't have their priorities right, our priority should be to get rid of BJP from power. But what our people are focusing on is 'if not Modi then who', Modi is a fucking clown, anyone is better than MODI. But don't vote for anyone vote for the party that's has the best chance to defeat BJP.\n\nIt's common sense.""",
        "doc3": """
        > the dogma itself matters a huge deal. \n\nSure, if one is doing a granular, discrete level of analysis. Which is not what my comment was about or even what this post's insinuation is.\n\nIn meta, general, normalized terms ALL Dogma is regressive, without exception. It is not irrelevant that 1 approach wastes more generations sure but compared to approaches which don't waste any or near to that it isn't much.\n\n> And nobody talks about spectrums\n\nWhen one is already Inside a spectrum and as you say *Simplify* (which is what above mentioned granular research would be about) then it's not necessary to invoke Spectrums or Gradients sure.\n\nBut that is not what my comment and this topic was about. \n\nIf entire world was on the same Dogma fix then it would be applicable to not even mention this since everyone is on the same boat.  \nBut the entire world is NOT on the same exact Dogma. There are different Dogma's, All regressive, all with different decay curves/half-lives. \n\n> The ethnically monolithic, clan-based, Sunni Pushtun Taliban are not to be compared with Hindu Nationalism in India in any credible way. It's a complete mischaracterization of the economic, linguistic, ethnic, and inter-religious, and historic issues we face, that have led to our current predicament.\n\nThis is that different topic to my comment's intentions. Though interestingly even this can be sort of squared in a way.  \nWe know there isn't a place on this planet which had a more powerful endogamic dynamic than South Asia. \nWe have both cultural and most critically genetic evidence to back this. \n\nVarious Caste and clan networks in India makes anything the Afghans came up with as juvenile play.\n\nThen there is Scale, which most western social sciences model just can not adjust to because they had no reference to even comprehend it.\n\nTo me India is in the midst of having multiple different Dogmas (of severity which are in net terms indeed near in place inside that Spectrum space to whatever the Talibanisation is).   \n\nOne of them is this Hindutva, Hindu Nationalization, Hindu Supremacy, whatever term one wants to use.  \n\nAnother is one India shares with large part of the world and that is this Dogma of Governance System supremacy.\n\nThese are Dogma which are State and society ending level. Just because their execution timeframe is a century longer is hardly relevant when the level of destruction is of that sort of scale.
        """
    }

    tokenizer = TFIDF_tokenizer(doc)
    tf_idf_score_dict = tokenizer.get_tf_idf_score()
    result = tokenizer.get_top_n(tf_idf_score_dict,20)
    print(result)