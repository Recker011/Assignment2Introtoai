#import re

class Parse:
    @staticmethod
    def parse(filename):
        with open(filename, 'r') as f:
            lines = f.read().splitlines()
            lines = [line.replace(' ', '').strip() for line in lines]
            t, a = lines[1].split(';'), lines[3].split(';')
            tell, ask = list(filter(None, t)), list(filter(None, a))
        return tell, ask

    @staticmethod
    def is_horn_clause(kb):
        for clause in kb:
            if "=>" in clause:
                if clause.count("&") > 1:
                    return False
            elif "|" in clause:
                return False
        return True

    @staticmethod
    def checktype(filename):
        tell, _ = Parse.parse(filename)
        if Parse.is_horn_clause(tell):
            return "HC"
        else:
            return "GK"