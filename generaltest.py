from Sentence import Sentence
from KB import KB
import sys

def parse_input_file(filename):
    try:
        with open(filename, 'r') as f:
            lines = f.read().splitlines()
            lines = [line.replace(' ', '').strip() for line in lines]
            tell_list, ask_list = lines[1].split(';'), lines[3].split(';')
            tell, ask = list(filter(None, tell_list)), list(filter(None, ask_list))
            kb = KB()
            for sentence in tell:
                kb.tell(sentence)
            query = Sentence(ask[0])
            return kb, query
    except FileNotFoundError:
        # Error handling for file not found
        print(f"Error: file {filename} not found.")
        sys.exit(1)
    except IndexError:
        # error handling for wrong formatting of input text
        print(f"Error: file {filename} is not in the correct format.")
        sys.exit(1)

kb, query = parse_input_file('test_HornKB.txt')
print('Knowledge base:', kb.get_clauses)
print('Query:', query)


