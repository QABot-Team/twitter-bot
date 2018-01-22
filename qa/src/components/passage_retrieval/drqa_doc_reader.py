# Requirements:
# export CLASSPATH=:/Users/felix/Development/htw/pim-projekt/DrQA/data/corenlp/*
# export PYTHONPATH=/Users/felix/Development/htw/pim-projekt/DrQA

import os

BUILD_PATH = os.getcwd() + '/build'

from drqa.reader import Predictor

print(os.path.join(BUILD_PATH, "multitask.mdl"))
predictor = Predictor(os.path.join(BUILD_PATH, "multitask.mdl"))


def get_answer(document, question, candidates=None, top_n=1):
    predictions = predictor.predict(document, question, candidates, top_n)
    return predictions[0][0]
