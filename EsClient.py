from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
INDEX_NAME = "wiki"
class EsClient: 
  def __init__(self):
    self.client = Elasticsearch()

  def search(self, title_match, text_match, exclude_title, exclude_text, search_filter):
    s = Search(using=self.client, index=INDEX_NAME) \
    .query("match", title=title_match, text=text_match)   \
    .exclude("match", title=exclude_title, text=exclude_text)

    return s.execeute()

esclient = EsClient()
print(esclient.search("arnold", "arnold", "", "", ""))