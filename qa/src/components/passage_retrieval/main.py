from models.Passages import Passages
from models.documents import Documents
from models.question_model import QuestionModel


def receive_passages(docs: Documents, question_model: QuestionModel) -> Passages:
    return Passages([docs.docs[0].title])
