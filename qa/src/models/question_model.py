class QuestionModel:
    def __init__(self, keywords: list, question) -> None:
        self.keywords = keywords
        self.question = question

    def get_keywords(self):
        return self.keywords
