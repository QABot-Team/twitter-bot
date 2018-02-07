from models.passages import Passages, Passage


class Document:
    def __init__(self, title: str, text: str, passages: Passages = None) -> None:
        self.title = title
        self.text = text
        self.passages = Passages() if passages is None else passages

    def add_passage(self, passage: Passage):
        self.passages.add(passage)

    def get_passages(self):
        return self.passages
