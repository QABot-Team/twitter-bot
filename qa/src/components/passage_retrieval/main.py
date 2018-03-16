from datetime import datetime

from prettytable import PrettyTable

from components.passage_retrieval.our_tfidf.tfidf_ranker import TfIdfRanker
from config import TOP_N_DOCS, TOP_N_PASSAGES
from models.passages import Passages
from models.documents import Documents
from models.qp_result import QPResult
from utils.logger import Logger
from utils.nlptoolkit import NLPToolkit
from utils.scorer import Scorer


def log_passages(passages: Passages):
    table = PrettyTable(['Id', 'Passage', 'Score'])
    format_num = lambda x: '{0:.2f}'.format(x)
    for passage in passages.passages[:TOP_N_PASSAGES]:
        text = passage.text if len(passage.text) < 61 else passage.text[:60] + '...'
        table.add_row([passage.get_id(), text, format_num(passage.tfidf_score)])
    Logger.info('Tf.idf result:\n' + str(table))


def receive_passages(docs: Documents, qp_result: QPResult, nlp_toolkit: NLPToolkit) -> Passages:
    # start logging
    Logger.info('started')
    start = datetime.now()

    # Rank passages of the TOP_N_DOC documents with tfidf
    passages = Passages()

    for doc in docs.docs[:TOP_N_DOCS]:
        for p in doc.passages:
            passages.add(p)
    tfidf = TfIdfRanker(nlp_toolkit.remove_stop_words)
    ranked_passages = tfidf.calc_passage_ranks(passages, qp_result.question_model)
    log_passages(ranked_passages)
    Logger.info('#Passages: ' + str(len(ranked_passages.passages)) + ' considering ' + str(TOP_N_PASSAGES))
    scorer = Scorer()
    scorer.min_max_norm(ranked_passages)

    end = datetime.now()
    diff = end - start
    Logger.info('finished (' + str(diff.seconds) + '.' + str(diff.microseconds) + ' s)')
    Logger.small_seperator()

    return ranked_passages
