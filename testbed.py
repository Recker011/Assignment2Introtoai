from TTchecking import TTchecking
from Sentence import Sentence
import sys


def parse_input_file(filename):
    try:
        with open(filename, 'r') as f:
            lines = f.read().splitlines()
            lines = [line.replace(' ', '').strip() for line in lines]
            tell_list, ask_list = lines[1].split(';'), lines[3].split(';')
            tell, ask = list(filter(None, tell_list)), list(filter(None, ask_list))
            kb = [Sentence(sentence) for sentence in tell]
            query = Sentence(ask[0])
            return kb, query
    except FileNotFoundError: # Error handling for file not found
        print(f"Error: file {filename} not found.")
        sys.exit(1)
    except IndexError: # error handling for wrong formatting of input text
        print(f"Error: file {filename} is not in the correct format.")
        sys.exit(1)


def checkparsein():
    line1, line2 = parse_input_file(
        "C:\\Users\\Randew Kumarasinghe\\Desktop\\COS30019\\Assignment2Introtoai\\Assignment2Introtoai\\test.txt"
    )
    print(line1, line2)


def checkTTcheck():
    filename = "test_HornKB.txt"
    print(f"Reading input file: {filename}")
    kb, query = parse_input_file(filename)
   # print(f"kb: {kb}")
   # print(f"query: {query}")
    if not query:
        print("Error: query list is empty")
        return
    tt = TTchecking(kb, query)
    result = tt.check()
    print(result)
    
    
checkTTcheck()




