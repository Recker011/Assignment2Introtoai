import unittest
from Algorithms.TruthTable import TruthTable
from Sentence import Sentence


class TestTruthTable(unittest.TestCase):
    
    def test_TruthTable_SentenceParse_HornClause_TRUE(self):
        kb, query = Sentence.parse('Test-Files/test_HornKB.txt')
        result = TruthTable.check(kb, query)
        self.assertEqual(result, 'YES:3')
        
    def test_TruthTable_SentenceParse_HornClause_FALSE(self):
        kb, query = Sentence.parse('Test-Files/test_HornKBF.txt')
        result = TruthTable.check(kb, query)
        self.assertEqual(result, 'NO')
        

if __name__ == '__main__':
    unittest.main()
