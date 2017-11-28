from models.answer_type import AnswerType
from models.question_model import QuestionModel


class QPResult:
    def __init__(self, question_model: QuestionModel, answer_type: AnswerType) -> None:
        self.question_model = question_model
        self.answer_type = answer_type
