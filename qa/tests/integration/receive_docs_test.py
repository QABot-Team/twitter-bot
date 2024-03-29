import unittest

from components import document_retrieval
from models.question_model import QuestionModel
import urllib3

from utils.nlptoolkit import NLPToolkit


def elastic_connection_established():
    try:
        http = urllib3.PoolManager()
        http.request('GET', 'http://localhost:9200')
        return True
    except Exception as err:
        return False


@unittest.skipUnless(elastic_connection_established(), "requires elastic connection")
class TestReceiveDocs(unittest.TestCase):

    def test_returns_main_article(self):
        question_str = "Arnold Schwarzenegger"
        question_model = QuestionModel(question_str.split(), question_str)
        result = document_retrieval.receive_docs(question_model, NLPToolkit())
        self.assertEqual(result.get_doc_with_highest_rank().title, 'Arnold Schwarzenegger')


if __name__ == '__main__':
    unittest.main()
