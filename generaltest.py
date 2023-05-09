from Sentence import Sentence

def parse_input_file(filename):
    with open(filename, 'r') as f:
        lines = f.read().splitlines()
        tell_line = lines[1].strip()
        ask_line = lines[3].strip()
        tell_sentences = tell_line.split(';')
        ask_sentence = ask_line
        kb = [Sentence(sentence).cnf for sentence in tell_sentences if sentence]
        query = Sentence(ask_sentence).cnf
        return kb, query

kb, query = parse_input_file('test_genericKB.txt')
print('Knowledge base:', kb)
print('Query:', query)