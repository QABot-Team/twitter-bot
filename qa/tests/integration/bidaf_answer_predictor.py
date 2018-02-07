import unittest

from components.answer_processing.bidaf import AnswerPredictor
from utils.nlptoolkit import NLPToolkit


class TestReceiveDocs(unittest.TestCase):

    def test_returns_the_expected_answer(self):
        passage = "A reusable launch system (RLS, or reusable launch vehicle, RLV) is a launch system which is " \
                  "capable of launching a payload into space more than once. This contrasts with expendable launch " \
                  "systems, where each launch vehicle is launched once and then discarded. No completely reusable " \
                  "orbital launch system has ever been created. Two partially reusable launch systems were months of " \
                  "refitting work for each launch. The external tank was discarded after each flight."
        question = "How many partially reusable launch systems were developed?"

        answer_predictor = AnswerPredictor(NLPToolkit())
        result = answer_predictor.predict(passage, question)

        self.assertEqual(result['answer'], 'Two')


if __name__ == '__main__':
    unittest.main()
