

def answer_question(question, process_question, receive_docs, receive_passages, process_answer):
    qp_result = process_question(question)
    docs = receive_docs(qp_result.question_model)
    passages = receive_passages(docs)
    return process_answer(passages, qp_result.answer_type)
