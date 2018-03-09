from models.documents import Documents
from models.question_model import QuestionModel
from components.document_retrieval.es_client import EsClient
from components.document_retrieval.wiki_parser import WikiParser
from utils.logger import Logger
from datetime import datetime
from utils.nlptoolkit import NLPToolkit
from utils.scorer import Scorer


def receive_docs(question_model: QuestionModel, nlp_toolkit: NLPToolkit) -> Documents:
    # start logging
    Logger.info('started')
    start = datetime.now()

    # get documents by elastic search
    keywords = ' '.join(question_model.keywords)
    Logger.info('Query Keywords: ' + keywords)
    client = EsClient()
    docs = client.search(keywords)

    # min-max-normalization of elastic score
    scorer = Scorer()
    scorer.min_max_norm(docs)

    # parse documents by Wiki MarkUp
    parser = WikiParser()
    parser.add_passages(docs)

    # end logging
    end = datetime.now()
    diff = end - start
    Logger.info('finished (' + str(diff.seconds) + '.' + str(diff.microseconds) + ' s)')
    Logger.small_seperator()

    return docs
