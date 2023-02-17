import spacy
from spacy import displacy


class NER:
    def __init__(self) -> None:
        self.NER = spacy.load("en_core_web_sm") 

    
    def get_orgs(self, text) -> list[str]:
        text = self.NER(text)
        

if __name__ == "__main__":
    NER = spacy.load("en_core_web_sm")
    lemmatizer = NER.get_pipe("lemmatizer")
    print(lemmatizer.mode)

    # example = "> the dogma itself matters a huge deal. \n\nSure, if one is doing a granular, discrete level of analysis. Which is not what my comment was about or even what this post's insinuation is.\n\nIn meta, general, normalized terms ALL Dogma is regressive, without exception. It is not irrelevant that 1 approach wastes more generations sure but compared to approaches which don't waste any or near to that it isn't much.\n\n> And nobody talks about spectrums\n\nWhen one is already Inside a spectrum and as you say *Simplify* (which is what above mentioned granular research would be about) then it's not necessary to invoke Spectrums or Gradients sure.\n\nBut that is not what my comment and this topic was about. \n\nIf entire world was on the same Dogma fix then it would be applicable to not even mention this since everyone is on the same boat.  \nBut the entire world is NOT on the same exact Dogma. There are different Dogma's, All regressive, all with different decay curves/half-lives. \n\n> The ethnically monolithic, clan-based, Sunni Pushtun Taliban are not to be compared with Hindu Nationalism in India in any credible way. It's a complete mischaracterization of the economic, linguistic, ethnic, and inter-religious, and historic issues we face, that have led to our current predicament.\n\nThis is that different topic to my comment's intentions. Though interestingly even this can be sort of squared in a way.  \nWe know there isn't a place on this planet which had a more powerful endogamic dynamic than South Asia. \nWe have both cultural and most critically genetic evidence to back this. \n\nVarious Caste and clan networks in India makes anything the Afghans came up with as juvenile play.\n\nThen there is Scale, which most western social sciences model just can not adjust to because they had no reference to even comprehend it.\n\nTo me India is in the midst of having multiple different Dogmas (of severity which are in net terms indeed near in place inside that Spectrum space to whatever the Talibanisation is).   \n\nOne of them is this Hindutva, Hindu Nationalization, Hindu Supremacy, whatever term one wants to use.  \n\nAnother is one India shares with large part of the world and that is this Dogma of Governance System supremacy.\n\nThese are Dogma which are State and society ending level. Just because their execution timeframe is a century longer is hardly relevant when the level of destruction is of that sort of scale."
    example = "Everyone knows it already. Hindu People of Gujarat loved those riots as well. Thats why they have kept bjp in power for so many decades. Try to get close to any of ur hindu Gujarati friends, u ll see how brainwashed they all are. \n\nIt's a very tragic affair."
    example = """Tbh, this is nothing new. Whatever this documentary revealed was common acceptance in India, even in BJP, up until 2012.\n\nABV almost sacked Modi as Gujarat CM for his role in the riots. Everyone knows this.', b"Bhakts voted Modi not because they think he's innocent but because they know he's not and they admire his actions as that of a 21st century hindu warrior king. They're all as unethical as he is. Lying, dishonesty, dissembling are their core characteristics."""

    example = """The important thing is most of the Hindu middle class supports communalism against Muslims. It began with Babri Masjid and continues. Before anyone points finger at me, I have seen enough of anti-muslim bigotry by well-educated Hindu youths who themselves won't engage in violence but fully support Modi precisely because of his anti-Muslim stance.", b'The mistake is the assumption that bhakts are ignorant regarding his role. They are not. They know he was involved and they love him because he was involved.', b"India's entire system is now a slave to Mr. Narendra Modi, All government institutions, judiciary have succumbed to death thanks to his muscleman Mr. Amit Shah."""

    example = """Why digging old evidence.. its not something hidden by BJP anymore. Recently amit shah on stage said something like "yaad hai na 2002 me kaise sabak sikahya"""

    example = """People already know, yet Gujrat has been a bjp state for over 20 years and india continues to vote for them for the past 10 years.\nYet further below, we still think that local ministers and MLA\xe2\x80\x99s should be people with police cases and serious courts trials."""

    example = """Fun fact: Modi won the Gujarat elections AFTER the riots in the same year. \n\nThat tells you everything you need to know about the Indian electorate. They liked what he did. Haven\'t watched these documentaries but it\'ll only benefit him. When the wrong is right in people\'s eyes, "evidence" is irrelevant."""

    text = NER(example)
    
    for word in text.ents:
        print(word.text, word.label_)

    ent_toks = set([tok.text for tok in text.ents if tok.label_ in ["ORG", "PERSON", "NORP", "EVENT"]])
    sub_toks = set([tok.text for tok in text if tok.pos_ != "PROPN"])
    print(ent_toks)
    print(sub_toks)
    imp_toks = ent_toks.difference(sub_toks)
    print(imp_toks)

# spacy complete list of entities
# PERSON:      People, including fictional.
# NORP:        Nationalities or religious or political groups.
# FAC:         Buildings, airports, highways, bridges, etc.
# ORG:         Companies, agencies, institutions, etc.
# GPE:         Countries, cities, states.
# LOC:         Non-GPE locations, mountain ranges, bodies of water.
# PRODUCT:     Objects, vehicles, foods, etc. (Not services.)
# EVENT:       Named hurricanes, battles, wars, sports events, etc.
# WORK_OF_ART: Titles of books, songs, etc.
# LAW:         Named documents made into laws.
# LANGUAGE:    Any named language.
# DATE:        Absolute or relative dates or periods.
# TIME:        Times smaller than a day.
# PERCENT:     Percentage, including ”%“.
# MONEY:       Monetary values, including unit.
# QUANTITY:    Measurements, as of weight or distance.
# ORDINAL:     “first”, “second”, etc.
# CARDINAL:    Numerals that do not fall under another type.

