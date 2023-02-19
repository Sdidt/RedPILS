class Comment:
    def __init__(self, submission_id, submission_title, id, comment, timestamp, url, score, redditor_id) -> None:
        self.submission_id = submission_id
        self.submission_title = submission_title
        self.id = id
        self.comment = comment
        self.timestamp = timestamp
        self.url = url
        self.score = score
        self.redditor_id = redditor_id
