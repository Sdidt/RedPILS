class Comment:
    def __init__(self, submission_id, submission_title, subreddit_id, subreddit_name, id, comment, timestamp, url, score, redditor_id) -> None:
        self.submission_id = submission_id
        self.submission_title = submission_title
        self.subreddit_id = subreddit_id
        self.subreddit_name = subreddit_name
        self.id = id
        self.comment = comment
        self.timestamp = timestamp
        self.url = url
        self.score = score
        self.redditor_id = redditor_id
    
    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, str):
            return __o == self.submission_id
