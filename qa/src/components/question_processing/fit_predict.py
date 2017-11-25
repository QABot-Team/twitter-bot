#http://scikit-learn.org/stable/tutorial/text_analytics/working_with_text_data.html
from sklearn import svm
from lib import select_questions, get_questions_and_labels, get_features, vectorize_test, vectorize_train
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score

def fit_svm(train_qu, train_lb):
    clf = svm.SVC(kernel='linear')
    clf.fit(train_qu, train_lb)
    return clf

def score_svm(clf, test_qu, test_lb):
    print("SVM Accuracy: ", clf.score(test_qu, test_lb))
    
def fit_naive_bayes(train_qu, train_lb):
    nb = MultinomialNB(alpha=1.0)
    nb.fit(train_qu, train_lb)
    return nb

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
    
train_qu, train_lb = prepare_questions_from_file("labeled_questions/train_5500_first_lvl.label")
train_qu = vectorize_train(train_qu)

test_qu, test_lb = prepare_questions_from_file("labeled_questions/test_first_lvl.label")
test_qu = vectorize_test(test_qu)

svm_clf = fit_svm(train_qu, train_lb)
nb_clf = fit_naive_bayes(train_qu, train_lb)

score_svm(svm_clf, test_qu, test_lb)
score_naive_bayes(nb_clf, test_qu, test_lb)

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

#passage retrieval:

'''
Introduction to information retrieval manning, Language Modeling
Passage Retrieval auf Wikipedia daten - Was machen andere Paper? - Position der Passage ausnutzen?
'''