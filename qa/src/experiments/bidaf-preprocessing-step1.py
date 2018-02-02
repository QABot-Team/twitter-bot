import spacy
import torch
from allennlp.common import Params
from allennlp.data import Vocabulary
from allennlp.models import load_archive
from torch.autograd import Variable


def _remove_pretrained_embedding_params(params: Params):
    keys = params.keys()
    if 'pretrained_file' in keys:
        del params['pretrained_file']
    for value in params.values():
        if isinstance(value, Params):
            _remove_pretrained_embedding_params(value)


archive = load_archive("https://s3-us-west-2.amazonaws.com/allennlp/models/bidaf-model-2017.09.15-charpad.tar.gz")

model_params = archive.config.get('model')
_remove_pretrained_embedding_params(model_params)
vocabulary = Vocabulary.from_files('/Users/felix/Development/htw/pim-projekt/bidaf-model/vocabulary')

# --------------------

nlp = spacy.load('en_core_web_sm')


def tokenize(string):
    doc = nlp(string)
    tokens = []
    for token in doc:
        tokens.append(str(token))
    return tokens


def tokens_to_tensor(tokens):
    indizes = []
    for token in tokens:
        token_index = vocabulary.get_token_index(token.lower())
        indizes.append(token_index)
    return Variable(torch.LongTensor([indizes]))


def token_to_charnum_list(token, length):
    chars = [259]
    for c in token:
        chars.append(ord(c) + 1)
    chars.append(260)
    chars += [0] * (length - len(chars))
    return chars


def tokens_to_char_tensor(tokens):
    char_vector_size = 7 + len(max(tokens, key=lambda x: len(x)))
    list_of_vectors = []
    for token in tokens:
        list_of_vectors.append(token_to_charnum_list(token, char_vector_size))
    return Variable(torch.LongTensor([list_of_vectors]))


passage_str = "A reusable launch system (RLS, or reusable launch vehicle, RLV) is a launch system which is capable " \
          "of launching a payload into space more than once. This contrasts with expendable launch systems, where " \
          "each launch vehicle is launched once and then discarded. No completely reusable orbital launch system has " \
          "ever been created. Two partially reusable launch systems were developed, the Space Shuttle and Falcon 9. " \
          "The Space Shuttle was partially reusable: the orbiter (which included the Space Shuttle main engines and " \
          "the Orbital Maneuvering System engines), and the two solid rocket boosters were reused after several " \
          "months of refitting work for each launch. The external tank was discarded after each flight."
question_str = "How many partially reusable launch systems were developed?"

p_str_tokens = tokenize(passage_str)
q_str_tokens = tokenize(question_str)


p_tokens = tokens_to_tensor(p_str_tokens)
q_tokens = tokens_to_tensor(q_str_tokens)

passage = {
    'tokens': p_tokens,
    'token_characters': tokens_to_char_tensor(p_str_tokens)
}

question = {
    'tokens': q_tokens,
    'token_characters': tokens_to_char_tensor(q_str_tokens)
}

res = archive.model.forward(question, passage)

print('fertig')
