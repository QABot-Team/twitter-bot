from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from utils.logger import Logger

INDEX_NAME = "enwiki"

TITLE_EXCLUDES = ["(surname)"]
REFER_TEXT = "may refer to"
CAT_EXCL = ["Disambiguation pages"]


class EsClient:
    def __init__(self):
        self.client = Elasticsearch()

    def search(self, query) -> list:
        s = Search(using=self.client, index=INDEX_NAME) \
            .query("multi_match", query=query, fields=["title^5", "text"])  # boost title by 5
        response = s.execute()

        docs = []
        for idx, doc in enumerate(response):
            if not any(excl in doc.title for excl in TITLE_EXCLUDES) and \
               not any(excl in doc.category for excl in CAT_EXCL) and \
               REFER_TEXT not in doc.text:
                doc.text = str(str(doc.text).encode('utf-8'))
                doc.title = str(str(doc.title).encode('utf-8'))
                docs.append(doc)
                Logger.info('Document ' + str(idx) + ": \"" + doc.title + '\"' +
                            ' Scoring: ' + str(doc.meta.score) +
                            ' Populairty: ' + str(doc.popularity_score))
        return docs
