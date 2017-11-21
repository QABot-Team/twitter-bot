import sys

from components.answer_processing import process_answer
from components.document_retrieval import receive_docs
from components.passage_retrieval import receive_passages
from components.question_processing import process_question
from qa_process import answer_question

if len(sys.argv) != 2:
    print('usage python ' + sys.argv[0] + ' <question>')
else:
    question = sys.argv[1]
    answer = answer_question(question, process_question, receive_docs, receive_passages, process_answer)
    print(answer)
