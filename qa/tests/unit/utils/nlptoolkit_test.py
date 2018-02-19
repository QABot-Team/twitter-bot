import unittest

from utils.nlptoolkit import NLPToolkit

nlp_toolkit = NLPToolkit()


class TestNLPToolkit(unittest.TestCase):

    def test_get_headwords(self):
        headwords = nlp_toolkit.get_headwords('What is question answering')
        print(headwords)


if __name__ == '__main__':
    unittest.main()
