from models.iterable import Iterable
from models.prediction import Prediction


class Predictions(Iterable):
    def __init__(self) -> None:
        self.predictions = []

    def add(self, prediction: Prediction) -> None:
        self.predictions.append(prediction)

    def get_passage_at(self, index: int) -> Prediction:
        return self.predictions[index]

    def __iter__(self):
        return iter(self.predictions)

    def get_score(self, prediction: Prediction):
        return prediction.bidaf_score

    def set_score(self, prediction: Prediction, score: float):
        prediction.bidaf_score = score
