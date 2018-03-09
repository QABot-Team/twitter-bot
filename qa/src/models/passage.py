class Passage:
    def __init__(self, text, elastic_score, parent_doc) -> None:
        self.text = text
        self.parent_doc = parent_doc
        self.elastic_score = elastic_score
        self.tfidf_score = 0
        self.bidaf_score = 0
