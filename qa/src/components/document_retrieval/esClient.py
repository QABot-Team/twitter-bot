from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from models.document import Document
from models.documents import Documents
import re

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
            self.parse_source_text(hit.source_text.encode("utf-8"), hit.heading)
            documents.add(Document(hit.title.encode("utf-8"), hit.text.encode("utf-8")))
            print(hit.source_text.encode("utf-8"))
        return documents

    def parse_source_text(self, source_text, heading):
        output = ""
        fobj_out = open("log1.txt", "w")
        #array = re.split('{{([^}]+)}}', str(source_text))
        array = str(source_text).split('{{')
        for i in range(0, len(array)):
            results = array[i].split('}}')
            if len(results) == 2:
                #fobj_out.write(str(self.cut_refs(results[1])) + "\n")
                output += str(self.cut_refs(results[1])) + "\n"
            elif len(results) == 1:
               #fobj_out.write(str(self.cut_refs(results[0])) + "\n")
                output += str(self.cut_refs(results[0])) + "\n"
            elif len(results) == 3:
                #fobj_out.write(str(self.cut_refs(results[2])) + "\n")
                output += str(self.cut_refs(results[2])) + "\n"
        results = self.split_headings(output, heading)
        for r in results:
            fobj_out.write(r + "\n\n\n\n")
        #print(output)

    def cut_refs(self, string):
        result = string
        data = string.split("</ref>")
        if len(data) > 1:
            result = data[1]
        result = result.split("<ref>")[0]
        data = result.split("[[")
        result = ""
        for d in data:
            result += d
        data = result.split("]]")
        result = ""
        for d in data:
            result += d
        return result

    def split_headings(self, text, heading):
        results = []
        for h in heading:
            data = text.split("==" + str(h) + "==")
            results.append(data[0])
            if len(data) > 1:
                text = data[1]
            else:
                text = data[0]
        return results


esclient = EsClient()
response = esclient.search("arnold schwarzenegger")
