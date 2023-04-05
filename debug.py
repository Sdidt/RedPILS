from utils.constants import solr_var
from reddit_retriever.solr_interface import solr_ingest


def check_total_word_length():
    search_data = data_ingest.query_data({'q':'*:*','rows':1000000},solr_var['data_collection_name'])
    total_num_words = 0
    for comment in search_data:
        # print(comment)
        num_words = len(comment["comment"].split(" "))
        total_num_words += num_words
        print("Comment length: {}".format(num_words))

    print("Total word length: {}".format(total_num_words))

def check_unique_words():
    search_data = data_ingest.query_data({'q':'*:*','rows':1000000},solr_var['data_collection_name'])
    total_words = set()
    for comment in search_data:
        # print(comment)
        total_words.update(set(comment["comment"].split(" ")))
        print("Comment unique length: {}".format(len(set(comment["comment"].split(" ")))))

    print("Total word length: {}".format(len(total_words)))

def get_avg_length():
    search_data = data_ingest.query_data({'q':'*:*','rows':1000000},solr_var['data_collection_name'])
    avg_num_words = 0
    for comment in search_data:
        # print(comment)
        num_words = len(comment["comment"].split(" "))
        avg_num_words += num_words
        print("Comment length: {}".format(num_words))
    avg_num_words = avg_num_words / len(search_data)
    print("Average comment length: {}".format(avg_num_words))

def compute_query_term_score(query_term):
    search_results = data_ingest.compute_query_term_score(query_term, solr_var['data_collection_name'], 10)
    [print("Score: {}\nComment: {}".format(doc["score"], doc["comment"])) for doc in search_results]

def get_phrase_query_results(phrase_query):
    time_elapsed, search_results = data_ingest.phrase_query(solr_var['data_collection_name'], phrase_query, 5, 10, 20, 40, "2022-03-29T00:00:00Z", "2022-04-29T00:00:00Z", True, 10, "5", "5")
    print(search_results)
    search_results = [{
        "score": doc["score"],
        "comment": doc["comment"],
        "url": "https://www.reddit.com" + doc["url"],
        "timestamp": doc["timestamp"]
    } for doc in search_results]
    [print("Score: {}\nComment: {}\nURL: {}\nPosted at: {}".format(doc["score"], doc["comment"], doc["url"], doc["timestamp"])) for doc in search_results]

if __name__ == "__main__":
    data_ingest = solr_ingest(solr_var["solr_url"],solr_var['data_collection_name'],solr_var['headers'])
    # check_total_word_length()
    # check_unique_words()
    # get_avg_length()
    # compute_query_term_score("INC")
    get_phrase_query_results("islam NOT Congress")