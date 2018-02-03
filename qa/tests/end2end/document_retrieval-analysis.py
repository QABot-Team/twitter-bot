import os
import sys
import json

from models.question_model import QuestionModel
from components.document_retrieval import receive_docs
from utils.logger import Logger
from utils.nlptoolkit import NLPToolkit

DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.append(DIR + '/../../src')
data = json.load(open('dev-v1.1.json'))


def text_contains_any_answer(text, answers):
    for a in answers:
        if a['text'] in text:
            return True
    return False


Logger.config('error')

Logger.error("Start analysis")

nlp = NLPToolkit()
question_counter = 0
correct_answers_counter = 0
correct_answer_dict = {
    0: 0,
    1: 0,
    2: 0,
    3: 0,
    4: 0
}

false_answer = 0

for dataset in data['data']:
    title = dataset['title']
    title_ext = title.replace('_', ' ')
    Logger.error('Dataset: ' + title)

    for paragraph in dataset['paragraphs'][:5]:
        for question_answer_set in paragraph['qas']:
            Logger.error('####################################################')
            Logger.error('Question ' + str(question_counter))
            Logger.error('')
            question_counter += 1
            question = question_answer_set['question']
            correct_answers = question_answer_set['answers']
            Logger.error(question)

            # answer = process_answer_question(question)

            keywords = nlp.get_headwords(question)
            Logger.error('Headwords: ' + ', '.join(keywords))
            keywords.append(title_ext)
            qm = QuestionModel(keywords, question)
            # error("Keywords: " + ', '.join(keywords))
            docs = receive_docs(qm, nlp)
            Logger.error("Correct Doc: " + title_ext)

            found = False
            for idx, doc in enumerate(docs.docs[:5]):
                if doc.title in title_ext:
                    correct_answer_dict[idx] += 1
                    found = True
                    break

            if not found:
                Logger.error("No Matching Doc found: ")
                Logger.error("Docs: " + docs.get_doc(1).title + ", " +
                             docs.get_doc(2).title + ", " + docs.get_doc(3).title)
                false_answer += 1

            Logger.error('')

    Logger.error("Result: ")
    Logger.error('Correct Article 1: ' + str(correct_answer_dict[0]))
    Logger.error('Correct Article 2: ' + str(correct_answer_dict[1]))
    Logger.error('Correct Article 3: ' + str(correct_answer_dict[2]))
    Logger.error('Correct Article 4: ' + str(correct_answer_dict[3]))
    Logger.error('Correct Article 5: ' + str(correct_answer_dict[4]))
    Logger.error('')
    Logger.error('Correct Articles: ' +
                 str(correct_answer_dict[0] + correct_answer_dict[1] + correct_answer_dict[2] +
                     correct_answer_dict[3] + correct_answer_dict[4]) + ' / ' +
                 str(question_counter))
    Logger.error('####################################################################################################')
    break
