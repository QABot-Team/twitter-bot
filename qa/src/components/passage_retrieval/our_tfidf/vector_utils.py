import math


def vectorize(list_of_word_score_dicts):
    word_index_dict = {}
    index = 0
    for word_score_dict in list_of_word_score_dicts:
        for key in word_score_dict:
            if key not in word_index_dict:
                word_index_dict[key] = index
                index = index + 1

    length = len(word_index_dict)
    res = []
    for word_score_dict in list_of_word_score_dicts:
        res.append(_build_vector_with(word_score_dict, word_index_dict, length))
    return res


def _build_vector_with(word_score_dict, word_index_dict, length):
    vector = [0] * length
    for word in word_score_dict:
        vector[word_index_dict[word]] = word_score_dict[word]
    return vector


def sim(vector_1, vector_2):
    zaehler = _scalar_product(vector_1, vector_2)
    nenner = _vector_length(vector_1) * _vector_length(vector_2)
    return zaehler / nenner


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

