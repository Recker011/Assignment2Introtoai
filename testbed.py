from TTchecking import TTchecking


def parse_input_file(filename):
    with open(filename, "r") as f:
        lines = f.read().splitlines()
        lines = [line.replace(" ", "").strip() for line in lines]
        t, a = lines[1].split(";"), lines[3].split(";")
        tell, ask = list(filter(None, t)), list(filter(None, a))
        return tell, ask


def checkparsein():
    line1, line2 = parse_input_file(
        "test_genericKB.txt"
    )
    print(line1, line2)


def checkTTcheck():
    kb, query = parse_input_file(
        "test_HornKB.txt"
    )
    tt = TTchecking(kb, query[0])
    result = tt.check()
    print(result)
    

checkparsein()




