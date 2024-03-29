from enum import Enum


#class AnswerType(Enum)_
#    #PERSON = 1
#    #LOCATION = 2
#    ABBR = 1
#    DESC = 2
#    ENTY = 3
#    HUM = 4
#    LOC = 5
#    NUM = 6

class AnswerType(Enum):
    NUM_perc = 1
    ENTY_dismed = 2
    HUM_title = 3
    DESC_def = 4
    NUM_other = 5
    ENTY_religion = 6
    NUM_weight = 7
    ENTY_food = 8
    ENTY_animal = 9
    ENTY_cremat = 10
    ENTY_plant = 11
    NUM_temp = 12
    ENTY_sport = 13
    NUM_speed = 14
    ENTY_event = 15
    NUM_date = 16
    ABBR_abb = 17
    ENTY_word = 18
    NUM_count = 19
    ENTY_currency = 20
    LOC_mount = 21
    LOC_city = 22
    DESC_manner = 23
    ENTY_body = 24
    HUM_desc = 25
    ENTY_product = 26
    NUM_money = 27
    DESC_desc = 28
    ENTY_lang = 29
    ENTY_instru = 30
    NUM_code = 31
    ENTY_color = 32
    NUM_period = 33
    NUM_volsize = 34
    ENTY_symbol = 35
    NUM_ord = 36
    HUM_gr = 37
    ENTY_letter = 38
    NUM_dist = 39
    HUM_ind = 40
    ENTY_veh = 41
    LOC_state = 42
    LOC_other = 43
    ENTY_termeq = 44
    ENTY_substance = 45
    ABBR_exp = 46
    DESC_reason = 47
    ENTY_other = 48
    LOC_country = 49
    ENTY_techmeth = 50

    UNKNOWN = 51
