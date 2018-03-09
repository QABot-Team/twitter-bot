from models.document import Document
from models.iterable import Iterable


class Documents(Iterable):
    def __init__(self) -> None:
        self.docs = []

    def add(self, doc: Document) -> None:
        self.docs.append(doc)

    def get_doc(self, idx):
        if 0 <= idx < len(self.docs):
            return self.docs[idx]
        else:
            return None

    def get_doc_with_highest_rank(self) -> Document:
        return self.docs[0]

    def __iter__(self):
        return iter(self.docs)

    def get_score(self, doc: Document):
        return doc.elastic_score

    def set_score(self, doc: Document, score: float):
        doc.elastic_score = score

