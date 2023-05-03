def parse_input_file(filename):
    with open(filename, 'r') as f:
        lines = f.read().splitlines()
        lines = [line.replace(' ', '').strip() for line in lines]
        t, a = lines[1].split(';'), lines[3].split(';')
        tell, ask = list(filter(None, t)), list(filter(None, a))
        return tell, ask
