import unittest

from models.passages import Passages
from models.answer_type import AnswerType
from models.documents import Documents
from models.qp_result import QPResult
from models.question_model import QuestionModel
from qa_process import answer_question


def process_question(question: str, nlp_toolkit):
    if not isinstance(question, str):
        raise Exception("process_question expects parameter of type str")
    return QPResult(QuestionModel([], ""), AnswerType.HUM_ind)


def receive_docs(question_model: QuestionModel, nlp_toolkit):
    if not isinstance(question_model, QuestionModel):
        raise Exception("receive_docs expects parameter of type QuestionModel")
    return Documents()


def receive_passages(docs: Documents, question_model: QuestionModel, nlp_toolkit):
    if not isinstance(docs, Documents):
        raise Exception("receive_passages expects parameter of type Documents")
    return Passages()


def process_answer(passages: Passages, answer_type: AnswerType):
    if not isinstance(passages, Passages):
        raise Exception("process_answer expects parameter of type Passages")
    if not isinstance(answer_type, AnswerType):
        raise Exception("process_answer expects parameter of type AnswerType")
    return 'amazing answer'


class TestQAProcess(unittest.TestCase):

    def test_process_pipeline(self):
        answer = answer_question(
            'strange question', process_question, receive_docs, receive_passages, process_answer, None)
        self.assertEqual(answer, 'amazing answer')


if __name__ == '__main__':
    unittest.main()
