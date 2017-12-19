# twitter-bot

Simple knowledge based question answering system for factoid questions with the help of wikipedia.

## Project setup

We document our dependencies in the [requirements.txt](./requirements.txt) file. To install all dependencies simply
execute the following command:

    pip install -r requirements.txt

To download the necessary data models for spacy and nltk execute the following commands:

    python -m spacy download en
    python -m nltk.downloader all
    python -m spacy download en_core_web_lg

Then you can run our application with the following command:

    python src/main.py [--help]

## Link collection

* To learn more about question answering have a look at [21 - 1 - What is Question Answering-NLP-Dan Jurafsky & Chris Manning](https://www.youtube.com/watch?v=DAHZPL6voc4) or the whole draft about [Speech and Language Processing](https://web.stanford.edu/~jurafsky/slp3/).
* [START](http://start.csail.mit.edu/index.php) is another question answering system developed by the [MIT InfoLab](https://groups.csail.mit.edu/infolab/index.html). How the system works is superficially explained [here](https://groups.csail.mit.edu/infolab/projects.html).
* [yodaqa](https://github.com/brmson/yodaqa) is a further question answering system developed in python which is unfortunately currently not working since the necessary services provided by the auther are not reachable at the moment (see [issue #73](https://github.com/brmson/yodaqa/issues/73)).
