# twitter-bot

Simple knowledge based question answering system for factoid questions with the help of wikipedia.

## Project setup

We use [pipenv](https://pypi.python.org/pypi/pipenv) to install project dependencies and manage virtual environments
(where the dependencies will be installed).
To install pipenv simply issue:

    pip install pipenv

Make sure you the terminal points to the directory where the `Pipefile` is located. Then you can install all dependencies
listed in the `Pipfile` by executing

    pipenv install
    pipenv run python -m spacy download en
    pipenv run python -m nltk.downloader all

The latter command downloads the spacy model into the virtual environment.

Now you can execute our application with the following command:

    pipenv run python src/main.py


## Link collection

* To learn more about question answering have a look at [21 - 1 - What is Question Answering-NLP-Dan Jurafsky & Chris Manning](https://www.youtube.com/watch?v=DAHZPL6voc4) or the whole draft about [Speech and Language Processing](https://web.stanford.edu/~jurafsky/slp3/).
* [START](http://start.csail.mit.edu/index.php) is another question answering system developed by the [MIT InfoLab](https://groups.csail.mit.edu/infolab/index.html). How the system works is superficially explained [here](https://groups.csail.mit.edu/infolab/projects.html).
* [yodaqa](https://github.com/brmson/yodaqa) is a further question answering system developed in python which is unfortunately currently not working since the necessary services provided by the auther are not reachable at the moment (see [issue #73](https://github.com/brmson/yodaqa/issues/73)).
