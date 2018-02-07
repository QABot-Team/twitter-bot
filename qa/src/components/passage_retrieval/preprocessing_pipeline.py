from components.passage_retrieval.filter_passages import filter_passages
from models.documents import Documents
from models.qp_result import QPResult
from utils.nlptoolkit import NLPToolkit


def preprocessing_pipeline(docs: Documents, qp_result: QPResult, nlp_toolkit: NLPToolkit):
    # preprocessing pipeline:
    # 1: split docs in sentences
    # 2: filter sentences

    processed_docs = []
    # we use all docs in the moment and evaluate based on the probability distribution available through softmax
    for doc in docs.docs:
        sentences = nlp_toolkit.text_to_sentences(doc.text)
        filtered_sentences = \
            [sentence for sentence in sentences if filter_passages(sentence, qp_result.answer_type, nlp_toolkit)]
        processed_docs.append(' '.join(filtered_sentences))

    return processed_docs
