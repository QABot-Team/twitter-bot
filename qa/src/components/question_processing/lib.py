import spacy
from spacy.symbols import nsubj, attr, NOUN, PROPN
from pywsd.lesk import simple_lesk
from nltk.corpus import wordnet as wn

FINE_CLASSES = ["abbreviation", "expression", "animal", "body", "color", "creative", "currency",
                "diseases and medicine", "event", "food", "instrument", "language", "letter", "other entities",
                "plant", "product", "religion", "sport", "substance", "symbol", "technique", "term", 
                "vehicle", "word", "definition", "description", "manner", "reason", "group", "individual",
                "title of a person", "description of a person", "city", "country", "mountain", "other location"
                "state", "code", "count", "date", "distance", "money", "order", "other numbers", "period", 
                "percent", "speed", "temperature", "size", "weight" ]
FINE_CLASSES_SYNSETS = ['abbreviation.n.01', 'formula.n.01', 'animal.n.01', 'body.n.01', 'color.n.01',
                        'creative.a.01', 'currency.n.01', 'event.n.01', 'food.n.01', 'musical_instrument.n.01',
                        'speech.n.02', 'letter.n.02', 'plant.n.02', 'merchandise.n.01', 'religion.n.01',
                        'sport.n.01', 'substance.n.01', 'symbol.n.01', 'technique.n.01', 'term.n.01', 'vehicle.n.01',
                        'word.n.01', 'definition.n.01', 'description.n.01', 'manner.n.01', 'reason.n.02', 'group.n.01',
                        'person.n.01', 'city.n.01', 'state.n.04', 'mountain.n.01', 'code.v.02', 'count.n.01', 'date.n.01',
                        'distance.n.01', 'money.n.01', 'rate.v.01','period.n.05', 'percentage.n.01', 'speed.n.01', 'temperature.n.01',
                        'size.n.01', 'weight.n.01', 'disease.n.01',  'entity.n.01', 'title.n.06', 'description.n.02', 'location.n.01',
                        'state.n.01', 'numeral.n.01']

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
            #enriched_question = enriched_question question + " " + ' '.join(get_named_enitity_types(doc)) + " " + str(get_root_token(doc)) + str(get_head_word(doc)) + " " + str(get_head_word(doc))
            pass
        else:
            pass
        #head_word = get_head_word_noun_phrase(doc)
        #similarity_class = get_word_similarity(doc, head_word)
        #enriched_question = enriched_question + " " + str(head_word) #+ " " + str(similarity_class) #+ " " + str(get_hypernym(doc, head_word))
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

def get_word_similarity(doc, head_word):
    head_word_synset = simple_lesk(str(doc), str(head_word))
    if not head_word_synset:
        return ""
    max_similarity = -1
    max_class_synset = ""
    for category in FINE_CLASSES_SYNSETS:
        class_synset = wn.synset(category)
        similarity = wn.path_similarity(head_word_synset, class_synset)
        if similarity and similarity > max_similarity:
            max_class_synset = class_synset
            max_similarity = similarity
    return max_class_synset
