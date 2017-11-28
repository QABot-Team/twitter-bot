import math

import spacy


def tf(word, wordlist):
    return wordlist.count(word)  # / len(wordlist)


def n_containing(word, bloblist):
    return sum(1 for blob in bloblist if word in blob)


def idf(word, bloblist):
    return math.log(len(bloblist) / (n_containing(word, bloblist)), 2)


def tfidf(word, blob, bloblist):
    return tf(word, blob) * idf(word, bloblist)


def build_vector_with(word_score_dict, word_index_dict, length):
    vector = [0] * length
    for word in word_score_dict:
        vector[word_index_dict[word]] = word_score_dict[word]
    return vector


def vectorize(list_of_word_score_dicts):
    word_index_dict = {}
    index = 0
    for word_score_dict in list_of_word_score_dicts:
        for key in word_score_dict:
            if key not in word_index_dict:
                word_index_dict[key] = index
                index = index + 1

    length = len(word_index_dict)
    # return map(lambda x: build_vector_with(x, word_index_dict, length), list_of_word_score_dicts)
    res = []
    for word_score_dict in list_of_word_score_dicts:
        res.append(build_vector_with(word_score_dict, word_index_dict, length))
    return res


def scalar_product(vector_1, vector_2):
    summe = 0
    for i, v1 in enumerate(vector_1):
        summe += v1 * vector_2[i]
    return summe


def vector_length(vector):
    summe = 0
    for v in vector:
        summe += v**2
    return math.sqrt(summe)


def sim(vector_1, vector_2):
    zaehler = scalar_product(vector_1, vector_2)
    nenner = vector_length(vector_1) * vector_length(vector_2)
    return zaehler / nenner


def compare_docs_with_query(list_of_doc_vectors, query_vector):
    res = []
    for doc_vector in list_of_doc_vectors:
        similarity = sim(doc_vector, query_vector)
        res.append(similarity)
    return res


def compare_word_lists_with_query(word_lists, query_list):
    query_dict = {}
    for q in query_list:
        query_dict[q] = 1

    score_list = []
    for i, word_list in enumerate(word_lists):
        scores = {word: tfidf(word, word_list, word_lists) for word in word_list}
        score_list.append(scores)

    vectors = vectorize(score_list + [query_dict])
    return compare_docs_with_query(vectors[:-1], vectors[-1])


doc_1 = ["c++", "c++", "object", "class", "oriented"]
doc_2 = ["class", "oriented", "code", "code", "sort", "sort", "python", "python"]
doc_3 = ["java", "java", "overflow", "sort", "stack", "stack"]
doc_4 = ["c++", "pointer", "code", "code", "array"]
doc_5 = ["c++", "object", "class", "oriented", "java"]
doc_6 = ["sort", "python", "python"]
doc_7 = ["object", "class", "java", "java", "array"]
doc_8 = ["c++", "c++" "java", "java", "python", "python"]
doc_9 = ["loop", "loop", "code", "sort", "sort"]
doc_10 = ["class", "class", "code", "array", "array", "stack", "stack"]

query = ["java", "stack", "overflow"]
bloblist = [doc_1, doc_2, doc_3, doc_4, doc_5, doc_6, doc_7, doc_8, doc_9, doc_10]


similarities = compare_word_lists_with_query(bloblist, query)
print(similarities)
print()
print()
print()


def read_file(filename):
    result = ""
    file = open('docs/' + filename)
    for line in file:
        result += " " + line
    file.close()
    return result


arni_complete = read_file('arni.txt')
arni_paragraphs = arni_complete.split("\n")

nlp = spacy.load('en')

array_of_doc_tokens = []
for p in arni_paragraphs:
    doc = nlp(p)
    doc_tokens = []
    for token in doc:
        if not token.is_punct | token.is_space | token.is_stop:
            doc_tokens.append(token.text)
    array_of_doc_tokens.append(doc_tokens)


arni_sims = compare_word_lists_with_query(
    array_of_doc_tokens, ["Wie", "heißt", "der", "Bruder", "von", "Arnold", "Schwarzenegger"])
print(arni_sims)
