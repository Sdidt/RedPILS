from models.political_wing import PoliticalWing

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

schema = [
    {"name": "title", "type": "text_en", 'indexed':'true','stored':'true'},
    {"name": " comment_id", "type": "string", 'indexed':'true','stored':'true'},
    {"name": "comment", "type": "text_en", 'indexed':'true','stored':'true'},
    {"name": "timestamp", "type": "string", 'indexed':'true','stored':'true'},
    {"name": "url", "type": "text_en"},
    {"name": "score", "type": "pint"},
    {"name": "redditor_id", "type": "text_en"},
    ]