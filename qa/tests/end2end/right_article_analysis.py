import os
import sys
import json

DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.append(DIR + '/../../src')

from qa_process_impl import process_answer_question

from utils.logger import Logger

from components.document_retrieval.main import receive_docs

from utils.nlptoolkit import NLPToolkit
from models.question_model import QuestionModel
from components.question_processing.main import process_question
from components.passage_retrieval.main import receive_passages
from components.answer_processing.main import process_answer

#data = json.load(open('dev-v1.1.json'))
data = json.load(open('custom_data_set.json'))


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


Logger.config('error')

Logger.info("Start document_retrieval analysis")

nlpToolkit = NLPToolkit()
question_counter = 0
correct_article_counter = 0
correct_firstArticle_counter = 0
correct_secondArticle_counter = 0
correct_thirdArticle_counter = 0
correct_answers_counter = 0

for dataset in data['data']:
    title = dataset['title']
    Logger.info('Dataset: ' + title)

    for paragraph in dataset['paragraphs'][:5]:
        for question_answer_set in paragraph['qas']:
            question_counter += 1
            question = question_answer_set['question']
            correct_answers = question_answer_set['answers']

            Logger.error(question)
            qp_result = process_question(question)
            #question_model = QuestionModel(nlpToolkit.get_key_words(question), question)
            question_model = qp_result.question_model
            docs = receive_docs(question_model)
            Logger.error("Dataset Title: " + title)
            for idx, doc in enumerate(docs.docs[:3]):
                isCorrectTitle = is_correct_article(doc.title, title)
                if isCorrectTitle:
                    Logger.error("Article found on Index: " + str(idx) + ": " + doc.title)
                    correct_article_counter += 1
                    passages = receive_passages(docs, qp_result, nlpToolkit)
                    answer = process_answer(passages, qp_result.answer_type)
                    Logger.error('')
                    Logger.error('Antwort: ' + answer)
                    Logger.error('')
                    if text_contains_any_answer(answer, correct_answers):
                        correct_answers_counter += 1

                    if idx == 0:
                        correct_firstArticle_counter += 1
                    elif idx == 1:
                        correct_secondArticle_counter += 1
                    elif idx == 2:
                        correct_thirdArticle_counter += 1
                else:
                    Logger.error("Article not found in " + str(idx))
            Logger.error("Result: " + str(correct_article_counter) + " / " + str(question_counter))
            Logger.error("Result first Article: " + str(correct_firstArticle_counter) + " / " + str(question_counter))
            Logger.error("Result second Article: " + str(correct_secondArticle_counter) + " / " + str(question_counter))
            Logger.error("Result third Article: " + str(correct_thirdArticle_counter) + " / " + str(question_counter))
            Logger.error('')
            Logger.error('')
            Logger.error('')
            Logger.error('Right Answers: ' + str(correct_answers_counter) + " / " + str(correct_article_counter))
            Logger.error('')
            Logger.error('##############################################################################################')
            Logger.error('')
