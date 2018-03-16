from config import PASSAGE_WEIGHT, BIDAF_WEIGHT


class Prediction:
    def __init__(self, answer, context, doc_title, passage_id, elastic_score, tfidf_score, passage_score, bidaf_score):
        self.answer = answer
        self.context = context
        self.doc_title = doc_title
        self.passage_id = passage_id
        self.elastic_score = elastic_score
        self.tfidf_score = tfidf_score
        self.passage_score = passage_score
        self.bidaf_score = bidaf_score

    def calc_final_score(self):
        return (PASSAGE_WEIGHT * self.passage_score) + (BIDAF_WEIGHT * self.bidaf_score)
