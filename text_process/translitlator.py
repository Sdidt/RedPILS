from __future__ import annotations  # required for older python versions before 3.9
from elt import translit
from googletrans import Translator
from nltk import tokenize
import time 


class Translitlator:
    def __init__(self) -> None:
        self.transliterator = translit("hindi")
        self.translator = Translator()
    
    def split_sent(self,text) -> list[str]:
        sentences = tokenize.sent_tokenize(text)
        print(sentences)
        return sentences

    def transliterate(self, texts: list[str]):
        res = self.transliterator.convert(texts)
        return res
    
    def translate(self, texts: str):
        # infeasible cuz of rate limits
        res = []
        for text in texts:
            # print(text)
            split_sent = []
            sents = self.split_sent(text)
            for sent in sents:
                try:
                    sent_trans = self.translator.translate(sent).text
                except AttributeError:
                    print("Overloaded requests; sleeping for 5 seconds")
                    time.sleep(5)
                split_sent.append(sent_trans)
                # print(sent_trans)
            res.append(" ".join(split_sent))
        return res

if __name__ == "__main__":
    translitlator = Translitlator()
    texts = [
        "All I'm talking about is an app translation, usme tujhe kyu itni khujli ho rahi hai? Usko West Bihar bana denge 😂 Duniya bhar mein inka chatt te ho bihar se Gautam Bauddh aye, unka gaurva is prithvi ko darshana hai. Aur bauddha apna hi ek panth hai.",
        'Kejriji is saying " Aap ka paisa aap ko hi free dene mein use kar rahe hai toh kya galat hai"? but never say about the direct tax payers involved in the economy, though indrect tax payers are every 1 but these free sceheme are mostly targeted towards illegal migrants and lower class who actually venture out to vote. '
    ]
    # print(transliterated)
    translated = translitlator.translate(texts)
    print(translated)


