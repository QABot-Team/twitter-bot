def answer_question(question, process_question, receive_docs, receive_passages, process_answer, nlp_toolkit):
    qp_result = process_question(question)
    docs = receive_docs(qp_result.question_model)
    passages = receive_passages(docs, qp_result.question_model, nlp_toolkit)
    return process_answer(passages, qp_result.answer_type)
