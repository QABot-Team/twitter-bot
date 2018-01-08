import unittest

from components.document_retrieval.wiki_parser import WikiParser
from models.document import Document


class TestWikiParser(unittest.TestCase):

    def test_parse_headline_with_whitespace(self):
        parser = WikiParser()
        doc = Document('Title', 'Text')

        source_text = 'Text without headline\n=== Headline 1 ===\nBla bla bla.'
        header = ['Headline 1']

        result = parser.parse_source_text(doc, source_text, header)
        self.assertEqual(len(result.get_passages().passages), 1)

    def test_parse_headline_without_whitespace(self):
        parser = WikiParser()
        doc = Document('Title', 'Text')

        source_text = 'Text without headline\n===Headline 1===\nBla bla bla.'
        header = ['Headline 1']

        result = parser.parse_source_text(doc, source_text, header)
        self.assertEqual(len(result.get_passages().passages), 1)


if __name__ == '__main__':
    unittest.main()
