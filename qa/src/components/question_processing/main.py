from models.answer_type import AnswerType
from models.qp_result import QPResult
from models.question_model import QuestionModel
from .fit_predict import get_clf_from_disk, get_predicted_label, get_clf_name


def process_question(question: str) -> QPResult:
    clf_name = get_clf_name(question)
    clf = get_clf_from_disk(clf_name)
    label = get_predicted_label(question, clf)
    return QPResult(QuestionModel(question.split()), AnswerType[label.upper()])
