import spacy
from collections import Counter
from spacy.lang.en.stop_words import STOP_WORDS
import spacy

nlp = spacy.load('en_core_web_sm')

def get_keywords(text, nlp, num_keywords=5):
    doc = nlp(text)
    filtered_words = [token.text for token in doc if not token.is_stop and not token.is_punct and token.pos_ in ['NOUN', 'ADJ', 'VERB']]
    word_freq = Counter(filtered_words)
    common_words = word_freq.most_common(num_keywords)
    return [word[0] for word in common_words]

def textrank_keyword_extraction(text, nlp, num_keywords=5):
    doc = nlp(text)
    sentences = [sent.text for sent in doc.sents]
    phrase_list = [phrase for phrase in sentences if len(phrase.strip()) > 0]
    num_phrases = len(phrase_list)
    
    # Build similarity matrix
    similarity_matrix = [[0.0] * num_phrases for _ in range(num_phrases)]
    for i in range(num_phrases):
        for j in range(i, num_phrases):
            if i == j:
                similarity_matrix[i][j] = 1.0
            else:
                similarity_matrix[i][j] = similarity_matrix[j][i] = nlp(phrase_list[i]).similarity(nlp(phrase_list[j]))

    # PageRank Algorithm
    damping_factor = 0.85
    iterations = 50
    pr = [1.0 / num_phrases] * num_phrases
    for epoch in range(iterations):
        updated_pr = [0] * num_phrases
        for i in range(num_phrases):
            for j in range(num_phrases):
                if i == j or not similarity_matrix[i][j]:
                    continue
                updated_pr[i] += (similarity_matrix[j][i] / sum(similarity_matrix[j])) * pr[j]
            updated_pr[i] = (1 - damping_factor) / num_phrases + damping_factor * updated_pr[i]
        pr = updated_pr

    # Extract top keywords
    phrase_scores = [(phrase_list[i], pr[i]) for i in range(num_phrases)]
    phrase_scores = sorted(phrase_scores, key=lambda t: t[1], reverse=True)

    keywords = []
    for i in range(num_keywords):
        if i >= len(phrase_scores):
            break
        keyword = get_keywords(phrase_scores[i][0], nlp, num_keywords=1)[0]
        keywords.append(keyword)
    
    return keywords

if __name__ == '__main__':
    doc = """
         The important thing is most of the Hindu middle class supports communalism against Muslims.
         It began with Babri Masjid and continues. Before anyone points finger at me, I have seen enough of anti-muslim 
         bigotry by well-educated Hindu youths who themselves won't engage in violence but fully support Modi 
         precisely because of his anti-Muslim stance.
      """
    keywords = textrank_keyword_extraction(doc,nlp)
    print(keywords)
    """
    result
    ['important', 'anti', 'began']
    
    there are certain improvements which need to be tested. BERT seems to be better
    """
