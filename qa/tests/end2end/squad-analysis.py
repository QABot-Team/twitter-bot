import os
import sys
import json

DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.append(DIR + '/../../src')


from qa_process_impl import process_answer_question

data = json.load(open('dev-v1.1.json'))


def text_contains_any_answer(text, answers):
    for a in answers:
        if a['text'] in text:
            return True
    return False


print("Start analysis")

question_counter = 0
correct_answers_counter = 0

for dataset in data['data']:
    title = dataset['title']
    print('Dataset: ' + title)

    for paragraph in dataset['paragraphs'][:5]:
        for question_answer_set in paragraph['qas']:
            question_counter += 1
            question = question_answer_set['question']
            correct_answers = question_answer_set['answers']
            print(question)

            answer = process_answer_question(question)

            print(answer)
            print(correct_answers)
            if text_contains_any_answer(answer, correct_answers):
                correct_answers_counter += 1
            print(str(correct_answers_counter) + " / " + str(question_counter))
            print()
            print()
