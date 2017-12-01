import spacy

from components.passage_retrieval.our_tfidf import tfidf
from components.passage_retrieval.our_tfidf.vector_utils import sim, vectorize


def receive_passages_ordered_by_best_matches_with_tfidf(unordered_passages, query):
    similarities = compare_word_lists_with_query(array_of_doc_tokens, query)
    passages_with_similarities = merge_passages_with_similarities(unordered_passages, similarities)
    return sorted(passages_with_similarities, key=lambda item: item['similarity'], reverse=True)


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


def merge_passages_with_similarities(passages, similarities):
    return [{'paragraph': p, 'similarity': similarities[passages.index(p)]} for p in passages]


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


similarities_result = compare_word_lists_with_query(bloblist, query)
print(similarities_result)
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


def str_to_input_list(passage):
    doc = nlp(passage)
    doc_tokens = []
    for token in doc:
        if not token.is_punct | token.is_space | token.is_stop:
            doc_tokens.append(token.text)
    return doc_tokens


array_of_doc_tokens = []
for p in arni_paragraphs:
    array_of_doc_tokens.append(str_to_input_list(p))


query = "Who is the brother of Arnold Schwarzenegger"
query = str_to_input_list(query)
print(query)
ordered_passages = receive_passages_ordered_by_best_matches_with_tfidf(array_of_doc_tokens, query)
for p in ordered_passages:
    print(str(p['similarity']) + ': ' + str(p['paragraph'])[:50])

