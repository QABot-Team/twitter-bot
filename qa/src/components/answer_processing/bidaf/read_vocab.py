class VocabReader:

    def __init__(self, vocab_file: str):
        self.vocab_file = vocab_file
        self.vocab_dict = {}
        self._read_file()

    def _read_file(self):
        with open(self.vocab_file) as fp:
            line = fp.readline()
            cnt = 1
            while line:
                token = line.strip()
                self.vocab_dict[token] = cnt
                line = fp.readline()
                cnt += 1

    def get_token_index(self, token: str):
        token = token.lower()
        if token in self.vocab_dict:
            return self.vocab_dict[token]
        else:
            return 1
