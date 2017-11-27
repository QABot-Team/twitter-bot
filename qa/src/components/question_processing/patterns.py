import re

def get_category(theStr):

    #DESC:def pattern 1
    if re.search('[Ww]hat (is|are|\'s) (a|an|the)? ([a-zA-Z])+(\s([a-zA-Z])+)?(\s)?[?]', theStr):
        return "DESC"

    #DESC.def pattern 2
    elif re.search('[Ww]hat (do|does)(\s([a-zA-Z])+)+ mean(\s)?[?]', theStr):
        return "DESC"

    #ENTY:substance pattern
    elif re.search('[Ww]hat (is|are)(\s([a-zA-Z])+)+ (composed of|made of|made out of)(\s)?[?]', theStr):
        return "ENTY"

    #DESC:desc pattern
    elif re.search('[Ww]hat does(\s([a-zA-Z])+)+ do(\s)?[?]', theStr):
        return "DESC"

    #ENTY:term pattern
    elif re.search('[Ww]hat do you call(\s([a-zA-Z])+)+(\s)?[?]', theStr):
        return "ENTY"

    #DESC:reason pattern 1
    elif re.search('[Ww]hat (causes|cause)(\s([a-zA-Z])+)+(\s)?[?]', theStr):
        return "DESC"

    #DESC:reason pattern 2
    elif re.search('[Ww]hat (is|are)(\s([a-zA-Z])+)+ used for(\s)?[?]', theStr):
        return "DESC"

    #ABBR:exp pattern
    elif re.search('[Ww]hat (does|do)(\s([a-zA-Z])+)+ stand for(\s)?[?]', theStr):
        return "ABBR"

    else:
        return -1

    #HUM:desc pattern
    ''' elif re.search('[Ww]ho (is|was) (([A-Z])([a-zA-Z])*)[?]', theStr):
        print("found") '''

def get_pattern_accuracy(questions, labels):
    right = 0
    for question, label in zip(questions, labels):
        _label = get_category(question)
        if _label == label:
            right += 1
    print(float(right)/float(len(questions)))