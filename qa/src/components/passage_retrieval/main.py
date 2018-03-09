from datetime import datetime

from components.passage_retrieval.our_tfidf.tfidf_ranker import TfIdfRanker
from config import TOP_N_DOCS
from models.passages import Passages
from models.documents import Documents
from models.qp_result import QPResult
from utils.logger import Logger
from utils.nlptoolkit import NLPToolkit
from utils.scorer import Scorer


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
    Logger.info('#Passages: ' + str(len(ranked_passages.passages)))
    scorer = Scorer()
    scorer.min_max_norm(ranked_passages)

    end = datetime.now()
    diff = end - start
    Logger.info('finished (' + str(diff.seconds) + '.' + str(diff.microseconds) + ' s)')
    Logger.small_seperator()

    return ranked_passages
