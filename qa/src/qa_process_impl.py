from components.answer_processing import process_answer
from components.document_retrieval import receive_docs
from components.passage_retrieval import receive_passages
from components.question_processing import process_question
from qa_process import answer_question
from utils.nlptoolkit import NLPToolkit
from utils.logger import Logger
from datetime import datetime

nlp_toolkit = NLPToolkit()


def process_answer_question(question):

    # start logging
    Logger.big_seperator()
    Logger.info('Start answer processing pipeline')
    Logger.info('Question: ' + question)
    start = datetime.now()

    answer = answer_question(question, process_question, receive_docs, receive_passages, process_answer, nlp_toolkit)

    # end logging
    end = datetime.now()
    diff = end - start
    Logger.info('Finished answer processing pipeline (' + str(diff.seconds) + '.' + str(diff.microseconds) + ' s)')
    return answer
