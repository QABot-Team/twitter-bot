from models.answer_type import AnswerType
from models.qp_result import QPResult
from models.question_model import QuestionModel
from utils.nlptoolkit import NLPToolkit
from .fit_predict import get_clf_from_disk, get_predicted_label, get_clf_name


def process_question(question: str, nlp_toolkit: NLPToolkit) -> QPResult:
    question_keywords = nlp_toolkit.extract_stop_words(question)[1:]
    return QPResult(QuestionModel(question_keywords), AnswerType.ENTY)
    # clf_name = get_clf_name(question)
    # clf = get_clf_from_disk(clf_name)
    # label = get_predicted_label(question, clf)
    # return QPResult(QuestionModel(question.split()), AnswerType[label])
