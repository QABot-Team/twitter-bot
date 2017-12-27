from models.documents import Document, Documents

import re

EXCLUDES = ["(disambiguation)", "(surname)"]


class WikiParser:

    @staticmethod
    def parse_source_text(es_doc) -> Document:
        doc = Document(es_doc['title'], es_doc['text'])

        src = es_doc['source_text']
        headers = es_doc['heading']

        # remove xml comments
        src = re.sub(r'(<!--([\s]*|.)*-->)', '', src)
        # remove references
        # src = re.sub(r'(<ref>.*</ref>)', '', src)

        # parse info box
        ib_start = src.lower().find("{{infobox")
        if ib_start >= 0:
            count_opened = 2
            count_closed = 0
            ib_end = ib_start + 9
            while count_closed != count_opened:
                char = src[ib_end:ib_end + 1]
                if char == "{":
                    count_opened += 1
                elif char == "}":
                    count_closed += 1
                ib_end += 1

            doc.set_infobox(src[ib_start:ib_end])
            src = src[:ib_start] + src[ib_end + 1:]

        # parse short description
        sd_start = src.find("'''")
        sd_end = src.find("==", sd_start)
        if sd_end > sd_start:
            short_desc = src[sd_start:sd_end - 2]
            src = src.replace(short_desc, "")
            doc.set_sort_desc(short_desc)

        # parse paragraphs
        for header in headers:
            hdr = "=== " + header.strip() + " ==="
            pos_start = src.find(hdr)
            pos_end = src.find("===", pos_start + len(hdr))
            if pos_start > 0:
                paragraph = src[pos_start:pos_end]
                doc.add_passage(paragraph)
                src = src.replace(paragraph, "")

        return doc

    def parse_docs(self, raw_docs: list) -> Documents:
        docs = Documents()
        for doc in raw_docs:
            docs.add(self.parse_source_text(doc))

        return docs
