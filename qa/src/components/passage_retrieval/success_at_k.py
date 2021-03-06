#test passage retrieval using the sentence_train file

#first, extract the questions, the possible answers, and the answer rating (true/false) for every possible answer

import os
import re
import numpy as np
from models.answer_type import AnswerType
from components.question_processing.fit_predict import get_clf_from_disk, get_predicted_label, get_clf_name
from .filter_passages import filter_passages
from utils.nlptoolkit import NLPToolkit

DIR = os.path.dirname(__file__)


class Question(object):

    def __init__(self, question, passages, passage_labels):
        self.question = question
        self.passages = passages
        self.passage_labels = passage_labels
        self.passage_ratings = []
        self.filter_passages()

    def relevant_in_top_k(self, k):
        """ returns 1 if the real answer is included in the k top rated passages, otherwise returns 0 """
        arr = np.array(self.passage_ratings)
        if k > len(self.passages):
            k = len(self.passages)
        top_k_ratings = np.argpartition(arr, -(k))[-(k):]
        top_k_labels = list(np.array(self.passage_labels)[top_k_ratings])
        #print("Question: {}".format(self.question))
        #print(list(np.array(self.passages)[top_k_ratings]))
        #print()
        return int((sum(map(lambda label: label == "True\n", top_k_labels))) >= 1)
        

    def rate_passages(self, rater):
        question = nlp_toolkit.get_key_words(self.question)
        question = " ".join(question)
        for passage in self.passages:
            passage = nlp_toolkit.get_key_words(passage)
            passage = " ".join(passage)
            rating = rater(question, passage)
            rating = rating + (0.1 * _rater(question, passage))
            self.passage_ratings.append(rating)

    def filter_passages(self):
        clf_name = get_clf_name(self.question)
        clf = get_clf_from_disk(clf_name)
        label = get_predicted_label(self.question, clf)
        #print("Question: {}".format(self.question))
        #print("Label: {}".format(label))
        passages = filter_passages(self.passages, AnswerType[label], nlp_toolkit)

        #get index of missing passages to remove the corresponding labels
        missing_passages = [idx for (idx, passage) in enumerate(self.passages) if passage not in passages]
        self.passage_labels = list(np.delete(self.passage_labels, missing_passages))
        #print("Length old: {}".format(len(self.passages)))
        #print("Length new: {}".format(len(passages)))
        #print()
        self.passages = passages
        #print(self.passages)

class Questions(object):

    def __init__(self, file):
        self.file = file
        self.questions = []
        self.setup()
    def setup(self):
        file = open(self.file, "r", encoding="utf8")
        questions_dict = {}
        for line in file:
            split_question = line.split("? ")
            question = split_question[0] + "?"
            passage, label = re.split("\d \d.\d* ::: ", split_question[1])
            if question not in questions_dict:
                questions_dict[question] = {"passages": [], "labels": []}
            questions_dict[question]["passages"].append(passage)
            questions_dict[question]["labels"].append(label)
        file.close()

        for key in questions_dict:
            question = Question(key, questions_dict[key]["passages"], questions_dict[key]["labels"])
            self.questions.append(question)

    def relevant_in_top_k(self, k):
        num_relevant = 0.0
        for question in self.questions:
            num_relevant += question.relevant_in_top_k(k)
        return float(num_relevant)/len(self.questions)

    def rate_passages(self, rater):
        for question in self.questions:
            question.rate_passages(rater)

def _rater(question, answer):
    question = question.split()
    question = list(set(question))
    answer = answer.split()

    counter = 0
    for token in question:
        if token in answer:
            counter += 1
    return counter

if __name__ == "__main__":
    print("create toolkit")
    nlp_toolkit = NLPToolkit()
    print("create questions object")
    questions = Questions(os.path.join(DIR, "sentence_train"))
    print("get similarity")
    questions.rate_passages(nlp_toolkit.get_similiarity)
    #questions.rate_passages(_rater)
    print("get relevant at k")

    print("Relevant at 1: {}".format(questions.relevant_in_top_k(1)))
    print("Relevant at 2: {}".format(questions.relevant_in_top_k(2)))
    print("Relevant at 3: {}".format(questions.relevant_in_top_k(3)))
    print("Relevant at 4: {}".format(questions.relevant_in_top_k(4)))
    print("Relevant at 5: {}".format(questions.relevant_in_top_k(5)))
    print("Relevant at 10: {}".format(questions.relevant_in_top_k(10)))
    print("Relevant at 15: {}".format(questions.relevant_in_top_k(15)))
    print("Relevant at 20: {}".format(questions.relevant_in_top_k(20)))
    print("Relevant at 25: {}".format(questions.relevant_in_top_k(25)))
    print("Relevant at 50: {}".format(questions.relevant_in_top_k(50)))