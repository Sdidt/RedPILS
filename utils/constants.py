from models.political_wing import PoliticalWing

# subreddits = {
#     "indiaspeaks": PoliticalWing.RIGHT,
#     "india": PoliticalWing.LEFT
# }

subreddits = {
    "indiaspeaks": PoliticalWing.RIGHT,
    "india": PoliticalWing.LEFT
}


keywords = [
    "BJP",
    "Congress",
    "AAP",
    # "Hindutva",
    # "Muslim",
    # "Hindu", 
    # "Riots",
    # "Gujarat"
]

solr_var = {
    "solr_url" : 'http://localhost:8983/solr',
    "configset_zip_path": "configset_modified.zip",
    "configset_name": "myConfigSet",
    "data_collection_name" : 'data_collection',
    "data_unique_key": "comment_id",
    "keyword_collection_name" : 'keyword_collection',
    "keyword_unique_key" : 'keyword',
    "headers" : {'Content-type': 'application/json'},
    "data_schema" : [
    {"name": "submission_id", "type": "string",'indexed': "true", "stored": "true"},
    {"name": "submission_title", "type": "filtered_text",'indexed': "true", "stored": "true"},
    {"name": "subreddit_id", "type": "text_en",'indexed': "true", "stored": "true"},
    {"name": "subreddit_name", "type": "text_en",'indexed': "true", "stored": "true"},
    {"name": "comment_id", "type": "string",'indexed': "true", "stored": "true"},
    {"name": "comment", "type": "filtered_text",'indexed': "true", "stored": "true", "termVectors": "true"},
    {"name": "timestamp", "type": "pdate",'indexed': "true", "stored": "true"},
    {"name": "url", "type": "text_en", "indexed": "true", "stored": "true"},
    {"name": "reddit_score", "type": "pint",'indexed': "true", "stored": "true"},
    {"name": "redditor_id", "type": "text_en",'indexed': "true", "stored": "true"},
    {"name": "polarity", "type": "pfloat", "indexed": "true", "stored": "true", "default": "0.0"}
    ],
    "tag_field_type": {
        "name": "tag",
        "class": "solr.TextField",
            "omitNorms":"true",
        "omitTermFreqAndPositions":"true",
        "indexAnalyzer":{
        "tokenizer":{
            "class":"solr.StandardTokenizerFactory" },
        "filters":[
            {"class":"solr.EnglishPossessiveFilterFactory"},
            {"class":"solr.ASCIIFoldingFilterFactory"},
            {"class":"solr.LowerCaseFilterFactory"},
            {"class":"solr.ConcatenateGraphFilterFactory", "preservePositionIncrements":"false" }
        ]},
        "queryAnalyzer":{
        "tokenizer":{
            "class":"solr.StandardTokenizerFactory" },
        "filters":[
            {"class":"solr.EnglishPossessiveFilterFactory"},
            {"class":"solr.ASCIIFoldingFilterFactory"},
            {"class":"solr.LowerCaseFilterFactory"}
      ]}
    },
    "tag_field": {
        "name": "comment_tag",
        "type": "tag",
        "stored": "false"
    },
    "tag_request_handler": {
        "name": "/tag",
        "class":"solr.TaggerRequestHandler",
        "defaults":{"field":"comment_tag"}
    },
    "copy_tag_field": {
        "source": "comment", 
        "dest": ["comment_tag"]
    },
    'params': {
            'q': 'comment_id:j0u6jwf',
            'fl': 'comment_id,comment,score',
            'rows': 10
        },
    "posted_at_field": {
        "name": "posted_at",
        "type": "pdate",
        "stored": "true",
        "indexed": "true",
        "docValues": "true"
    },
    "copy_timestamp_field": {
        "source": "timestamp",
        "dest": ["posted_at"]
    },
    "update_timestamp": {
        "name": "timestamp", "type": "pdate",'indexed': "true", "stored": "true"
    },
    'keyword_schema':[
    {"name": "keyword", "type": "filtered_text",'indexed': "true", "stored": "true"},
    ],
    'filtered_text_type': {
        "name": "filtered_text",
        "class": "solr.TextField",
        "autoGeneratePhraseQueries": "true",
        "indexAnalyzer": {
            "tokenizer": {
                "name": "standard"
            },
            "filters": [
            {"name": "trim"},
            {"name": "lowercase"},
            {
                "name": "synonymGraph",
                "synonyms": "synonyms_redpils.txt",
                "ignoreCase": "true"
            },
            {
                "name": "stop",
                "words": "lang/stopwords_nltk.txt",
                # "ignoreCase": "true"
            },
            # not ideal; modify the NGram filter
            # {
            #     "name": "nGram",
            #     "minGramSize": "2",
            #     "maxGramSize": "3"
            # }
            ]
        },
        "queryAnalyzer": {
            "tokenizer": {
                "name": "standard"
            },
            "filters": [
            {
                "name": "trim"
            },
            {
                "name": "lowercase"
            },
            {
                "name": "synonymGraph",
                "synonyms": "synonyms_redpils.txt",
                "ignoreCase": "true"
            },
            {
                "name": "stop",
                "words": "lang/stopwords_nltk.txt",
                # "ignoreCase": "true"
            },
            # not ideal; modify the NGram filter
            # {
            #     "name": "nGram",
            #     "minGramSize": "2",
            #     "maxGramSize": "3"
            # },
            ]
        },
        "similarity": {
            "class": "solr.ClassicSimilarityFactory"
        }
    }
}