from components.answer_processing import process_answer
from components.document_retrieval import receive_docs
from components.passage_retrieval import receive_passages
from components.question_processing import process_question
from qa_process import answer_question
from utils.nlptoolkit import NLPToolkit
from utils.logger import get_logger


def process_answer_question(question):
    nlp_toolkit = NLPToolkit()
    get_logger().info('Start answer processing pipeline')
    answer = answer_question(question, process_question, receive_docs, receive_passages, process_answer, nlp_toolkit)
    get_logger().info('Finished answer processing pipeline')
    return answer
