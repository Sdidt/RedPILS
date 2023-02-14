import spacy
from spacy import displacy


if __name__ == "__main__":
    NER = spacy.load("en_core_web_sm")

    example = "> the dogma itself matters a huge deal. \n\nSure, if one is doing a granular, discrete level of analysis. Which is not what my comment was about or even what this post's insinuation is.\n\nIn meta, general, normalized terms ALL Dogma is regressive, without exception. It is not irrelevant that 1 approach wastes more generations sure but compared to approaches which don't waste any or near to that it isn't much.\n\n> And nobody talks about spectrums\n\nWhen one is already Inside a spectrum and as you say *Simplify* (which is what above mentioned granular research would be about) then it's not necessary to invoke Spectrums or Gradients sure.\n\nBut that is not what my comment and this topic was about. \n\nIf entire world was on the same Dogma fix then it would be applicable to not even mention this since everyone is on the same boat.  \nBut the entire world is NOT on the same exact Dogma. There are different Dogma's, All regressive, all with different decay curves/half-lives. \n\n> The ethnically monolithic, clan-based, Sunni Pushtun Taliban are not to be compared with Hindu Nationalism in India in any credible way. It's a complete mischaracterization of the economic, linguistic, ethnic, and inter-religious, and historic issues we face, that have led to our current predicament.\n\nThis is that different topic to my comment's intentions. Though interestingly even this can be sort of squared in a way.  \nWe know there isn't a place on this planet which had a more powerful endogamic dynamic than South Asia. \nWe have both cultural and most critically genetic evidence to back this. \n\nVarious Caste and clan networks in India makes anything the Afghans came up with as juvenile play.\n\nThen there is Scale, which most western social sciences model just can not adjust to because they had no reference to even comprehend it.\n\nTo me India is in the midst of having multiple different Dogmas (of severity which are in net terms indeed near in place inside that Spectrum space to whatever the Talibanisation is).   \n\nOne of them is this Hindutva, Hindu Nationalization, Hindu Supremacy, whatever term one wants to use.  \n\nAnother is one India shares with large part of the world and that is this Dogma of Governance System supremacy.\n\nThese are Dogma which are State and society ending level. Just because their execution timeframe is a century longer is hardly relevant when the level of destruction is of that sort of scale."


    text = NER(example)
    
    for word in text.ents:
        print(word.text, word.label_)

    sub_toks = [tok for tok in text if (tok.dep_ == 'nsubj' and tok.pos_ == "PROPN")]
    print(sub_toks)