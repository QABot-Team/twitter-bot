from models.documents import Documents
from models.question_model import QuestionModel
from components.document_retrieval.esClient import EsClient
from utils.logger import Logger


def receive_docs(question_model: QuestionModel) -> Documents:
    Logger.info('started')
    client = EsClient()
    result = client.search(' '.join(question_model.keywords))
    Logger.info('finished')
    return result
