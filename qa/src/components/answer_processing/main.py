from components.answer_processing.bidaf import AnswerPredictor
from models.passages import Passages
from models.qp_result import QPResult
from utils.logger import Logger
from datetime import datetime

from utils.nlptoolkit import NLPToolkit

TOP_N_PASSAGES = 10


def prediction_pipeline(passages: Passages, question: str, nlp_toolkit: NLPToolkit):
    predictor = AnswerPredictor(nlp_toolkit)
    predictions = []
    for passage in passages.passages[:TOP_N_PASSAGES]:
        if passage.text:
            prediction = predictor.predict(passage.text, question)
            predictions.append(prediction)
    return predictions


def get_best_answer(predictions):
    best_answer = ''
    best_confidence = -1
    for prediction in predictions:
        answer = prediction['answer']
        confidence = prediction['confidence']
        print(answer + ' with confidence: ' + str(confidence))
        if confidence > best_confidence:
            best_confidence = confidence
            best_answer = answer
    return best_answer


def process_answer(passages: Passages, qp_result: QPResult, nlp_toolkit: NLPToolkit) -> str:
    # start logging
    Logger.info('started')
    start = datetime.now()

    predictions = prediction_pipeline(passages, qp_result.question_model.question, nlp_toolkit)
    result = get_best_answer(predictions)

    # end logging
    end = datetime.now()
    diff = end - start
    Logger.info('finished (' + str(diff.seconds) + '.' + str(diff.microseconds)[0:2] + ' s)')
    Logger.small_seperator()

    return result
