from models.passage import Passage


class RankedPassage(Passage):
    def __init__(self, text, rank: float) -> None:
        super(RankedPassage, self).__init__(text)
        self.rank = rank
