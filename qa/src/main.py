from qa_process_impl import process_answer_question
from argparse import ArgumentParser
from ui import twitter_daemon

parser = ArgumentParser(description="Jarvis (Question Answering System)")
parser.add_argument("--twitter", help="set this option to start the app by the twitter daemon",
                    action="store_true")
args = parser.parse_args()

if args.twitter:
    twitter_daemon.start_daemon()
else:
    while True:
        question = input('Enter a question: ')
        answer = process_answer_question(question)
        print('Answer: ' + answer)
        print()
        print()
