import unittest
import os

from components.answer_processing.bidaf import AnswerPredictor
from utils.nlptoolkit import NLPToolkit

DIR = os.path.dirname(__file__)


def read_file(filename):
    result = ""
    file = open(os.path.join(DIR, filename))
    for line in file:
        result += " " + line
    file.close()
    return result


passage = "A reusable launch system (RLS, or reusable launch vehicle, RLV) is a launch system which is " \
                  "capable of launching a payload into space more than once. This contrasts with expendable launch " \
                  "systems, where each launch vehicle is launched once and then discarded. No completely reusable " \
                  "orbital launch system has ever been created. Two partially reusable launch systems were months of " \
                  "refitting work for each launch. The external tank was discarded after each flight."
question = "How many partially reusable launch systems were developed?"
correct_answer = 'Two'
correct_context = 'Two partially reusable launch systems were months of refitting work for each launch.'


class TestReceiveDocs(unittest.TestCase):

    def test_get_context_can_return_multiple_sentences(self):
        expected_context = "This contrasts with expendable launch " \
                  "systems, where each launch vehicle is launched once and then discarded. No completely reusable " \
                  "orbital launch system has ever been created."
        answer_predictor = AnswerPredictor(NLPToolkit())
        context = answer_predictor._get_context_of_best_span(passage, 259, 270)
        self.assertEqual(context, expected_context)

    def test_returns_the_expected_answer(self):
        answer_predictor = AnswerPredictor(NLPToolkit())
        result = answer_predictor.predict(passage, question)

        self.assertEqual(result['answer'], correct_answer)

    def test_returns_the_sentence_containing_the_answer(self):
        answer_predictor = AnswerPredictor(NLPToolkit())
        result = answer_predictor.predict(passage, question)

        self.assertEqual(result['context'], correct_context)

    def test_can_handle_long_passages(self):
        answer_predictor = AnswerPredictor(NLPToolkit())
        long_passage = read_file('long_passage.txt')[:60000]
        answer_predictor.predict(long_passage, 'When was Barack Obama born?')


if __name__ == '__main__':
    unittest.main()
