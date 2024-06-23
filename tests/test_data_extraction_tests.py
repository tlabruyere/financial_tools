import unittest

from data_extraction import split_transactions



class Test_DataExtraction(unittest.TestCase):
    def setUp(self):
        pass

    def test_split_transaction(self):
        """
        test split transactions
        """
        data = '=99.96-37.95+229.03+92.16'
        result = split_transactions(data)
        expect = [-37.95, 92.16, 99.96, 229.03]
        self.assertEqual(result, expect)
        
        data = '=99.96-0+229.03+92.16'
        result = split_transactions(data)
        expect = [0, 92.16, 99.96, 229.03]
        self.assertEqual(result, expect)

        data = ''
        result = split_transactions(data)
        expect = [0.0]
        self.assertEqual(result, expect)

if __name__ == '__main__':
    unittest.main()