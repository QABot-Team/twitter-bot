#!/bin/sh

pip install -r requirements.txt
pip install http://download.pytorch.org/whl/cu80/torch-0.3.1-cp36-cp36m-linux_x86_64.whl
pip install torchvision
python3 -m spacy download en
python3 -m nltk.downloader all
python3 -m spacy download en_core_web_lg