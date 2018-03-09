from config import ELASTIC_WEIGHT, TFIDF_WEIGHT
from models.passage import Passage


class RankedPassage(Passage):
    def __init__(self, passage, rank: float) -> None:
        super(RankedPassage, self).__init__(passage.text, passage.elastic_score, passage.parent_doc)
        self.rank = rank
        self.tfidf_score = rank

    def get_rank(self):
        return ELASTIC_WEIGHT * self.elastic_score + TFIDF_WEIGHT * self.tfidf_score
