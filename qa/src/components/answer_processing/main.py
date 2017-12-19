from models.passages import Passages
from models.answer_type import AnswerType
from utils.logger import Logger


def process_answer(passages: Passages, answer_type: AnswerType) -> str:
    Logger.info('started')
    result = passages.get_passage_at(0).text
    Logger.info('finished')
    return result
