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

    # we use the first document
    # doc = docs.get_doc_with_highest_rank()
    doc_sections = []
    for doc in docs.docs:
        _sections = nlp_toolkit.text_to_sentences(str(doc.text))
        doc_sections += _sections
    doc_sections = set(doc_sections)
    doc_sections = list(doc_sections)
    doc_sections = filter_passages(doc_sections, qp_result.answer_type, nlp_toolkit)
    # doc_sections = nlp_toolkit.text_to_sentences(str(doc.text))
    # get_passage(doc_sections, ' '.join(question_model.keywords))
    most_similar = get_most_similar(doc_sections, qp_result.question_model.question, nlp_toolkit)
    passages = Passages()
    passages.add(Passage(most_similar))

    # passages = Passages()
    # for section in doc_sections:
    #    passages.add(Passage(section))

    # tfidf = TfIdfRanker(nlp_toolkit.remove_stop_words)
    # ranked_passages = tfidf.calc_passage_ranks(passages, qp_result.question_model)

    # end logging
    end = datetime.now()
    diff = end - start
    Logger.info("Answer from PassageClf: " + most_similar)
    # Logger.info("Answer from tf.idf: " + ranked_passages.get_passage_at(0).text)
    Logger.info('finished (' + str(diff.seconds) + '.' + str(diff.microseconds) + ' s)')
    Logger.small_seperator()

    return passages
