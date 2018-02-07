from datetime import datetime

from models.passage import Passage
from models.passages import Passages
from models.documents import Documents
from models.qp_result import QPResult
from utils.logger import Logger
from utils.nlptoolkit import NLPToolkit
from components.passage_retrieval.filter_passages import filter_passages
from components.passage_retrieval.preprocessing_pipeline import preprocessing_pipeline


def receive_passages(docs: Documents, qp_result: QPResult, nlp_toolkit: NLPToolkit) -> Passages:
    # start logging
    Logger.info('started')
    start = datetime.now()
    passages = Passages()
    
    processed_docs = preprocessing_pipeline(docs, qp_result, nlp_toolkit)
    for doc in processed_docs:
        passages.add(Passage(doc))
        

    end = datetime.now()
    diff = end - start
    Logger.info('finished (' + str(diff.seconds) + '.' + str(diff.microseconds) + ' s)')
    Logger.small_seperator()

    return passages
