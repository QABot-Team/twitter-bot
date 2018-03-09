import sys

from models.iterable import Iterable


class Scorer:
    @staticmethod
    def min_max_norm(iterables: Iterable):
        min_val = sys.float_info.max
        max_val = 0

        for it in iterables:
            tmp_score = iterables.get_score(it)
            if min_val > tmp_score:
                min_val = tmp_score
            if max_val < tmp_score:
                max_val = tmp_score

        for it in iterables:
            tmp_score = iterables.get_score(it)
            new_score = 1 if max_val == min_val else (tmp_score - min_val)/(max_val - min_val)
            iterables.set_score(it, new_score)
