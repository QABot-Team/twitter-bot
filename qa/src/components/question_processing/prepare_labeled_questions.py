from pipeline import get_doc, get_wh_word


def prepare_coarse():
    file = open("test_questions.label", "r")
    file_first_lvl = open("test_first_lvl.label", "w+")

    for line in file:
        words = line.split()
        first_lvl_label, second_lvl_label = words[0].split(":")
        #print(first_lvl_label)
        words.pop(0)
        words = [first_lvl_label] + words
        #print(words)
        line_first_lvl = ' '.join(words)
        file_first_lvl.write(line_first_lvl + "\n")
        #break

def prepare_fine(wh_words):
    for wh_word in wh_words:
        file = open("train_5500.label", "r")
        file_fine = open(wh_word + "_questions.label", "w+")

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

#prepare_fine(["what", "which", "when","how" , "who", "where", "why"])

prepare_coarse()