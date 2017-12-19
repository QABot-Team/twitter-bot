from models.passages import Passages
from models.answer_type import AnswerType
from utils.logger import get_logger


def process_answer(passages: Passages, answer_type: AnswerType) -> str:
    get_logger().info('started')
    result = passages.get_passage_at(0).text
    get_logger().info('finished')
    return result
