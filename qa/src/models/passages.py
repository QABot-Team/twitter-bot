from models.passage import Passage


class Passages:
    def __init__(self) -> None:
        self.passages = []

    def add(self, passage: Passage) -> None:
        self.passages.append(passage)
