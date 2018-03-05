import spacy


class NLPToolkit:
    def __init__(self):
        self.nlp = spacy.load('en_core_web_sm')
        # self.nlp = spacy.load('en_core_web_lg')

    def tokenize(self, text: str) -> list:
        doc = self.nlp(text)
        tokens = []
        for token in doc:
            tokens.append(token)
        return tokens

    def remove_stop_words(self, text: str) -> list:
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

    def text_to_sentences_with_offsets(self, text) -> list:
        doc = self.nlp(text)

        return [self._sentence_span_to_dict_with_offsets(sent) for sent in doc.sents]

    @staticmethod
    def _sentence_span_to_dict_with_offsets(sent_span):
        return {
            'text': sent_span.string.strip(),
            'start': sent_span.start_char,
            'end': sent_span.end_char
        }

    def add_pos_tags(self, text) -> list:
        doc = self.nlp(text)

        return [token.text + "|" + token.pos_ for token in doc]

    def token_is_wh_w(self, token):
        return token.tag_ == "WDT" or token.tag_ == "WP" or token.tag_ == "WP$" or token.tag_ == "WRB"

    def get_wh_word(self, doc):
        for token in doc:
            if self.token_is_wh_w(token):
                return token

    def get_root_token(self, doc):
        for token in doc:
            if token.dep_ == "ROOT":
                return token

    def get_named_enitity_types(self, text):
        doc = self.nlp(text)
        ents = [(e.label_) for e in doc.ents]
        return ents

    def get_similiarity(self, question, answer):
        q_doc = self.nlp(question)
        q_ans = self.nlp(answer)
        return q_doc.similarity(q_ans)

    def get_key_words(self, question):
        doc = self.nlp(question)
        keywords = []
        for token in doc:
            if self.token_is_wh_w(token):
                continue
            if str(token) == "?":
                continue
            if token.is_stop:
                continue
            keywords.append(str(token))
        return keywords

    def get_headwords(self, question):
        doc = self.nlp(question)
        headwords = []
        for sent in doc.sents:
            for token in sent:
                if self.token_is_wh_w(token):
                    continue
                if str(token) == "?":
                    continue
                if token.is_stop:
                    continue
                # if (token.dep_ in ['nsubj', 'attr', 'pobj']) and (token.pos_ in ['NOUN', 'PROPN']):
                if token.pos_ in ['NOUN', 'PROPN', 'NUM']:
                    headwords.append(token.text)

        return headwords
