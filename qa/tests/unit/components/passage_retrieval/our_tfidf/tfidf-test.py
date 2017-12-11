import unittest

import spacy

from components.passage_retrieval.our_tfidf.tfidf_ranker import TfIdfRanker
from models.passage import Passage
from models.passages import Passages
from models.question_model import QuestionModel

nlp = spacy.load('en')


def read_file(filename):
    result = ""
    file = open(filename)
    for line in file:
        result += " " + line
    file.close()
    return result


def text_to_token_list(text):
    doc = nlp(text)
    doc_tokens = []
    for token in doc:
        if not token.is_punct | token.is_space | token.is_stop:
            doc_tokens.append(token.text)
    return doc_tokens


class TfIdfTest(unittest.TestCase):

    def test_with_simple_input(self):
        passages = Passages()
        passages.add(Passage("c++ c++ object class oriented"))
        passages.add(Passage("class oriented code code sort sort python python"))
        passages.add(Passage("java java overflow sort stack stack"))
        passages.add(Passage("c++ pointer code code array"))
        passages.add(Passage("c++ object class oriented java"))
        passages.add(Passage("sort python python"))
        passages.add(Passage("object class java java array"))
        passages.add(Passage("c++ c++java java python python"))
        passages.add(Passage("loop loop code sort sort"))
        passages.add(Passage("class class code array array stack stack"))
        question = QuestionModel(["java", "stack", "overflow"])

        tfidf = TfIdfRanker(lambda text: text.split())
        ranked_passages = tfidf.calc_passage_ranks(passages, question)

        self.assertEqual("java java overflow sort stack stack", ranked_passages.get_passage_at(0).text)

    def test_with_wiki_article(self):
        arnold_article = read_file('arnold.txt')
        arnold_article_doc = nlp(arnold_article)
        arnold_sections = [sent.string.strip() for sent in arnold_article_doc.sents]  # arnold_article.split("\n")
        passages = Passages()
        for section in arnold_sections:
            passages.add(Passage(section))
        question = QuestionModel(text_to_token_list("Who is the brother of Arnold Schwarzenegger"))

        tfidf = TfIdfRanker(text_to_token_list)
        ranked_passages = tfidf.calc_passage_ranks(passages, question)

        self.assertTrue(ranked_passages.get_passage_at(0).text.find('Meinhard') != -1)
        for p in ranked_passages.passages:
            print(str(p.rank) + ': ' + p.text)


if __name__ == '__main__':
    unittest.main()
