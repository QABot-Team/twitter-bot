import os
import shutil
import tarfile
import tempfile

import torch
from allennlp.common import Params
from allennlp.common.file_utils import cached_path
from allennlp.data import Vocabulary

from components.answer_processing.bidaf.read_vocab import VocabReader

_CONFIG_NAME = "config.json"
_WEIGHTS_NAME = "weights.th"
_VOCAB_DIR_NAME = "vocabulary"
_TOKENS_NAME = "tokens.txt"


class ArchiveLoader:

    def __init__(self, url_or_filename):
        self.url_or_filename = url_or_filename
        self.tempdir = ''
        self.config = None
        self.vocabulary = None
        self.vocab_reader = None
        self.model_state = None

        self._load_archive()
        self._load_files()
        self._clean_config()
        self._clean_tmpdir()

    def _load_archive(self):
        archive_file = cached_path(self.url_or_filename)
        self.tempdir = tempfile.mkdtemp()
        with tarfile.open(archive_file, 'r:gz') as archive:
            archive.extractall(self.tempdir)

    def _load_files(self):
        self.config = Params.from_file(os.path.join(self.tempdir, _CONFIG_NAME))
        self.vocabulary = Vocabulary.from_files(os.path.join(self.tempdir, _VOCAB_DIR_NAME))
        self.vocab_reader = VocabReader(os.path.join(self.tempdir, _VOCAB_DIR_NAME, _TOKENS_NAME))
        weights_path = os.path.join(self.tempdir, _WEIGHTS_NAME)
        self.model_state = torch.load(weights_path, map_location=lambda storage, loc: storage)

    def _clean_config(self):
        model_params = self.config.get('model')
        self._remove_pretrained_embedding_params(model_params)
        model_params.pop("type")

    def _clean_tmpdir(self):
        shutil.rmtree(self.tempdir)

    def _remove_pretrained_embedding_params(self, params: Params):
        keys = params.keys()
        if 'pretrained_file' in keys:
            del params['pretrained_file']
        for value in params.values():
            if isinstance(value, Params):
                self._remove_pretrained_embedding_params(value)

    def get_vocabulary(self):
        return self.vocabulary

    def get_vocab_reader(self):
        return self.vocab_reader

    def get_config(self):
        return self.config

    def get_model_state(self):
        return self.model_state
