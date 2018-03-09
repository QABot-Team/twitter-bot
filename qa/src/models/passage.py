class Passage:
    def __init__(self, text, elastic_score) -> None:
        self.text = text
        self.elastic_score = elastic_score
        self.tfidf_score = 0
        self.bidaf_score = 0
