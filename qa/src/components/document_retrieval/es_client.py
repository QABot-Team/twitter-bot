from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from prettytable import PrettyTable

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

        table = PrettyTable(['Index', 'Title', 'Score', 'Popularity'])
        docs = Documents()
        skip_count = 0
        for idx, doc in enumerate(response):
            if not any(excl in doc.title for excl in TITLE_EXCLUDES) and \
               not any(excl in doc.category for excl in CAT_EXCL) and \
               REFER_TEXT not in doc.text:
                # uft encode values
                doc.title = str.encode(doc.title, encoding='utf-8').decode(encoding='utf-8')
                doc.text = str.encode(doc.text, encoding='utf-8').decode(encoding='utf-8')

                docs.add(Document(doc.title, doc.text, doc.meta.score))
                format_num = lambda x: '{0:.2f}'.format(x)
                table.add_row([idx, doc.title, format_num(doc.meta.score), doc.popularity_score])
            else:
                skip_count += 1
        Logger.info('Elastic result:\n' + str(table))
        Logger.info(str(skip_count) + ' elastic results were skipped')
        return docs
