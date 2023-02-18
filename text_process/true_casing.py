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
    example = "Why digging old evidence.. its not something hidden by BJP anymore. Recently amit shah on stage said something like yaad hai na 2002 me kaise sabak sikahya"
    truecased_sent = true_casing(example)
    print(truecased_sent)