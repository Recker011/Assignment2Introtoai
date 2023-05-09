from TTchecking import TTchecking
from BackwardChaining import BackwardChaining
from Sentence import Sentence
import sys
import re

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
    KB = []
    algorithm = "TTcheck"
    filename = "test_HornKB.txt"
    print(f"Reading input file: {filename}   |||||   algorithm: {algorithm}")
    kb, query = parse_input_file(filename)
    print(f"kb: {kb}")
    for i in kb:
        KB.append(i.clause)
        print(f'{i.clause}')
        print(f'a: {KB}')
    
    Q = query.clause
    print(f'{query.clause}')
    if not query:
        print("Error: query list is empty")
        return
    tt = TTchecking(kb,query)
    result = tt.check()
    print(result)

def checkBCcheck():
    algorithm = 'BCcheck'
    filename = "input.txt"  # Make sure this is the correct input file
    print(f"Reading input file: {filename}    |||||   algorithm: {algorithm}")
    kb, query = parse_input_file(filename)
    if not query:
        print("Error: query list is empty")
        return
    bc = BackwardChaining(kb, query)
    result = bc.check()
    print(result)

#checkTTcheck()
checkBCcheck()