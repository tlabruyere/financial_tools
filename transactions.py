import csv
import sys
import datetime
from logger_config import setup_logger
log = setup_logger(__name__)

class Transaction:
    _transaction_date = ""
    _post_date = ""
    _description = ""
    _category = ""
    _type = ""
    _ammount = ""
    _memo = ""
    _date_format = ""
    _my_category = ""

    def __init__(self, transDate, postDate, desc, category, type, ammount, memo):
        self._transaction_date = transDate
        self._post_date = postDate
        self._description = desc
        self._category = category
        self._type = type
        self._ammount = ammount
        self._memo = memo

    def print(self):
        return 'Transaction Date: ' + datetime.datetime.strftime(self._transaction_date, self._date_format)  + \
            ' Post Date: ' + datetime.datetime.strftime(self._post_date, self._date_format) + \
            ' Desc: ' + self._description + \
            ' Category: ' + self._category + \
            ' Type: ' + self._type + \
            ' Ammount: ' + str(self._ammount) + \
            ' Memo: ' + self._memo

    def set_my_category(self, cat):
        self._my_category = cat

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
        Transaction._ammount = float(data[5])
        Transaction._memo = data[6]

class Transaction_Mgr(object):
    _transactions = None
    _total = 0
    _trans_iter = None

    def __init__(self):
        self._transactions = {}
        self._trans_iter = None
    
    def add(self, trans: Transaction):
        if not trans._description in self._transactions:
            self._transactions[trans._description] = []
        self._transactions[trans._description].append(trans)
        self._total+=1
        #set iterator to beginning, if not set
        if self._trans_iter == None:
            self._trans_iter = self._transactions[trans._description][-1]

    def get_transactions(self, key):
        if key in self._transactions:
            return self._transactions[key]
        raise ValueError

    # maybe add an interator




def read_chase_transaction_csv(filePath):
    trans_mgr = Transaction_Mgr()
    with open(filePath, newline='') as csvfile:
        transaction_reader = csv.reader(csvfile, delimiter=',')
        next(transaction_reader, None) #skip header
        for row in transaction_reader:
            trans_mgr.add(Chase_Transaction(row))
    return trans_mgr

if __name__ == '__main__':
    if len(sys.argv) != 2:
        log.error('Must provide the csv as the third parameter')
        sys.exit(1)
    f = sys.argv[1]
    trans_mgr = read_chase_transaction_csv(f)
    print("tot:" + str(trans_mgr._total) + " num " + str(len(trans_mgr._transactions)))

