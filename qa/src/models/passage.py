from config import ELASTIC_WEIGHT, TFIDF_WEIGHT


class Passage:
    def __init__(self, text, elastic_score=0, parent_doc=None, passage_index=0) -> None:
        self.text = text
        self.parent_doc = parent_doc
        self.passage_index = passage_index
        self.elastic_score = elastic_score
        self.tfidf_score = 0
        self.bidaf_score = 0

    def get_passage_score(self):
        return ELASTIC_WEIGHT * self.elastic_score + TFIDF_WEIGHT * self.tfidf_score

    def get_id(self) -> str:
        return str(self.passage_index) if self.parent_doc is None \
            else str(self.parent_doc.get_id()) + '-' + str(self.passage_index)
