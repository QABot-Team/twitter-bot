from models.documents import Document, Documents
from models.passage import Passage


class WikiParser:
    @staticmethod
    def parse_docs(raw_docs: list) -> Documents:
        docs = Documents()
        for es_doc in raw_docs:
            text = es_doc['text']
            doc = Document(es_doc['title'], text)

            paragraphs = text.split('    ')
            for p in paragraphs[:-1]:
                if p.strip() != "":
                    doc.add_passage(Passage(p))

            docs.add(doc)

        return docs
