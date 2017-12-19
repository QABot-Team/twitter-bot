from models.documents import Documents
from models.question_model import QuestionModel
from components.document_retrieval.esClient import EsClient
from utils.logger import get_logger


def receive_docs(question_model: QuestionModel) -> Documents:
    get_logger().info('started')
    client = EsClient()
    result = client.search(' '.join(question_model.keywords))
    get_logger().info('finished')
    return result
