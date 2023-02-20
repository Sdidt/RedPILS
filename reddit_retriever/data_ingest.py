from reddit_retriever.crawler import Crawler
from reddit_retriever.solr_interface import solr_ingest
from models.comment import Comment

import json




# define solr endpoint
solr_url = 'http://localhost:8983/solr'
# define collection name
collection_name = 'new_collection'
# global headers definition
headers = {'Content-type': 'application/json'}
# dummy data to be ingested into solr database
data = [
        {'id': '1', 'title': 'Document 1', 'text': 'This is the first document'},
        {'id': '2', 'title': 'Document 2', 'text': 'This is the second document'},
        {'id': '3', 'title': 'Document 3', 'text': 'This is the third document'}
    ]
# query params
# q - query
# fl - fields to query
# rows - max rows to query
params = {
        'q': 'text:document',
        'fl': 'id,title',
        'rows': 10
    }
fields = [
        {"name": "id", "type": "string"},
        {"name": "title", "type": "text_en"},
        {"name": "content", "type": "text_en"},
        ]

# define solr_ingest object
data_ingest = solr_ingest(solr_url,collection_name,headers,data)
# delete collection defined above
data_ingest.delete_collection('my_collection')
# create new collection using same name
data_ingest.create_collection(collection_name,fields)
# delete all data in the collection
data_ingest.delete_data(collection_name)
# push data to the collection
data_ingest.push_data(collection_name)
# query data based on paramaters defined above
search_data = data_ingest.query_data(params,collection_name)
print(search_data)
# update data based on rules defined inside the function
data_ingest.update_data(collection_name)
