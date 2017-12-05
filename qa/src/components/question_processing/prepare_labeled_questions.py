from lib import get_doc, get_wh_word


def prepare_coarse():
    file = open("labeled_questions/train_5500.label", "r")
    file_first_lvl = open("labeled_questions/train_5500_second_lvl.label", "w+")

    for line in file:
        words = line.split()
        first_lvl_label, second_lvl_label = words[0].split(":")
        words.pop(0)
        words = [second_lvl_label] + words
        line_first_lvl = ' '.join(words)
        file_first_lvl.write(line_first_lvl + "\n")

def prepare_fine(wh_words):
    for wh_word in wh_words:
        file = open("labeled_questions/train_5500.label", "r")
        file_fine = open("labeled_questions/" + wh_word + "_questions.label", "w+")

        for line in file:
            doc = get_doc(line)
            _wh_word = get_wh_word(doc)
            if wh_word.lower() != str(_wh_word).lower():
                continue
            words = line.split()
            first_lvl_label, second_lvl_label = words.pop(0).split(":")
            words = [second_lvl_label] + words
            line_second_lvl = ' '.join(words)
            file_fine.write(line_second_lvl + "\n")
        file_fine.close()
        file.close()

def split_fine():
    coarse_classes = ["ABBR", "ENTY", "DESC", "HUM", "LOC", "NUM"]
    for coarse in coarse_classes:
        file = open("labeled_questions/test_questions.label", "r")
        file_fine = open("labeled_questions/" + coarse + "_questions_test.label", "w+")
        for line in file:
            words = line.split()        
            first_lvl_label, second_lvl_label = words[0].split(":")
            if first_lvl_label == coarse:
                words.pop(0)
                words = [second_lvl_label] + words
                line_fine = ' '.join(words)
                file_fine.write(line_fine + "\n")

#prepare_fine(["what", "which", "when","how" , "who", "where", "why"])

#prepare_coarse()

split_fine()

