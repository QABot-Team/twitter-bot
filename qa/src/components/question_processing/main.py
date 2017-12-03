from models.answer_type import AnswerType
from models.qp_result import QPResult
from models.question_model import QuestionModel
from .fit_predict import get_clf_from_disk, get_predicted_label, SVM_CLF_NAME

def process_question(question: str) -> QPResult:
    clf = get_clf_from_disk(SVM_CLF_NAME)
    label = get_predicted_label(question, clf)
    return QPResult(QuestionModel(question.split()), AnswerType[label])
