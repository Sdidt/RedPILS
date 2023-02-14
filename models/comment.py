class Comment:
    def __init__(self, id, comment, timestamp, url, score, redditor_id) -> None:
        self.id = id
        self.comment = comment
        self.timestamp = timestamp
        self.url = url
        self.score = score
        self.redditor_id = redditor_id
