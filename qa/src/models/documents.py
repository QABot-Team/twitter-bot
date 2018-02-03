from models.document import Document


class Documents:
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
