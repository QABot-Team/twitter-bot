import os
from itertools import chain, combinations
import pandas as pd
from pandas import DataFrame

from .lib import get_root_token, get_named_enitity_types, get_head_word, get_bigrams, get_head_word_noun_phrase, get_hypernym, get_word_similarity, get_doc
from .fit_predict import SVM_CLASS, NB_CLASS, TEST_FILE, create_clf, prepare_questions_from_file

DIR = os.path.dirname(__file__)

clfs = [NB_CLASS, SVM_CLASS]
feature_funcs = [get_root_token, get_named_enitity_types, get_head_word, get_bigrams, get_head_word_noun_phrase]
wh_words = ["how", "who", "when", "where", "which", "what"]

def subsets(_list):
    xs = list(_list)
    return chain.from_iterable(combinations(xs,n) for n in range(len(xs)+1))

def create_feature_set(funcs):
    funcs = funcs
    def get_features(questions):
        feature_enriched_questions = []
        for question in questions:
            features = question
            doc = get_doc(question)
            for func in funcs:
                if callable(func):
                    try:
                        _features = func(doc)
                    except:
                        _features = func(question)
                if isinstance(_features, list):
                    _features = [str(feature) for feature in _features]
                    _features = " ".join(_features)
                else:
                    _features = str(_features)
                features = features + " " + _features
            feature_enriched_questions.append(str(features))
        return feature_enriched_questions

    return get_features

def assess_features():
    func_subsets = list(subsets(feature_funcs))
    assessed_combinations = []
    for wh_word in wh_words:
        for _clf in clfs:
            for func_subset in func_subsets:
                print(_clf.__class__.__name__)
                print([func.__name__ for func in func_subset])
                clf = create_clf(_clf, create_feature_set(func_subset), [wh_word])
                test_qu, test_lb = prepare_questions_from_file(TEST_FILE, create_feature_set(func_subset), [wh_word])
                score = clf.score(test_qu, test_lb)
                print(wh_word)
                print(score)
                print()
                assessed_combinations.append([wh_word, score, _clf.__class__.__name__, " ".join([func.__name__ for func in func_subset]), len(test_qu)])
    return assessed_combinations

columns=["wh_word", "accuracy", "classifier", "features", "#_test_questions"]    

def get_best_combinations(assessed: DataFrame):
    df = pd.DataFrame([], columns=columns)    
    for wh_word in wh_words:
        selected = assessed.loc[assessed["wh_word"]==wh_word]
        best_comb = selected.loc[selected["accuracy"].idxmax()]
        df = df.append(best_comb)
    print(df.head())
    df.to_csv(os.path.join(DIR, "feature_assessment", "fine_best"))

def calc_acc(df):
    total_questions = 0
    true_positive = 0
    for index, row in df.iterrows():
        total_questions += float(row["#_test_questions"])
        true_positive += float(row["#_test_questions"]) * float(row["accuracy"])
    #add total + true_postive for why
    total_questions += 4
    true_positive += 4
    return true_positive/total_questions

assessed = assess_features()
assessed = DataFrame(assessed, columns=columns)
assessed.to_csv(os.path.join(DIR, "feature_assessment", "fine"))
get_best_combinations(assessed)

#coarse_best = 0.888663967611336
#fine_best = 0.8433734939759037

assessed = pd.read_csv(os.path.join(DIR, "feature_assessment", "fine_best"))
print(calc_acc(assessed))