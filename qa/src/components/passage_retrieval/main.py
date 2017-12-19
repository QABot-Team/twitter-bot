from components.passage_retrieval.our_tfidf.tfidf_ranker import TfIdfRanker
from models.passage import Passage
from models.passages import Passages
from models.documents import Documents
from models.question_model import QuestionModel
from utils.logger import get_logger
from utils.nlptoolkit import NLPToolkit


def receive_passages(docs: Documents, question_model: QuestionModel, nlp_toolkit: NLPToolkit) -> Passages:
    get_logger().info('started')
    # we use the first document
    doc = docs.get_doc_with_highest_rank()
    doc_sections = nlp_toolkit.text_to_sentences(str(doc.text))
    passages = Passages()
    for section in doc_sections:
        passages.add(Passage(section))

    tfidf = TfIdfRanker(nlp_toolkit.extract_stop_words)
    ranked_passages = tfidf.calc_passage_ranks(passages, question_model)

    get_logger().info('finished')
    return ranked_passages
