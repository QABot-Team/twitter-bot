import spacy
from spacy.symbols import nsubj, attr, NOUN, PROPN
from pywsd.lesk import simple_lesk
from nltk.corpus import wordnet as wn

nlp = spacy.load('en')

def get_features(questions):
    feature_enriched_questions = []
    for question in questions:
        doc = get_doc(question)
        wh_word = str(get_wh_word(doc))
        enriched_question = question
        if wh_word == "how":
            pass
        elif wh_word == "who":
            pass
        elif wh_word == "why":
            pass
        elif wh_word == "when":
            pass
        elif wh_word == "where":
            pass
        elif wh_word == "which":
            pass
        elif wh_word == "what":
            #enriched_question = enriched_question + question + " " + ' '.join(get_named_enitity_types(doc)) + " " + str(get_root_token(doc)) + str(get_head_word(doc)) + " " + str(get_head_word(doc))
            pass
        else:
            pass
        #head_word = get_head_word_noun_phrase(doc)
        #enriched_question = enriched_question + " " + str(head_word) + " " + str(get_head_word(doc))# + " " + str(get_hypernym(doc, head_word))
        feature_enriched_questions.append(enriched_question)
    return feature_enriched_questions

def get_label(question):
    words = question.split()
    label = words[0]
    return label

def get_question(question):
    words = question.split()
    words.pop(0)
    return ' '.join(words)

def get_questions_and_labels(questions):
    _questions = []
    _labels = []
    for question in questions:
        _labels.append(get_label(question))
        _questions.append(get_question(question))
    return {"questions": _questions , "labels": _labels}

def select_questions(questions, wh_words = []):
    selected_questions = []
    for question in questions:
        doc = get_doc(question)
        wh_word = str(get_wh_word(doc)).lower()
        if len(wh_words) > 0 and wh_word not in wh_words:
            continue
        selected_questions.append(question)
    return selected_questions

def get_doc(str):
    return nlp(str)

def token_is_wh_w(token):
    return token.tag_ == "WDT" or token.tag_ == "WP" or token.tag_ == "WP$" or token.tag_ == "WRB"

def get_wh_word(sent):
    for token in sent:
        if token_is_wh_w(token):
            return token

def get_root_token(doc):
    for token in doc:
        if token.dep_ == "ROOT":
            return token

def get_named_enitity_types(doc):
    ents = [(e.label_) for e in doc.ents]
    return ents

def get_head_word(doc):
    for token in doc:
        if token.dep == nsubj and (token.pos == NOUN or token.pos == PROPN):
            return token
        elif token.dep == attr and (token.pos == NOUN or token.pos == PROPN):
            return token
    return ""
                
def get_bigrams(question):
    words = question.split()
    idx = 0
    bigrams = []
    while (idx+1) < len(words):
        bigrams.append(words[idx] + "-" + words[idx+1])
        idx += 1
    return bigrams

def get_head_word_noun_phrase(doc):
    noun_chunks = list(doc.noun_chunks)
    first = ""
    if len(noun_chunks) > 0:
        first = noun_chunks[0]
        #print("\n question: " + str(doc))
        for noun_chunk in noun_chunks:
            #print("\n chunk: " + str(noun_chunk))
            for token in reversed(noun_chunk):
                if token.pos_ == "NOUN" and not token_is_wh_w(token):
                    #print("head word: " + str(token))
                    return token

def get_hypernym(doc, head_word):
    hypernyms = []
    if head_word:
        #print("question: " + str(doc))
        #print("head word: " + str(head_word) + " pos=" + str(head_word.pos_))
        synset = simple_lesk(str(doc), str(head_word))
        if synset:
            unvisited_hypernyms = synset.hypernyms()
            for i in range(5):
                for hypernym in unvisited_hypernyms:
                    unvisited_hypernyms = unvisited_hypernyms + hypernym.hypernyms()
                    unvisited_hypernyms.remove(hypernym)
                    hypernyms.append(hypernym)
            hypernyms.append(synset)
            #print(str(hypernyms))
    return hypernyms
