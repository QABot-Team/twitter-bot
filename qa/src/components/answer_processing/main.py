from datetime import datetime

from prettytable import PrettyTable

from components.answer_processing.bidaf import AnswerPredictor
from components.passage_retrieval.filter_passages import filter_passages
from config import TOP_N_PASSAGES, SCORE_FOR_BEST_ANSWER, USE_ANSWER_TYPE
from models.answer_type import AnswerType
from models.passages import Passages
from models.prediction import Prediction
from models.predictions import Predictions
from models.qp_result import QPResult
from utils.logger import Logger
from utils.nlptoolkit import NLPToolkit
from utils.scorer import Scorer


def prediction_pipeline(passages: Passages, question: str, nlp_toolkit: NLPToolkit) -> Predictions:
    predictor = AnswerPredictor(nlp_toolkit)
    predictions = Predictions()
    for index, passage in enumerate(passages.passages[:TOP_N_PASSAGES]):
        if passage.text:
            Logger.debug('Send (passage,question) to bidaf: (' + passage.text + ',' + question + ')')
            pred = predictor.predict(passage.text, question)
            prediction = Prediction(
                pred['answer'],
                pred['context'],
                passage.parent_doc.title,
                passage.elastic_score,
                passage.tfidf_score,
                passage.get_passage_score(),
                pred['confidence']
            )
            predictions.add(prediction)
    scorer = Scorer()
    scorer.min_max_norm(predictions)
    return predictions


def filter_predictions(predictions: Predictions, answer_type: AnswerType, nlp_toolkit: NLPToolkit):
    return [pred for pred in predictions if filter_passages(pred.context, answer_type, nlp_toolkit)]


def setup_table():
    table = PrettyTable(['Answer', 'doc-title', 'elastic-score', 'tfidf-score', 'passage_rank', 'bidaf-score',
                         'final-score'])
    return table


def print_prediction(prediction: Prediction, table):
    answer = prediction.answer
    answer = answer if len(answer) < 21 else answer[:20] + '...'
    doc_title = prediction.doc_title
    elastic_score = prediction.elastic_score
    tfidf_score = prediction.tfidf_score
    passage_score = prediction.passage_score
    bidaf_score = prediction.bidaf_score
    final_score = prediction.calc_final_score()
    format_num = lambda x: '{0:.2f}'.format(x)
    table.add_row([answer, doc_title, format_num(elastic_score), format_num(tfidf_score), format_num(passage_score),
                   format_num(bidaf_score), format_num(final_score)])


def get_best_answer(predictions: Predictions):
    best_answer = ''
    best_score = -1
    table = setup_table()
    for prediction in predictions:
        answer = prediction.answer
        if SCORE_FOR_BEST_ANSWER == 'bidaf':
            score = prediction.bidaf_score
        elif SCORE_FOR_BEST_ANSWER == 'final-score':
            score = prediction.calc_final_score()
        else:
            raise EnvironmentError('invalid-config: SCORE_FOR_BEST_ANSWER unknown')
        print_prediction(prediction, table)
        if score > best_score:
            best_score = score
            best_answer = answer
    Logger.info('Predictions:\n' + str(table))
    return best_answer


def process_answer(passages: Passages, qp_result: QPResult, nlp_toolkit: NLPToolkit) -> str:
    # start logging
    Logger.info('started')
    start = datetime.now()

    predictions = prediction_pipeline(passages, qp_result.question_model.question, nlp_toolkit)
    if USE_ANSWER_TYPE:
        predictions = filter_predictions(predictions, qp_result.answer_type, nlp_toolkit)
    result = get_best_answer(predictions)

    # end logging
    end = datetime.now()
    diff = end - start
    Logger.info('finished (' + str(diff.seconds) + '.' + str(diff.microseconds)[0:2] + ' s)')
    Logger.small_seperator()

    return result
