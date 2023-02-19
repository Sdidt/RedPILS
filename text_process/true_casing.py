import stanfordnlp

#--------------------------------------------
# uncomment when running for the first time
# stanfordnlp.download('en')
#--------------------------------------------

def true_casing(text):

    stf_nlp = stanfordnlp.Pipeline(processors='tokenize,mwt,pos')
    doc = stf_nlp(text)
    # print(*[f'word: {word.text+" "}\tupos: {word.upos}\txpos: {word.xpos}' for sent in doc.sentences for word in sent.words], sep='\n')
    truecased_sentence = ' '.join([w.text.capitalize() if w.upos in ["PROPN","NNS"] else w.text for sent in doc.sentences for w in sent.words])
    return truecased_sentence

if __name__ == '__main__':
    example = "The important thing is most of the Hindu middle class supports communalism against Muslims. It began with Babri Masjid and continues. Before anyone points finger at me, I have seen enough of anti-muslim bigotry by well-educated Hindu youths who themselves won't engage in violence but fully support Modi precisely because of his anti-Muslim stance."
    truecased_sent = true_casing(example)
    print(truecased_sent)