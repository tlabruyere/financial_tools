import csv
import sys
import datetime
from logger_config import setup_logger
log = setup_logger(__name__)

class Transaction:
    _date_format = "%m/%d/%Y"
    _transaction_date = ""
    _post_date = ""
    _description = ""
    _category = ""
    _type = ""
    _amount = ""
    _memo = ""
    _my_category = ""

    def __init__(self, transDate, postDate, desc, category, type, amount, memo):
        self.transaction_date = transDate
        self.post_date = postDate
        self._description = desc
        self._category = category
        self._type = type
        self._amount = amount
        self._memo = memo

    def print(self):
        return 'Transaction Date: ' + datetime.datetime.strftime(self._transaction_date, self._date_format)  + \
            ' Post Date: ' + datetime.datetime.strftime(self._post_date, self._date_format) + \
            ' Desc: ' + self._description + \
            ' Category: ' + self._category + \
            ' Type: ' + self._type + \
            ' Amount: ' + str(self._amount) + \
            ' Memo: ' + self._memo

    @property 
    def transaction_date(self):
        return self._transaction_date
    
    @transaction_date.setter
    def transaction_date(self, value):
        if type(value) == str:
            self._transaction_date = datetime.datetime.strptime(value, self._date_format)
        else:
            self._transaction_date = value

    @property 
    def post_date(self):
        return self._post_date
    
    @post_date.setter
    def post_date(self, value):
        if type(value) == str:
            self._post_date = datetime.datetime.strptime(value, self._date_format)
        else:
            self._post_date = value

    @property 
    def category(self):
        return self._category

    @property 
    def type(self):
        return self._type

    @property 
    def amount(self):
        return self._amount

    @property 
    def memo(self):
        return self._memo

    @property 
    def label(self):
        return self._my_category
    
    @label.setter 
    def label(self, value):
        self.label = value

class Chase_Transaction(Transaction):
    _date_format = "%m/%d/%Y"

    def __init__(self, line):
        super().__init__(
            datetime.datetime.strptime(line[0], self._date_format),
            datetime.datetime.strptime(line[1], self._date_format),
            line[2],
            line[3],
            line[4],
            float(line[5]),
            line[6],
        )

    def _set_transaction(self, data):
        Transaction._transaction_date = datetime.datetime.strptime(data[0], self._date_format)
        Transaction._post_date = datetime.datetime.strptime(data[1], self._date_format)
        Transaction._description = data[2]
        Transaction._category = data[3]
        Transaction._type = data[4]
        Transaction._amount = float(data[5])
        Transaction._memo = data[6]

class Transaction_Mgr(object):
    _transactions_by_desc = None
    _transactions_by_date = None # turn to an ordered dictionary by date
    _total = 0

    def __init__(self):
        self._transactions_by_desc = {}
        self._transactions_by_date = {}

    def _add_by_desc(self, trans: Transaction):
        if not trans._description in self._transactions_by_desc:
            self._transactions_by_desc[trans._description] = []
        self._transactions_by_desc[trans._description].append(trans)
    
    def _add_by_date(self, trans: Transaction):
        if not trans._transaction_date in self._transactions_by_date:
            self._transactions_by_date[trans._transaction_date] = []
        self._transactions_by_date[trans._transaction_date].append(trans)
     
    def add(self, trans: Transaction):
        self._add_by_date(trans)
        self._add_by_desc(trans)
        self._total+=1

    def get_transactions_by_desc(self, key):
        if key in self._transactions_by_desc:
            return self._transactions_by_desc[key]
        raise ValueError
    
    def get_keys_by_desc(self):
        return self._transactions_by_desc.keys()
    
    def get_keys_by_date(self):
        return self._transactions_by_date.keys()

    def get_transactions_by_date(self, key):
        if key in self._transactions_by_date:
            return self._transactions_by_date[key]
        raise ValueError
    # maybe add an interator


def read_chase_transaction_csv(filePath, trans_mgr=None):
    if not trans_mgr:
        trans_mgr = Transaction_Mgr()
    with open(filePath, newline='') as csvfile:
        transaction_reader = csv.reader(csvfile, delimiter=',')
        next(transaction_reader, None) #skip header
        for row in transaction_reader:
            trans_mgr.add(Chase_Transaction(row))
    return trans_mgr

def classify_statement(cur_statement:Transaction_Mgr, 
                       trans_mgr,#: dict<Transaction_Mgr>, 
                       cat_order: list):
    pass

if __name__ == '__main__':
    if len(sys.argv) != 2:
        log.error('Must provide the csv as the third parameter')
        sys.exit(1)
    f = sys.argv[1]
    trans_mgr = read_chase_transaction_csv(f)
    print("tot:" + str(trans_mgr._total) + " num " + str(len(trans_mgr._transactions)))

