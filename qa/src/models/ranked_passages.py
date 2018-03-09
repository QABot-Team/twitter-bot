from models.passage import Passage
from models.passages import Passages
from models.ranked_passage import RankedPassage


class RankedPassages(Passages):
    def __init__(self) -> None:
        super(RankedPassages, self).__init__()

    def add_passage(self, passage: Passage, rank: float):
        self.add(RankedPassage(passage, rank))

    def add(self, passage: RankedPassage) -> None:
        if not isinstance(passage, RankedPassage):
            raise ValueError('Object of type RankedPassage expected')
        super(RankedPassages, self).add(passage)

    def sort(self):
        self.passages = sorted(self.passages, key=lambda ranked_passage: ranked_passage.rank, reverse=True)
