import unittest

from components import document_retrieval
from models.question_model import QuestionModel


class TestReceiveDocs(unittest.TestCase):

    def test_returns_main_article(self):
        question_model = QuestionModel(['Arnold', 'Schwarzenegger'])
        result = document_retrieval.receive_docs(question_model)
        self.assertEqual(result.get_doc_with_highest_rank().title, 'Arnold Schwarzenegger')


if __name__ == '__main__':
    unittest.main()
