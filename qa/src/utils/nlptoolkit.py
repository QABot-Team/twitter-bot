import spacy


class NLPToolkit:
    def __init__(self):
        self.nlp = spacy.load('en')

    def extract_stop_words(self, text: str) -> list:
        doc = self.nlp(text)
        result = []
        for token in doc:
            if not token.is_punct | token.is_space | token.is_stop:
                result.append(token.text)

        return result

    def lemmatize(self, text: str) -> list:
        doc = self.nlp(text)
        result = []
        for token in doc:
            result += token.lemma_

        return result

    def minimize(self, text: str) -> list:
        doc = self.nlp(text)
        result = []
        for token in doc:
            if not token.is_punct | token.is_space | token.is_stop:
                result.append(token.lemma_)

        return result

    def text_to_sentences(self, text) -> list:
        doc = self.nlp(text)

        return [sent.string.strip() for sent in doc.sents]

    def add_pos_tags(self, text) -> list:
        doc = self.nlp(text)

        return [token.text + "|" + token.pos_ for token in doc]
