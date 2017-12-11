from components.passage_retrieval.our_tfidf import tfidf, vectorize, sim
from models.passages import Passages
from models.question_model import QuestionModel
from models.ranked_passages import RankedPassages


class TfIdfRanker:
    def __init__(self, convert_text_to_token_list):
        self.convert_text_to_token_list = convert_text_to_token_list

    def calc_passage_ranks(self, passages: Passages, question_model: QuestionModel) -> RankedPassages:
        query_vector = question_model.get_keywords()
        list_of_passage_tokens = passages.map(lambda passage: self.convert_text_to_token_list(passage.text))

        query_dict = self._build_query_dictionary(query_vector)
        score_list = self._calculate_score_list(list_of_passage_tokens)

        vectors = vectorize(score_list + [query_dict])
        list_of_passage_vectors = vectors[:-1]
        query_vector = vectors[-1]
        similarities_array = self._calculate_similarities(list_of_passage_vectors, query_vector)

        ranked_passages = self._build_ranked_passages_from(passages, similarities_array)
        ranked_passages.sort()
        return ranked_passages

    @staticmethod
    def _build_query_dictionary(query_vector):
        query_dict = {}
        for q in query_vector:
            query_dict[q] = 1
        return query_dict

    @staticmethod
    def _calculate_score_list(vector_of_passage_tokens):
        score_list = []
        for i, passage_vector in enumerate(vector_of_passage_tokens):
            scores = {word: tfidf(word, passage_vector, vector_of_passage_tokens) for word in passage_vector}
            score_list.append(scores)
        return score_list

    @staticmethod
    def _calculate_similarities(list_of_passage_vectors, query_vector):
        res = []
        for passage_vector in list_of_passage_vectors:
            similarity = sim(passage_vector, query_vector)
            res.append(similarity)
        return res

    @staticmethod
    def _build_ranked_passages_from(passages: Passages, similarities_array: list) -> RankedPassages:
        ranked_passages = RankedPassages()
        for i, similarity in enumerate(similarities_array):
            passage = passages.get_passage_at(i)
            ranked_passages.add_passage(passage, similarity)
        return ranked_passages

