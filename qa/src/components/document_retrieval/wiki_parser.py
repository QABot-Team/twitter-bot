from models.documents import Documents
from models.passage import Passage


def split_larg_paragraphs(paragraph, max_len=60000):
    if len(paragraph) > max_len:
        firstpart, secondpart = paragraph[:len(paragraph) // 2], paragraph[len(paragraph) // 2:]
        first = split_larg_paragraphs(firstpart, max_len)
        second = split_larg_paragraphs(secondpart, max_len)
        return first + second
    else:
        return [paragraph]


class WikiParser:
    @staticmethod
    def add_passages(raw_docs: Documents):
        for doc in raw_docs:
            text = doc.text

            paragraphs = text.split('    ')
            for p_large in paragraphs[:-1]:
                for p in split_larg_paragraphs(p_large):
                    if p.strip() != "":
                        doc.add_passage(Passage(p, doc.elastic_score, doc))
