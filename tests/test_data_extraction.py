import unittest

from data_extraction import split_transactions, get_cat_from_flat



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

        (11*3.25)
        data = ''
        result = split_transactions(data)
        expect = [0.0]
        self.assertEqual(result, expect)

    
    def test_get_cat_from_flat(self):
        data = [(15.13, 'Travel/Experiences (Including Food, Drink on travel)'), (17.38, 'Spotify'), (17.38, 'HBO'), (18.2, 'Pets supplies'), (18.45, 'Shopping'), (20.0, 'Camera payment (Ring+Armcrest)')]
        expect = [(15.13, 'Travel/Experiences (Including Food, Drink on travel)'), (17.38, 'HBO'), (18.2, 'Pets supplies'), (18.45, 'Shopping'), (20.0, 'Camera payment (Ring+Armcrest)')]
        value = 17.38
        label = get_cat_from_flat(data, value)
        print('label: ', label)
        self.assertEqual(label, 'Spotify')
        self.assertEqual(data, expect)

if __name__ == '__main__':
    unittest.main()