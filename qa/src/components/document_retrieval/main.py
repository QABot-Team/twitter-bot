from models.documents import Documents
from models.question_model import QuestionModel
from components.document_retrieval.esClient import EsClient

def receive_docs(question_model: QuestionModel) -> Documents:
    client = EsClient()
    return client.search(' '.join(question_model.keywords))
