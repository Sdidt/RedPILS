from models.political_wing import PoliticalWing

# subreddits = {
#     "indiaspeaks": PoliticalWing.RIGHT,
#     "india": PoliticalWing.LEFT
# }

subreddits = {
    "indiaspeaks": PoliticalWing.RIGHT}


keywords = [
    "BJP",
    # "Congress",
    # "AAP",
    # "Hindutva",
    # "Muslim",
    # "Hindu", 
    # "Riots",
    # "Gujarat"
]

solr_var = {
    "solr_url" : 'http://localhost:8983/solr',
    "data_collection_name" : 'data_collection',
    "data_unique_key": "comment_id",
    "keyword_collection_name" : 'keyword_collection',
    "keyword_unique_key" : 'keyword',
    "headers" : {'Content-type': 'application/json'},
    "data_schema" : [
    {"name": "submission_id", "type": "string",'indexed': "true", "stored": "true"},
    {"name": "submission_title", "type": "text_en",'indexed': "true", "stored": "true"},
    {"name": "subreddit_id", "type": "text_en",'indexed': "true", "stored": "true"},
    {"name": "subreddit_name", "type": "text_en",'indexed': "true", "stored": "true"},
    {"name": "comment_id", "type": "text_en",'indexed': "true", "stored": "true"},
    {"name": "comment", "type": "text_en",'indexed': "true", "stored": "true"},
    {"name": "timestamp", "type": "text_en",'indexed': "true", "stored": "true"},
    {"name": "url", "type": "text_en"},
    {"name": "score", "type": "pint",'indexed': "true", "stored": "true"},
    {"name": "redditor_id", "type": "text_en",'indexed': "true", "stored": "true"}
    ],
    'params': {
            'q': 'comment_id:j0u6jwf',
            'fl': 'comment_id,comment,score',
            'rows': 10
        },
    'keyword_schema':[
    {"name": "keyword", "type": "text_en",'indexed': "true", "stored": "true"},
    ]
}