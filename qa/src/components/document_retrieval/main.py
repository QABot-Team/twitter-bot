from models.documents import Documents
from models.question_model import QuestionModel
from components.document_retrieval.es_client import EsClient
from components.document_retrieval.wiki_parser import WikiParser


def receive_docs(question_model: QuestionModel) -> Documents:
    client = EsClient()
    raw_docs = client.search(' '.join(question_model.keywords))

    parser = WikiParser()
    docs = parser.parse_docs(raw_docs)

    return docs
