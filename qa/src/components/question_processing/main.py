from models.answer_type import AnswerType
from models.qp_result import QPResult
from models.question_model import QuestionModel
from utils.logger import Logger
from .fit_predict import get_clf_from_disk, get_predicted_label, get_clf_name, get_key_words


def process_question(question: str) -> QPResult:
    Logger.info('started')
    clf_name = get_clf_name(question)
    clf = get_clf_from_disk(clf_name)
    label = get_predicted_label(question, clf)
    keywords = get_key_words(question)
    # print(keywords)
    # print(AnswerType[label.upper()])
    Logger.info('finished')
    return QPResult(QuestionModel(keywords, question), AnswerType[label.upper()])
