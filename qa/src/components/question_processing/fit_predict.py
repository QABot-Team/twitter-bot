import os
from .lib import select_questions, get_questions_and_labels, get_features, get_doc, get_wh_word, token_is_wh_w
from sklearn import svm
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
from sklearn.externals import joblib
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer

SVM_CLASS = svm.SVC(kernel='linear')
NB_CLASS = MultinomialNB(alpha=1.0)

SVM_CLF_NAME = "svm_clf"
NB_CLF_NAME = "nb_clf"

DIR = os.path.dirname(__file__)

TRAIN_FILE = os.path.join(DIR, "labeled_questions", "train_5500_second_lvl.label")
TEST_FILE =  os.path.join(DIR, "labeled_questions", "test_second_lvl.label")

def fit_clf(clf_class, train_qu, train_lb):
    vec_clf = Pipeline([('vect', CountVectorizer()), ('clf', clf_class)])
    vec_clf.fit(train_qu, train_lb)
    return vec_clf

def create_clf(clf_class, feature_func = get_features, wh_words=[]):
    train_qu, train_lb = prepare_questions_from_file(TRAIN_FILE, feature_func, wh_words)
    clf = fit_clf(clf_class, train_qu, train_lb)
    return clf

def score_clf(clf, test_qu, test_lb, clf_name):
    print("{} Accuracy: {}".format(clf_name, clf.score(test_qu, test_lb)))

def prepare_questions_from_file(filepath, feature_func = get_features, wh_words = []):
    file = open(filepath, "r")
    file = list(file)
    labeled_questions = select_questions(file, wh_words)
    data = get_questions_and_labels(labeled_questions)
    if callable(feature_func):
        feature_enriched_questions = feature_func(data["questions"])
    else:
        feature_enriched_questions = data["questions"]
    return [feature_enriched_questions, data["labels"]]

def write_clf_2_disk(clf, name):
    joblib.dump(clf, os.path.join(DIR, name + '.pkl'), compress=9)

def get_clf_from_disk(name) -> Pipeline:
    clf = None
    try:
        clf = joblib.load(os.path.join(DIR, name + '.pkl'))
    except:
        if name == NB_CLF_NAME:
            clf = create_clf(NB_CLASS)
        elif name == SVM_CLF_NAME:
            clf = create_clf(SVM_CLASS)
        write_clf_2_disk(clf, name)
    return clf

def get_clf_name(question):
    doc = get_doc(question)
    wh_word = str(get_wh_word(doc)).lower()
    if wh_word == "how":
        return SVM_CLF_NAME
    elif wh_word == "who":
        return SVM_CLF_NAME
    elif wh_word == "why":
        return NB_CLF_NAME
    elif wh_word == "when":
        return NB_CLF_NAME
    elif wh_word == "where":
        return NB_CLF_NAME
    elif wh_word == "which":
        return NB_CLF_NAME
    elif wh_word == "what":
        return SVM_CLF_NAME
    else:
        return SVM_CLF_NAME

def get_predicted_label(question, clf):
    feature_enriched_question = get_features([question])
    return clf.predict(feature_enriched_question)[0]

def get_key_words(question):
    doc = get_doc(question)
    keywords = []
    for token in doc:
        if token_is_wh_w(token):
            continue
        if str(token) == "?":
            continue
        if token.is_stop:
            continue
        keywords.append(str(token))
    return keywords

def main():
    svm_clf = create_clf(SVM_CLASS)
    nb_clf = create_clf(NB_CLASS)

    test_qu, test_lb = prepare_questions_from_file(TEST_FILE)

    score_clf(svm_clf, test_qu, test_lb, "SVM")
    score_clf(nb_clf, test_qu, test_lb, "NB")

if __name__ == "__main__":
    main()

#SVM:
#Bag of Words
#alle: 0.868
#how: 0.97
#who: 1.0
#nur why: nur ein Label -> 1.0
#when: 1.0
#where: 1.0
#which: 0.363
#what: 0.828

#BoW + 1x headword:
#which: 0.4545

#BoW + 2x headword:
#which: 0.4545
#what: 0.828

#BoW + Named entity types:
#what: 0.822

#BoW + Named entity types + 2x headword:
#what: 0.848

#BoW + 2x headword + root token + headword pos:
#what: 0.833

#BoW + 2x headword + root token + headword pos + Named entity types:
#what: 0.828

#Naive Bayes
#Bag of Words:
#alle: 0.76
#nur how: 1.0
#nur who: 1.0
#nur why: nur ein Label -> 1.0
#nur when: 1.0
#nur where: 1.0
#nur which: 0.363
#nur what: 0.664

#BoW + 1x headword:
#which: 0.4545

#BoW + 2x headword:
#which: 0.5454
#what: 0.719

#BoW + Named entity types:
#0.659

#BoW + Named entity types + 2x headword:
#what: 0.722

#BoW + 2x headword + root token + headword pos:
#what: 0.71

#BoW + 2x headword + root token + headword pos + Named entity types:
#what: 0.73

#Anmerkungen:
#hinzufügen von headword pos verringert accuracy um ~0.001
#2 maliges hinzufügen von head word steigert accuracy von SVM um ~0.1, bei SVM um ~0.001


#feine taxonomie
#SVM:
#nur BoW:
#ABBR: 0.88
#DESC: 0.992
#ENTY: 0.595
#HUM: 0.953
#LOC: 0.95
#NUM: 0.858

#passage retrieval:

'''
Introduction to information retrieval manning, Language Modeling
Passage Retrieval auf Wikipedia daten - Was machen andere Paper? - Position der Passage ausnutzen?
'''