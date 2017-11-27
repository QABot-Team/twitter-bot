import spacy
from spacy.symbols import nsubj, attr, NOUN, PROPN
nlp = spacy.load('en')

def get_features(questions):
    feature_enriched_questions = []
    for question in questions:
        doc = get_doc(question)
        wh_word = str(get_wh_word(doc))
        enriched_question = question
        get_hypernym(question)
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
        print("\n first: " + str(first))
        print("question: " + str(doc))

    for token in reversed(first):
        if token.pos_ == "NOUN":
            print("head word: " + str(token))
            return token

def get_hypernym(question):
    head_word = get_head_word_noun_phrase(get_doc(question))
    answer = None
    #if head_word:
        #print("question: " + question)
        #print("head word: " + head_word)
        #answer = simple_lesk(question, str(head_word), pos=head_word.pos)
    if answer:
        print(answer)
