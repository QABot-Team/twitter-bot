import os
import sys
import json

DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.append(DIR + '/../../src')

from qa_process_impl import process_answer_question

from utils.logger import Logger
from utils.log_config import log_config


data = json.load(open(DIR + '/custom_data_set.json'))


def text_contains_any_answer(text, answers):
    for a in answers:
        if a['text'] in text:
            return True
    return False


def is_correct_article(title, correct_title) -> bool:
    if title == correct_title.replace("_", " "):
        return True
    else:
        return False


Logger.config('info')

Logger.info("Start document_retrieval analysis")

log_config()

question_counter = 0
correct_answers_counter = 0

for dataset in data['data']:
    title = dataset['title']
    Logger.info('Dataset: ' + title)

    for paragraph in dataset['paragraphs'][:5]:
        for question_answer_set in paragraph['qas']:
            question = question_answer_set['question']
            correct_answers = question_answer_set['answers']

            Logger.error("Dataset Title: " + title)
            Logger.error('')
            Logger.error(question)
            answer = process_answer_question(question)
            Logger.error("Answer: " + answer)
            Logger.error("Correct Answers: " + str(correct_answers))
            if text_contains_any_answer(answer, correct_answers):
                correct_answers_counter += 1

            question_counter += 1

            Logger.error('')
            Logger.error('')
            Logger.error('Right Answers: ' + str(correct_answers_counter) + " / " + str(question_counter))
            Logger.error('')
            Logger.error('############################################################################################')
            Logger.error('')
