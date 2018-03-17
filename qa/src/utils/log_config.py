from prettytable import PrettyTable

from config import ELASTIC_WEIGHT, TFIDF_WEIGHT, PASSAGE_WEIGHT, BIDAF_WEIGHT, TOP_N_PASSAGES, TOP_N_DOCS, \
    SCORE_FOR_BEST_ANSWER, USE_ANSWER_TYPE
from utils.logger import Logger


def log_config():
    table = PrettyTable(['Key', 'Value'])
    table.add_row(['ELASTIC_WEIGHT', ELASTIC_WEIGHT])
    table.add_row(['TFIDF_WEIGHT', TFIDF_WEIGHT])
    table.add_row(['PASSAGE_WEIGHT', PASSAGE_WEIGHT])
    table.add_row(['BIDAF_WEIGHT', BIDAF_WEIGHT])
    table.add_row(['TOP_N_PASSAGES', TOP_N_PASSAGES])
    table.add_row(['TOP_N_DOCS', TOP_N_DOCS])
    table.add_row(['SCORE_FOR_BEST_ANSWER', SCORE_FOR_BEST_ANSWER])
    table.add_row(['USE_ANSWER_TYPE', str(USE_ANSWER_TYPE)])
    Logger.info('Configuration:\n' + str(table) + '\n')
