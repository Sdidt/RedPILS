from elt import translit
from googletrans import Translator

# hindi_text = translit("hindi")
# translator = Translator()
# with open("hindi_text.txt", "a", encoding="utf-8") as f:
#     res = hindi_text.convert(["Me gyan chod raha hu? Lmao. Tune khud bola ki kuch logo ke basis par judge nahi kar sakte. Phir tu khud judge kar raha. Jab maine yahi cheez boli to tujhe lag raha ki me gyan chod raha hu? Kamal karte ho bhai", "Bosdk dang se pada kar tere jaisa internet se nai padai ki mere actual sc /st dost hai i live in a small town which is not that developed but not that backward either tere jaisa ghar me nai baitha rehta hun bhar ja k actual reality ko experience karta hun chutiya"])
#     for r in res:
#         print(r, file=f)
#         print(translator.translate(r).text)


class Translitlator:
    def __init__(self) -> None:
        self.transliterator = translit("hindi")
        self.translator = Translator()
    
    def transliterate(self, texts: list[str]):
        res = self.transliterator.convert(texts)
        return res
    
    def translate(self, text: str):
        res = self.translator.translate(text)
        return res.text

if __name__ == "__main__":
    translitlator = Translitlator()
    transliterated = [
        "All I'm talking about is an app translation, usme tujhe kyu itni khujli ho rahi hai?",
        "Usko West Bihar bana denge 😂",
        "Duniya bhar mein inka chatt te ho",
        "bihar se Gautam Bauddh aye, unka gaurva is prithvi ko darshana hai. ",
        "Aur bauddha apna hi ek panth hai."
    ]
    # print(transliterated)
    translated = []
    for text in transliterated:
        translated.append(translitlator.translate(text))
    print(translated)


