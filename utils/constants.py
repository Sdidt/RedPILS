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
    "collection_name" : 'new_collection',
    "headers" : {'Content-type': 'application/json'},
    "schema" : [
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
            'q': 'comment_id:j1vkv1r',
            'fl': 'comment_id,comment,score',
            'rows': 10
        }
}