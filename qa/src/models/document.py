from models.passages import Passages, Passage


class Document:
    def __init__(self, title: str, text: str, passages: Passages = Passages(),
                 infobox: str = "", short_desc: str = "") -> None:
        self.title = title
        self.text = text
        self.infobox = infobox
        self.short_desc = short_desc
        self.passages = passages

    def add_passage(self, passage: Passage):
        self.passages.add(passage)

    def get_passages(self):
        return self.passages

    def set_infobox(self, infobox: str):
        self.infobox = infobox

    def set_sort_desc(self, short_desc: str):
        self.short_desc = short_desc
