# elastic config
ELASTIC_TITLE_BOOST = 5
ELASTIC_TEXT_BOOST = 1

# scoring weights
ELASTIC_WEIGHT = 5 / 8
TFIDF_WEIGHT = 3 / 8
PASSAGE_WEIGHT = 3/8
BIDAF_WEIGHT = 5/8

# other constants
TOP_N_PASSAGES = 10
TOP_N_DOCS = 3

# decision points
SCORE_FOR_BEST_ANSWER = 'bidaf'  # bidaf|final-score
USE_ANSWER_TYPE = True
