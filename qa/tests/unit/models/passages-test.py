import unittest

from models.passage import Passage
from models.passages import Passages


class TestPassagesModel(unittest.TestCase):

    def test_for_each(self):
        passages = Passages()
        passages.add(Passage('Hello world'))
        passages.add(Passage('Goodbye'))
        length_array = passages.map(lambda p: len(p.text))
        self.assertEqual(18, length_array[0] + length_array[1])


if __name__ == '__main__':
    unittest.main()
