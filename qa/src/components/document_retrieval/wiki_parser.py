from models.documents import Document, Documents

import re

EXCLUDES = ["(disambiguation)", "(surname)"]


class WikiParser:

    @staticmethod
    def parse_source_text(doc: Document, src: str, headers: []) -> Document:
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

        # remove everything in double curly braces (e.g. {{Text}}) - do we have curly braces inside the text ??
        # src = re.sub(r'{{([^(}})]*)}}', '', src)

        # parse paragraphs
        for header in headers:
            hdr = "=== " + header.strip() + " ==="
            match = re.search('===(\s?)' + header.strip() + '(\s?)===', src)
            pos_start = -1 if match is None else match.start()
            pos_end = src.find("==", pos_start + len(hdr))
            if pos_start > 0:
                paragraph = src[pos_start:pos_end]
                doc.add_passage(paragraph)
                src = src.replace(paragraph, "")

        return doc

    def remove_references(self, text):
        paragraphs = text.split('    ')
        return '    '.join(paragraphs[:-1])

    def parse_docs(self, raw_docs: list) -> Documents:
        docs = Documents()
        for es_doc in raw_docs:
            text = self.remove_references(es_doc['text'])
            doc = Document(es_doc['title'], text)
            src = es_doc['source_text']
            headers = es_doc['heading']
            docs.add(self.parse_source_text(doc, src, headers))

        return docs
