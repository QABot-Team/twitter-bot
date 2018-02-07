from components.passage_retrieval.our_tfidf.tfidf_ranker import TfIdfRanker
from models.passage import Passage
from models.passages import Passages
from models.documents import Documents
from models.qp_result import QPResult
from utils.logger import Logger
from utils.nlptoolkit import NLPToolkit
from components.passage_retrieval.passage_classifier import get_most_similar
from components.passage_retrieval.filter_passages import filter_passages
from datetime import datetime


def receive_passages(docs: Documents, qp_result: QPResult, nlp_toolkit: NLPToolkit) -> Passages:
    # start logging
    Logger.info('started')
    start = datetime.now()
    passages = Passages()
    
    # we use the first document
    for doc in docs.docs:
        passages.add(Passage(doc))

    end = datetime.now()
    diff = end - start
    Logger.info('finished (' + str(diff.seconds) + '.' + str(diff.microseconds) + ' s)')
    Logger.small_seperator()

    return passages
