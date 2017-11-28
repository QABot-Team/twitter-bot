from models.document import Document


class Documents:
    def __init__(self) -> None:
        self.docs = []

    def add(self, doc: Document) -> None:
        self.docs.append(doc)
