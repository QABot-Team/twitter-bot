import spacy
from spacy.symbols import nsubj, attr, NOUN, PROPN
from sklearn.feature_extraction.text import CountVectorizer
vectorizer = CountVectorizer()
nlp = spacy.load('en')

def get_features(wh_word, doc, question):
    if wh_word == "how":
        return [question]
    elif wh_word == "who":
        return [question]
        #return wh_word
    elif wh_word == "why":
        return [question]
        #return wh_word        
    elif wh_word == "when":
        return [question]
        #return wh_word        
    elif wh_word == "where":
        return [question]
        #return wh_word        
    elif wh_word == "which":
        return [question]
    elif wh_word == "what":
        return [question]
        #return get_bigrams(question)
    else:
        return wh_word

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

def vectorize_train(questions):
    return vectorizer.fit_transform(questions)

def vectorize_test(questions):
    return vectorizer.transform(questions)

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
