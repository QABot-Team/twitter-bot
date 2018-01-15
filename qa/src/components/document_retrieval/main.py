from models.documents import Documents
from models.question_model import QuestionModel
from components.document_retrieval.es_client import EsClient
from components.document_retrieval.wiki_parser import WikiParser
from utils.logger import Logger
from datetime import datetime, timedelta, time


def receive_docs(question_model: QuestionModel) -> Documents:
    # start logging
    Logger.info('started')
    start = datetime.now()

    # get documents by elastic search
    keywords = ' '.join(question_model.keywords)
    Logger.info('Query Keywords: ' + keywords)
    client = EsClient()
    raw_docs = client.search(keywords)

    # parse documents by Wiki MarkUp
    parser = WikiParser()
    docs = parser.parse_docs(raw_docs)

    # end logging
    end = datetime.now()
    diff = end - start
    Logger.info('finished (' + str(diff.seconds) + '.' + str(diff.microseconds) + ' s)')
    Logger.small_seperator()

    return docs
