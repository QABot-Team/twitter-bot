# twitter-bot [![Build Status](https://travis-ci.org/QABot-Team/twitter-bot.svg?branch=master)](https://travis-ci.org/QABot-Team/twitter-bot)

Simple knowledge based question answering system for factoid questions with the help of wikipedia.

## Getting started

First clone our repository:

    git clone --depth 1 https://github.com/QABot-Team/twitter-bot.git --branch master --single-branch
    
Switch to the main project directory and install all dependencies:

    cd twitter-bot/qa
    ./install.sh

Then you can run our application with the following command:

    python src/main.py [--help]
    
## External dependencies

The application requires a running elastic search instance with a indexed wikipedia dump. Host, port and index name of
the elastic instance can be configured in our [`config.py`](./qa/src/config.py).

## Running tests

To write test cases we use the python [unittest](https://docs.python.org/3/library/unittest.html) framework.
To run our tests simply execute the following command:

    python setup.py test

This uses [pytest](https://docs.pytest.org/en/latest/contents.html) as test runner. If `pytest` is not installed
it will be downloaded automatically.


## Logging

For logging we use the `Logger` facade class which internal uses the [python logger module](https://docs.python.org/3.6/library/logging.html).
Our facade automatically adds the module name from which the log message was created.

Example:

    from utils.logger import Logger
    Logger.info('Start answer processing pipeline')

We use different log level for different purposes.

| **Level** | **When it’s used**                                                                                                                                                     | **Method call**          |
|-----------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------|
| DEBUG     | Detailed information, typically of interest only when diagnosing problems.                                                                                             | Logger.debug(message)    |
| INFO      | Confirmation that things are working as expected.                                                                                                                      | Logger.info(message)     |
| WARNING   | An indication that something unexpected happened, or indicative of some problem in the near future (e.g. ‘disk space low’). The software is still working as expected. | Logger.warning(message)  |
| ERROR     | Due to a more serious problem, the software has not been able to perform some function.                                                                                | Logger.error(message)    |
| CRITICAL  | A serious error, indicating that the program itself may be unable to continue running.                                                                                 | Logger.critical(message) |


## Link collection

* To learn more about question answering have a look at [21 - 1 - What is Question Answering-NLP-Dan Jurafsky & Chris Manning](https://www.youtube.com/watch?v=DAHZPL6voc4) or the whole draft about [Speech and Language Processing](https://web.stanford.edu/~jurafsky/slp3/).
* [START](http://start.csail.mit.edu/index.php) is another question answering system developed by the [MIT InfoLab](https://groups.csail.mit.edu/infolab/index.html). How the system works is superficially explained [here](https://groups.csail.mit.edu/infolab/projects.html).
* [yodaqa](https://github.com/brmson/yodaqa) is a further question answering system developed in python which is unfortunately currently not working since the necessary services provided by the auther are not reachable at the moment (see [issue #73](https://github.com/brmson/yodaqa/issues/73)).
