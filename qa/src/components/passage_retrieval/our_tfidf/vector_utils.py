import math


def vectorize(list_of_word_score_dicts):
    word_index_dict = {}
    index = 0
    for word_score_dict in list_of_word_score_dicts:
        for key in word_score_dict:
            if key not in word_index_dict:
                word_index_dict[key] = index
                index = index + 1

    res = []
    for word_score_dict in list_of_word_score_dicts:
        res.append(_build_vector_with(word_score_dict, word_index_dict))
    return res


def _build_vector_with(word_score_dict, word_index_dict):
    vector = [0] * len(word_index_dict)
    for word in word_score_dict:
        vector[word_index_dict[word]] = word_score_dict[word]
    return vector


def sim(vector_1, vector_2):
    numerator = _scalar_product(vector_1, vector_2)
    denumerator = _vector_length(vector_1) * _vector_length(vector_2)
    if denumerator == 0:
        return 0
    return numerator / denumerator


def _scalar_product(vector_1, vector_2):
    summe = 0
    for i, v1 in enumerate(vector_1):
        summe += v1 * vector_2[i]
    return summe


def _vector_length(vector):
    summe = 0
    for v in vector:
        summe += v**2
    return math.sqrt(summe)

