from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from utils.logger import Logger
from models.documents import Documents
from models.document import Document

INDEX_NAME = "enwiki"

TITLE_EXCLUDES = ["(disambiguation)", "(surname)"]
REFER_TEXT = "may refer to"
CAT_EXCL = ["Disambiguation pages"]


class EsClient:
    def __init__(self):
        self.client = Elasticsearch()

    def search(self, query) -> Documents:
        s = Search(using=self.client, index=INDEX_NAME) \
            .query("multi_match", query=query, fields=["title^5", "text"])  # boost title by 5
        response = s.execute()

        docs = Documents()
        for idx, doc in enumerate(response):
            if not any(excl in doc.title for excl in TITLE_EXCLUDES) and \
               not any(excl in doc.category for excl in CAT_EXCL) and \
               REFER_TEXT not in doc.text:
                # uft encode values
                doc.title = str.encode(doc.title, encoding='utf-8').decode(encoding='utf-8')
                doc.text = str.encode(doc.text, encoding='utf-8').decode(encoding='utf-8')

                docs.add(Document(doc.title, doc.text, doc.meta.score))
                Logger.info('Document ' + str(idx) + ": \"" + doc.title + '\"' +
                            ' Scoring: ' + str(doc.meta.score) +
                            ' Populairty: ' + str(doc.popularity_score))
        return docs
