import xml.etree.cElementTree as etree
from elasticsearch import Elasticsearch
import json
import time

start_time = time.time()
PATH_WIKI_XML = '/var/qabot-team/wikidump/enwiki-20171001-pages-articles.xml'
#PATH_WIKI_XML = 'test.xml'
es = Elasticsearch(timeout=60, max_retries=10, retry_one_timeout=True)
for event, elem in etree.iterparse(PATH_WIKI_XML, events=('start', 'end')):
  #elem.tag example: {http://www.mediawiki.org/xml/export-0.10/}page
  #split string after first occurence of } to retrieve the name
  tag_name = elem.tag.split('}', 1)[1]
  if event == 'start':
    if tag_name == 'page':
      page = {}
      in_revision = False
    elif tag_name == 'revision':
      in_revision = True
  else:
    if tag_name == 'page':
      res = es.index(index='wikipedia', doc_type='wiki_page', body=json.dumps(page))
      print('Id: ' + str(page['id']) + ' ' + str(res['created']))
    elif tag_name == 'ns':
      page['ns'] = int(elem.text)
    elif tag_name == 'title':
      page['title'] = elem.text
    elif tag_name == 'id' and not in_revision:
      page['id'] = int(elem.text)
    elif tag_name == 'text':
      page['text'] = elem.text

elapsed_time = time.time() - start_time
print('Elapsed time: ' + time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))
