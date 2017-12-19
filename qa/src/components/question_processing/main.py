from models.answer_type import AnswerType
from models.qp_result import QPResult
from models.question_model import QuestionModel
from utils.logger import get_logger
from .fit_predict import get_clf_from_disk, get_predicted_label, get_clf_name


def process_question(question: str) -> QPResult:
    get_logger().info('started')
    clf_name = get_clf_name(question)
    clf = get_clf_from_disk(clf_name)
    label = get_predicted_label(question, clf)
    get_logger().info('finished')
    return QPResult(QuestionModel(question.split()), AnswerType[label.upper()])
