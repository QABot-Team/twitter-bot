from models.passage import Passage


class RankedPassage(Passage):
    def __init__(self, passage, rank: float) -> None:
        super(RankedPassage, self).__init__(passage.text, passage.parent_doc)
        self.rank = rank
