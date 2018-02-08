import os
import sys
import json

from components.answer_processing.bidaf import AnswerPredictor
from components.passage_retrieval import receive_passages
from models.answer_type import AnswerType
from models.document import Document
from models.documents import Documents
from models.qp_result import QPResult
from models.question_model import QuestionModel
from utils.nlptoolkit import NLPToolkit

DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.append(DIR + '/../../src')


from utils.logger import Logger

data = json.load(open('dev-v1.1.json'))


def text_contains_any_answer(text, answers):
    for a in answers:
        if a['text'] in text:
            return True
    return False


Logger.config('info')

Logger.info("Start analysis")

question_counter = 0
correct_answers_counter = 0

nlptoolkit = NLPToolkit()

for dataset in data['data']:
    title = dataset['title']
    Logger.info('Dataset: ' + title)

    for paragraph in dataset['paragraphs'][:5]:
        context = paragraph['context']
        for question_answer_set in paragraph['qas']:
            question_counter += 1
            question = question_answer_set['question']
            correct_answers = question_answer_set['answers']
            Logger.info(question)

            doc = Document(title, context)
            docs = Documents()
            docs.add(doc)

            answer_predictor = AnswerPredictor(NLPToolkit())
            result = answer_predictor.predict(context, question)

            answer = result['answer']

            Logger.info(answer)
            Logger.info(correct_answers)
            if text_contains_any_answer(answer, correct_answers):
                correct_answers_counter += 1
            Logger.info("Result: " + str(correct_answers_counter) + " / " + str(question_counter))
            Logger.info('')
            Logger.info('')
