from models.passages import Passages
from models.answer_type import AnswerType
from utils.logger import Logger
from datetime import datetime


def process_answer(passages: Passages, answer_type: AnswerType) -> str:
    # start logging
    Logger.info('started')
    start = datetime.now()

    # start answer processing
    result = passages.get_passage_at(0).text

    # end logging
    end = datetime.now()
    diff = end - start
    Logger.info('finished (' + str(diff.seconds) + '.' + str(diff.microseconds)[0:2] + ' s)')
    Logger.small_seperator()

    return result
