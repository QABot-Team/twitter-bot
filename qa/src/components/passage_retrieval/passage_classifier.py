import json
from sklearn.svm import SVC
import pandas as pd
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score, accuracy_score

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
            relevant_sentences = []
            not_relevant_sentences = []
            for sentence in sentences:
                relevant = False
                for answer in qas['answers']:
                    if answer in sentence:
                        relevant = True
                f.write(question + " " + sentence + " ::: " + str(relevant) + '\n')
         
            #trainings_data_sentence.append({'question': question, 'answers': qas, 'relevant': relevant_sentences, 'not_relevant': not_relevant_sentences})
    #with open('trainings_data_sentence.json', 'w') as outfile:
     #   json.dump({'data': trainings_data_sentence}, outfile)   
                 
#split_trainingsdata_into_sentences()

sentence_train = pd.read_csv('sentence_train', header=None, encoding='utf-8', sep=':::')
X = sentence_train.iloc[:,0].values
vectorizer = CountVectorizer()
X_vec = vectorizer.fit_transform(X)
y = sentence_train.iloc[:, 1].values
X_train, X_test, y_train, y_test = train_test_split(X_vec, y, test_size=0.2, random_state=0)

nb = MultinomialNB(alpha=1.0)
nb.fit(X_train, y_train)
y_predicted = nb.predict(X_test)

## Gütemaße ausgeben
print("Korrektklassifizierungsrate:\n", accuracy_score(y_true=y_test, y_pred=y_predicted))
print("Präzision (mikro):\n", precision_score(y_true=y_test, y_pred=y_predicted, average='micro'))
print("Ausbeute (mikro):\n", recall_score(y_true=y_test, y_pred=y_predicted, average='micro'))
print("F1 (mikro):\n", f1_score(y_true=y_test, y_pred=y_predicted, average='micrgio'))
print("Kofusionsmatrix:\n", confusion_matrix(y_true=y_test, y_pred=y_predicted))