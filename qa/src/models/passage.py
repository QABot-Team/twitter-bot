import math

class Passage:
    def __init__(self, text, nlptoolkit) -> None:
        self.text = text
        self.score = 0
        self.nlptoolkit = nlptoolkit
        self.bins = 2
        self.passage_overlap = 1

    def num_sentences(self):
        return 0

    def get_sentences(self):
        return self.nlptoolkit.text_to_sentences(self.text)
    
    def split_passage(self):
        sentences = self.get_sentences()
        if len(sentences) == 1:
            return [Passage(sentences[0], self.nlptoolkit)]

        elif len(sentences) == 2:
            return [Passage(sentences[0], self.nlptoolkit), Passage(sentences[1], self.nlptoolkit)]
            
        elif self.bins > len(sentences):
            # erste passagen +1
            num_el_per_bin = math.floor((self.bins * self.passage_overlap + len(sentences)) / len(sentences) )
        #1 2
        #2 3
        #3 4
        #4 5


        # 1 2 3
        # 2 3 4

        # 1 2 
        # 2 3
        # 3 4
        # 4 5
        # 5 6
        # 6 7

        # 1 2
        # 2 3
        # 3 4

        #1 2 3
        #3 4 5