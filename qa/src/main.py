import sys
from qa_process_impl import process_answer_question

if len(sys.argv) != 2:
    print('usage python ' + sys.argv[0] + ' <question>')
else:
    question = sys.argv[1]

    answer = process_answer_question(question)
    print(answer)
