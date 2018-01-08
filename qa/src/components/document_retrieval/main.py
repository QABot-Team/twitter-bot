from models.documents import Documents
from models.question_model import QuestionModel
from components.document_retrieval.es_client import EsClient
from components.document_retrieval.wiki_parser import WikiParser
from utils.logger import Logger


def receive_docs(question_model: QuestionModel) -> Documents:
    Logger.info('started')
    client = EsClient()
    raw_docs = client.search(' '.join(question_model.keywords))

    parser = WikiParser()
    docs = parser.parse_docs(raw_docs)

    Logger.info('finished')
    return docs
