from utils.constants import solr_var
from reddit_retriever.solr_interface import solr_ingest


data_ingest = solr_ingest(solr_var["solr_url"],solr_var['data_collection_name'],solr_var['headers'])

def check_total_word_length():
    search_data = data_ingest.query_data({'q':'*:*','rows':1000000},solr_var['data_collection_name'])
    total_num_words = 0
    for comment in search_data:
        # print(comment)
        num_words = len(comment["comment"].split(" "))
        total_num_words += num_words
        print("Comment length: {}".format(num_words))

    print("Total word length: {}".format(total_num_words))

def compute_query_term_score(query_term):
    search_results = data_ingest.compute_query_term_score(query_term, solr_var['data_collection_name'], 10)
    [print("Score: {}\nComment: {}".format(doc["score"], doc["comment"])) for doc in search_results]

def get_phrase_query_results(phrase_query):
    search_results = data_ingest.phrase_query(solr_var['data_collection_name'], phrase_query, 5, 10, 20, 40, 10)
    search_results = [{
        "score": doc["score"],
        "comment": doc["comment"],
        "url": "https://www.reddit.com" + doc["url"]
    } for doc in search_results]
    [print("Score: {}\nComment: {}\nURL: {}".format(doc["score"], doc["comment"], doc["url"])) for doc in search_results]

# compute_query_term_score("INC")
get_phrase_query_results("BJP rss Bhakts Hindu Sanatan dharma NOT congress")