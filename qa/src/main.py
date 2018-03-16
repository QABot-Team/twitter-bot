from qa_process_impl import process_answer_question
from argparse import ArgumentParser
from ui import twitter_daemon
from utils.logger import Logger

parser = ArgumentParser(description="Jarvis (Question Answering System)")
parser.add_argument("--twitter", help="set this option to start the app by the twitter daemon",
                    action="store_true")
parser.add_argument("--log", help="set the log level threshold",
                    default="info", type=str, choices=["debug", "info", "warning", "error", "critical"])
parser.add_argument("--logfile", help="name for the logfile",
                    default="", type=str)

args = parser.parse_args()

Logger.config(args.log, args.logfile)

if args.twitter:
    twitter_daemon.start_daemon()
else:
    while True:
        question = input('Enter a question: ')
        answer = process_answer_question(question)
        print('Answer: ' + answer)
        print()
        print()
