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
    COUNT = 31
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
        if answer_type == AnswerType.HUM_ind:
            if 'PERSON' in named_ent_types:
                _filtered.append(passage)

        elif answer_type == AnswerType.NUM_date or answer_type == AnswerType.NUM_period:
            if 'DATE' in named_ent_types:
                _filtered.append(passage)

        elif answer_type == AnswerType.ENTY_event:
            if 'EVENT' in named_ent_types:
                _filtered.append(passage)
        
        elif answer_type == AnswerType.LOC_mount:
            if 'LOC' in named_ent_types:
                _filtered.append(passage)
        
        elif answer_type == AnswerType.LOC_city or answer_type == AnswerType.LOC_country or answer_type == AnswerType.LOC_state:
            if 'GPE' in named_ent_types:
                _filtered.append(passage)

        elif answer_type == AnswerType.NUM_money:
            if 'MONEY' in named_ent_types:
                _filtered.append(passage)
        
        elif answer_type == AnswerType.ENTY_lang:
            if 'LANGUAGE' in named_ent_types:
                _filtered.append(passage)

        elif answer_type == AnswerType.ENTY_cremat:
            if 'WORK_OF_ART' in named_ent_types:
                _filtered.append(passage)

        elif answer_type == AnswerType.NUM_dist or answer_type == AnswerType.NUM_weight:
            if 'QUANTITY' in named_ent_types:
                _filtered.append(passage)
        
        elif answer_type == AnswerType.HUM_gr:
            if 'ORG' in named_ent_types:
                _filtered.append(passage)

        else:
            _filtered = passages
            break
    return _filtered