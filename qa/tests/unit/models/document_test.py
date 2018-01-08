import unittest

from models.documents import Document
from models.passage import Passage


class TestDocument(unittest.TestCase):

    def test_add_passage_to_right_document(self):
        doc1 = Document('Doc 1', 'Text 1')
        doc2 = Document('Doc 1', 'Text 1')
        doc2.add_passage(Passage('Text'))
        self.assertEqual(len(doc1.get_passages().passages), 0)


if __name__ == '__main__':
    unittest.main()
