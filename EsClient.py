from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
import json
from pprint import pprint
INDEX_NAME = "wiki"
class EsClient: 
  def __init__(self):
    self.client = Elasticsearch()

  def search(self, query):
    s = Search(using=self.client, index=INDEX_NAME) \
    .query("multi_match", query=query, fields=["title", "text"]) 
    response = s.execute()
    return self.parse_response(response)

  def parse_response(self, response):
    output = {"results": []}
    for hit in response:
      categories = [c.encode("utf-8") for c in hit.category]
      links = [l.encode("utf-8") for l in hit.link]
      print(links)
      output["results"].append({"metadata": hit.meta, "title": hit.title.encode("utf-8"), "text": hit.text.encode("utf-8"), "categories": categories, "link": links})
    return output


esclient = EsClient()
response = esclient.search("arnold")
print(response["results"][0])
