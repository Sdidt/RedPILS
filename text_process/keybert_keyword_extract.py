from keybert import KeyBERT

# doc = """
#          Supervised learning is the machine learning task of learning a function that
#          maps an input to an output based on example input-output pairs. It infers a
#          function from labeled training data consisting of a set of training examples.
#          In supervised learning, each example is a pair consisting of an input object
#          (typically a vector) and a desired output value (also called the supervisory signal).
#          A supervised learning algorithm analyzes the training data and produces an inferred function,
#          which can be used for mapping new examples. An optimal scenario will allow for the
#          algorithm to correctly determine the class labels for unseen instances. This requires
#          the learning algorithm to generalize from the training data to unseen situations in a
#          'reasonable' way (see inductive bias).
#       """
doc = """
         The important thing is most of the Hindu middle class supports communalism against Muslims.
         It began with Babri Masjid and continues. Before anyone points finger at me, I have seen enough of anti-muslim 
         bigotry by well-educated Hindu youths who themselves won't engage in violence but fully support Modi 
         precisely because of his anti-Muslim stance.
      """
kw_model = KeyBERT()
keywords_1 = kw_model.extract_keywords(doc)
print(keywords_1)
"""
result
[('hindu', 0.4547), ('bigotry', 0.414), ('muslim', 0.3839), ('muslims', 0.3818), ('communalism', 0.3555)]
"""
keywords_2 = kw_model.extract_keywords(doc, keyphrase_ngram_range=(1, 2), stop_words=None)
print(keywords_2)
"""
[('muslim bigotry', 0.5646), ('hindu middle', 0.5147), ('muslim stance', 0.5126), ('anti muslim', 0.4846), ('supports communalism', 0.476)]
"""
