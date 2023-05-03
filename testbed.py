def parse_input_file(filename):
    with open(filename, 'r') as f:
        lines = f.read().splitlines()
        tell = lines[1]
        ask = lines[4]
        return tell, ask

def checkparsein():
    line1, line2 = parse_input_file("C:\\Users\\Randew Kumarasinghe\\Desktop\\COS30019\\Assignment2Introtoai\\Assignment2Introtoai\\test.txt")
    print(line1, line2)
    
checkparsein()