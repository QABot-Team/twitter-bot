from models.answer_type import AnswerType

"""
    PLANT = 2
    ORD = 3
    ANIMAL = 6
    CODE = 8
    DEF = 9
    COLOR = 10
    REASON = 11
    MANNER = 12
    EXP = 13
    VOLSIZE = 16
    PERC = 17
    SYMBOL = 18
    TITLE = 19
    DISMED = 22
    CURRENCY = 23
    LETTER = 24
    PRODUCT = 25
    SPORT = 26
    VEH = 27
    SUBSTANCE = 28
    FOOD = 29
    WORD = 30
    TEMP = 32
    SPEED = 34
    TERMEQ = 36
    INSTRU = 37
    RELIGION = 38
    ABB = 39
    OTHER = 40
    DESC = 43
    BODY = 45
    TECHMETH = 46
"""

def filter_passages(passages, answer_type, nlp_toolkit):
    _filtered = []
    for passage in passages:
        named_ent_types = nlp_toolkit.get_named_enitity_types(passage)
        if answer_type == AnswerType.IND:
            if 'PERSON' in named_ent_types:
                _filtered.append(passage)

        elif answer_type == AnswerType.DATE or answer_type == AnswerType.PERIOD:
            if 'DATE' in named_ent_types:
                _filtered.append(passage)

        elif answer_type == AnswerType.EVENT:
            if 'EVENT' in named_ent_types:
                _filtered.append(passage)
        
        elif answer_type == AnswerType.MOUNT:
            if 'LOC' in named_ent_types:
                _filtered.append(passage)
        
        elif answer_type == AnswerType.CITY or answer_type == AnswerType.COUNTRY or answer_type == AnswerType.STATE:
            if 'GPE' in named_ent_types:
                _filtered.append(passage)

        elif answer_type == AnswerType.MONEY:
            if 'MONEY' in named_ent_types:
                _filtered.append(passage)
        
        elif answer_type == AnswerType.LANG:
            if 'LANGUAGE' in named_ent_types:
                _filtered.append(passage)

        elif answer_type == AnswerType.CREMAT:
            if 'WORK_OF_ART' in named_ent_types:
                _filtered.append(passage)

        elif answer_type == AnswerType.DIST or answer_type == AnswerType.WEIGHT:
            if 'QUANTITY' in named_ent_types:
                _filtered.append(passage)
        
        elif  answer_type == AnswerType.COUNT:
            if 'QUANTITY' in named_ent_types or 'CARDINAL' in named_ent_types:
                _filtered.append(passage)

        elif answer_type == AnswerType.GR:
            if 'ORG' in named_ent_types:
                _filtered.append(passage)

        else:
            _filtered = passages
            break
    return _filtered