from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
import json
from pprint import pprint

from qa.src.models.document import Document
from qa.src.models.documents import Documents

INDEX_NAME = "enwiki"


class EsClient:
    def __init__(self):
        self.client = Elasticsearch()

    def search(self, query) -> Documents:
        s = Search(using=self.client, index=INDEX_NAME) \
            .query("multi_match", query=query, fields=["title", "text"])
        response = s.execute()
        return self.parse_response(response)

    def parse_response(self, response) -> Documents:
        documents = Documents()
        for hit in response:
            documents.add(Document(hit.title.encode("utf-8"), hit.text.encode("utf-8")))
        return documents

    def dummy_response(self) -> Documents:
        docs = Documents()
        docs.add(Document("Arnold Schwarzenegger", " "))
        return docs


esclient = EsClient()
response = esclient.search("arnold")
print(response[0].text)
