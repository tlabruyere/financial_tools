import unittest

from transactions import Transaction_Mgr, Transaction
from categorize import categorize_it, gen_category_from_transactions

class Test_Categorize(unittest.TestCase):

    def _build_trans_mgr(self, trans_tup) -> Transaction_Mgr:
        trans = Transaction(*trans_tup)
        trans_mgr = Transaction_Mgr()
        trans_mgr.add(trans)
        return trans_mgr

    def setUp(self):

        pass

    def test_categorize_it(self):
        amount = 1337
        trans_mgr = self._build_trans_mgr((
            '01/01/1901', 
            '01/01/1901',
            'test_01_desc',
            'test_01_category',
            'test_01_type',
            -1*amount,
            'test_01_memo',
        ))
        flat_data = [(amount, 'Groceries')]
        count = categorize_it(flat_data, trans_mgr)
        self.assertEqual(count, 0)

    def test_gen_category_from_transactions(self):
        amount = 1337
        trans_mgr = self._build_trans_mgr((
            '01/01/1901', 
            '01/01/1901',
            'test_01_desc',
            'test_01_category',
            'test_01_type',
            -1*amount,
            'test_01_memo',
        ))
        trans_mgr.get_transactions_by_desc('test_01_desc')[0].label = 'Groceries'
        categorized = gen_category_from_transactions(trans_mgr)
        expect = {
           'Groceries': [-1*amount]
        }
        self.assertEqual(categorized, expect)


if __name__ == '__main__':
    unittest.main()