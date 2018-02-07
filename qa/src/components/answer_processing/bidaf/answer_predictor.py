import torch
from allennlp.models import BidirectionalAttentionFlow
from torch.autograd import Variable

from components.answer_processing.bidaf import ArchiveLoader
from utils.nlptoolkit import NLPToolkit

_MODEL_ARCHIVE = 'https://s3-us-west-2.amazonaws.com/allennlp/models/bidaf-model-2017.09.15-charpad.tar.gz'


def char_to_int(c):
    int_repr = ord(c)
    if 8207 < int_repr < 8214:
        return 45
    if int_repr > 500:
        print(str(int_repr) + ' -> ' + str(c))
        return 0
    return int_repr


class AnswerPredictor:

    def __init__(self, nlp_toolkit: NLPToolkit):
        self.nlp_toolkit = nlp_toolkit
        archive_loader = ArchiveLoader(_MODEL_ARCHIVE)
        config = archive_loader.get_config()
        model_params = config.get('model')
        vocabulary = archive_loader.get_vocabulary()

        self.bidaf_model = BidirectionalAttentionFlow.from_params(vocabulary, model_params)
        model_state = archive_loader.get_model_state()
        self.bidaf_model.load_state_dict(model_state)

        self.vocab_reader = archive_loader.get_vocab_reader()

    def predict(self, passage: str, question: str):
        p_tokens = self.nlp_toolkit.tokenize(passage)
        q_tokens = self.nlp_toolkit.tokenize(question)

        passage_input = {
            'tokens': self._tokens_to_tensor(p_tokens),
            'token_characters': self._tokens_to_char_tensor(p_tokens)
        }

        question_input = {
            'tokens': self._tokens_to_tensor(q_tokens),
            'token_characters': self._tokens_to_char_tensor(q_tokens)
        }

        res = self.bidaf_model.forward(question_input, passage_input)

        start_confidence = float(torch.topk(res['span_start_probs'], 1)[0].data.cpu())
        end_confidence = float(torch.topk(res['span_end_probs'], 1)[0].data.cpu())
        confidence = start_confidence * end_confidence

        answer = self._best_span_to_answer(passage, res['best_span'], self._get_token_offsets(p_tokens))

        return {
            'answer': answer,
            'confidence': confidence
        }

    def _tokens_to_tensor(self, tokens):
        indizes = []
        for token in tokens:
            token_index = self.vocab_reader.get_token_index(token.text)
            indizes.append(token_index)
        return Variable(torch.LongTensor([indizes]))

    @staticmethod
    def _token_to_charnum_list(token, length):
        chars = [259]
        for c in token.text:
            chars.append(char_to_int(c) + 1)
        chars.append(260)
        chars += [0] * (length - len(chars))
        return chars

    def _tokens_to_char_tensor(self, tokens):
        char_vector_size = 7 + len(max(tokens, key=lambda x: len(x)))
        list_of_vectors = []
        for token in tokens:
            list_of_vectors.append(self._token_to_charnum_list(token, char_vector_size))
        return Variable(torch.LongTensor([list_of_vectors]))

    @staticmethod
    def _get_token_offsets(tokens):
        offsets = []
        for token in tokens:
            start = token.idx
            offset = (start, start + len(token.text))
            offsets.append(offset)
        return offsets

    @staticmethod
    def _best_span_to_answer(passage_str, best_spans, offsets):
        predicted_span = tuple(best_spans[0].data.cpu().numpy())
        start_offset = offsets[predicted_span[0]][0]
        end_offset = offsets[predicted_span[1]][1]
        return passage_str[start_offset:end_offset]
