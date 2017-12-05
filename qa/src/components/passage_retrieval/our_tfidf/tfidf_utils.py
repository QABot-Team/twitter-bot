import math
# see: http://stevenloria.com/finding-important-words-in-a-document-using-tf-idf/


def tf(word, list_of_words_in_doc):
    return list_of_words_in_doc.count(word)  # / len(wordlist)


def n_containing(word, list_of_docs):
    return sum(1 for list_of_words_in_doc in list_of_docs if word in list_of_words_in_doc)


def idf(word, list_of_docs):
    return math.log(len(list_of_docs) / (n_containing(word, list_of_docs)), 2)


def tfidf(word, list_of_words_in_doc, list_of_docs):
    return tf(word, list_of_words_in_doc) * idf(word, list_of_docs)
