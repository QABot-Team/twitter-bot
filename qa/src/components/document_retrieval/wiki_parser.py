from models.documents import Documents
from models.passage import Passage


class WikiParser:
    @staticmethod
    def add_passages(raw_docs: Documents):
        for doc in raw_docs:
            text = doc.text

            paragraphs = text.split('    ')
            for p in paragraphs[:-1]:
                if p.strip() != "":
                    doc.add_passage(Passage(p, doc.elastic_score, doc))
