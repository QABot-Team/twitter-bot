from config import ELASTIC_WEIGHT, TFIDF_WEIGHT


class Passage:
    def __init__(self, text, elastic_score=0, parent_doc=None) -> None:
        self.text = text
        self.parent_doc = parent_doc
        self.elastic_score = elastic_score
        self.tfidf_score = 0
        self.bidaf_score = 0

    def get_passage_score(self):
        return ELASTIC_WEIGHT * self.elastic_score + TFIDF_WEIGHT * self.tfidf_score
