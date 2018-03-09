from models.iterable import Iterable
from models.passage import Passage


class Passages(Iterable):
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

    def get_score(self, psg: Passage):
        return psg.tfidf_score

    def set_score(self, psg: Passage, score: float):
        psg.tfidf_score = score

    def sort(self):
        self.passages = sorted(
            self.passages,
            key=lambda passage: passage.get_passage_score(),
            reverse=True
        )
