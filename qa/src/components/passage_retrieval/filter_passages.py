from models.answer_type import AnswerType

"""
    DEF = 9
    COLOR = 10
    REASON = 11
    MANNER = 12
    EXP = 13
    VOLSIZE = 16
    SYMBOL = 18
    DISMED = 22
    LETTER = 24
    SUBSTANCE = 28
    WORD = 30
    TERMEQ = 36
    ABB = 39
    OTHER = 40
    DESC = 43
    BODY = 45
    TECHMETH = 46
"""

def filter_passages(passage, answer_type, nlp_toolkit):
    named_ent_types = nlp_toolkit.get_named_enitity_types(passage)
    if answer_type == AnswerType.HUM_ind or answer_type == AnswerType.ENTY_animal or answer_type == AnswerType.HUM_title:
        return 'PERSON' in named_ent_types
    elif answer_type == AnswerType.NUM_date or answer_type == AnswerType.NUM_period:
        return 'DATE' in named_ent_types
    elif answer_type == AnswerType.ENTY_event or answer_type == AnswerType.ENTY_sport:
        return 'EVENT' in named_ent_types
    elif answer_type == AnswerType.LOC_mount:
        return'LOC' in named_ent_types
    elif answer_type == AnswerType.LOC_city or answer_type == AnswerType.LOC_country or answer_type == AnswerType.LOC_state:
        return 'GPE' in named_ent_types
    elif answer_type == AnswerType.NUM_money:
        return 'MONEY' in named_ent_types
    elif answer_type == AnswerType.ENTY_lang:
        return 'LANGUAGE' in named_ent_types
    elif answer_type == AnswerType.ENTY_cremat:
        return 'WORK_OF_ART' in named_ent_types
    elif answer_type == AnswerType.NUM_dist or answer_type == AnswerType.NUM_weight \
         or answer_type == AnswerType.NUM_count or answer_type == AnswerType.NUM_temp \
         or answer_type == AnswerType.NUM_speed:
        return 'QUANTITY' in named_ent_types
    elif answer_type == AnswerType.HUM_gr:
        return 'ORG' in named_ent_types
    elif answer_type == AnswerType.ENTY_plant:
        return 'PLANT' in named_ent_types
    elif answer_type == AnswerType.NUM_ord:
        return 'ORDINAL' in named_ent_types
    elif answer_type == AnswerType.NUM_code:
        return 'CARDINAL' in named_ent_types
    elif answer_type == AnswerType.NUM_perc:
        return 'PERCENT' in named_ent_types
    elif answer_type == AnswerType.ENTY_product or answer_type == AnswerType.ENTY_veh \
        or answer_type == AnswerType.ENTY_food or answer_type == AnswerType.ENTY_instru:
        return 'PRODUCT' in named_ent_types
    elif answer_type == AnswerType.ENTY_religion:
        return 'NORP' in named_ent_types
    return True