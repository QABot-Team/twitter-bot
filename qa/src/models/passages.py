from models.passage import Passage


class Passages:
    def __init__(self) -> None:
        self.passages = []

    def add(self, passage: Passage) -> None:
        self.passages.append(passage)

    def get_passage_at(self, index: int) -> Passage:
        return self.passages[index]

    def map(self, action) -> []:
        return list(map(action, self.passages))

    def __iter__(self):
        return iter(self.passages)
