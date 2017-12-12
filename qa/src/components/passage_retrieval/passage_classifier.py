import os
import json
import sys
from sklearn.svm import SVC
import pandas as pd
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score, accuracy_score
from sklearn.externals import joblib
from sklearn.pipeline import Pipeline
sys.path.insert(0,'~/entwicklung/twitter-bot')
from components.question_processing import process_question
from utils.nlptoolkit import NLPToolkit

import spacy

DIR = os.path.dirname(__file__)

def prepare_trainingsdata():
    data = json.load(open('train-v1.1.json'))
    trainings_data = []
    for entry in data['data']:
        text = ""
        qas = []
        for paragraph in entry['paragraphs']:
            text = text + paragraph['context']
            qa_tmp = []
            for qa in paragraph['qas']:
                question = qa['question']
                answers = []
                for answer in qa['answers']:
                    answers.append(answer['text'])
                qa_tmp.append({'question': question, 'answers': answers})
            qas = qas + qa_tmp
        trainings_data.append({'text': text, 'qas': qas})
    with open('trainings_data.json', 'w') as outfile:
        json.dump({'data': trainings_data}, outfile)

def split_trainingsdata_into_sentences():
    data = json.load(open('trainings_data.json'))
    f = open('trainings_data_sentence','w')
    trainings_data_sentence = []
    for entry in data['data']:
        sentences = entry['text'].split('.')
        for qas in entry['qas']:
            question = qas['question']
            qp_result = process_question(question, NLPToolkit())
            #relevant_sentences = []
            #not_relevant_sentences = []
            for sentence in sentences:
                relevant = False
                for answer in qas['answers']:
                    if answer in sentence:
                        relevant = True
                    keywords = get_number_of_keywords(sentence, qp_result.question_model.get_keywords())
                    named_entities = get_number_of_named_entities(sentence, qp_result.answer_type)
                    print("Keywords: " + str(keywords))
                    print("NE: " + str(named_entities))
                    f.write(question + " " + sentence + " ::: " + str(relevant) + '\n')
         
            #trainings_data_sentence.append({'question': question, 'answers': qas, 'relevant': relevant_sentences, 'not_relevant': not_relevant_sentences})
    #with open('trainings_data_sentence.json', 'w') as outfile:
     #   json.dump({'data': trainings_data_sentence}, outfile)   
                 
def get_number_of_keywords(passage, keywords):
    count = 0
    passage_words = passage.spllit()
    for keyword in keywords:
        count = count + passage_words.count(keyword)
    return count 

def get_number_of_named_entities(passage, entity):
    count = 0
    doc = nlp(passage)
    for ent in doc.ents:
        if ent.label_ == entity:
            count = count + 1
    return count
        
        
def get_most_similar(passages, question):
    nlp = spacy.load('en_core_web_lg')

    q_doc = nlp(question)
    max_sim = 0.0
    max_sim_passage = ""

    for passage in passages:
        p_doc = nlp(passage)
        sim = q_doc.similarity(p_doc)
        if sim > max_sim:
            max_sim = sim
            max_sim_passage = passage
    print(max_sim_passage)

def get_passage(passages, question):
    _passages = []
    for passage in passages:
        passage = question + " " + passage
        _passages.append(passage)
    clf = joblib.load(os.path.join(DIR, "nb" + '.pkl'))
    prediction = clf.predict(_passages)
    for idx, pred in enumerate(prediction):
        if str(pred) == ' True':
            print(_passages[idx])
            print()
            print()
            print()
            print()
    
def main():
    split_trainingsdata_into_sentences()
    # sentence_train = pd.read_csv('sentence_train', header=None, encoding='utf-8', sep=':::', engine='python')
    # x = sentence_train.iloc[:,0].values
    # nb = Pipeline([('vect', CountVectorizer()), ('clf', MultinomialNB(alpha=1.0))])
    # y = sentence_train.iloc[:, 1].values
    # X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)
    # nb.fit(X_train, y_train)
    # y_predicted = nb.predict(X_test)

    # joblib.dump(nb, os.path.join(DIR, "nb" + '.pkl'), compress=9)
    # ## Gütemaße ausgeben
    # print("Korrektklassifizierungsrate:\n", accuracy_score(y_true=y_test, y_pred=y_predicted))
    # print("Präzision (mikro):\n", precision_score(y_true=y_test, y_pred=y_predicted, average='micro'))
    # print("Ausbeute (mikro):\n", recall_score(y_true=y_test, y_pred=y_predicted, average='micro'))
    # #print("F1 (mikro):\n", f1_score(y_true=y_test, y_pred=y_predicted, average='micrgio'))
    # print("Kofusionsmatrix:\n", confusion_matrix(y_true=y_test, y_pred=y_predicted))

if __name__ == "__main__":
    main()



