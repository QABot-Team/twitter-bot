from models.answer_type import AnswerType
from models.qp_result import QPResult
from models.question_model import QuestionModel


def process_question(question: str) -> QPResult:
    return QPResult(QuestionModel([]), AnswerType.PERSON)
