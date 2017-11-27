#http://scikit-learn.org/stable/tutorial/text_analytics/working_with_text_data.html
from lib import select_questions, get_questions_and_labels, get_features
from sklearn import svm
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
from sklearn.externals import joblib
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer

SVM_CLF_NAME = "svm_clf"
NB_CLF_NAME = "nb_clf"

def fit_svm(train_qu, train_lb):
    vec_clf = Pipeline([('vect', CountVectorizer()), ('clf', svm.SVC(kernel='linear'))])
    vec_clf.fit(train_qu, train_lb)
    return vec_clf

def score_svm(clf, test_qu, test_lb):
    print("SVM Accuracy: ", clf.score(test_qu, test_lb))
    
def fit_naive_bayes(train_qu, train_lb):
    vec_clf = Pipeline([('vect', CountVectorizer()), ('clf', MultinomialNB(alpha=1.0))])
    vec_clf.fit(train_qu, train_lb)
    return vec_clf

def score_naive_bayes(nb, test_qu, test_lb):
    y_predicted = nb.predict(test_qu)
    print("Naive Bayes Accuracy: ", accuracy_score(y_true=test_lb, y_pred=y_predicted))

def prepare_questions_from_file(filepath):
    file = open(filepath, "r")
    file = list(file)
    labeled_questions = select_questions(file, [])
    data = get_questions_and_labels(labeled_questions)
    feature_enriched_questions = get_features(data["questions"])
    return [feature_enriched_questions, data["labels"]]

def write_clf_2_disk(clf, name):
    joblib.dump(clf, name + '.pkl', compress=9)

def get_clf_from_disk(name):
    clf = joblib.load(name + '.pkl')
    return clf

def get_predicted_label(question, clf):
    feature_enriched_question = get_features([question])
    return clf.predict(feature_enriched_question)

def main():
    train_qu, train_lb = prepare_questions_from_file("labeled_questions/NUM_questions_train.label")
    test_qu, test_lb = prepare_questions_from_file("labeled_questions/NUM_questions_test.label")

    svm_clf = fit_svm(train_qu, train_lb)
    nb_clf = fit_naive_bayes(train_qu, train_lb)

    score_svm(svm_clf, test_qu, test_lb)
    score_naive_bayes(nb_clf, test_qu, test_lb)

    #write_clf_2_disk(svm_clf, SVM_CLF_NAME)
    #write_clf_2_disk(nb_clf, NB_CLF_NAME)

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