import csv
import sys
import datetime
import uuid
from logger_config import setup_logger
log = setup_logger(__name__)

class Transaction:
    _unique_id = None
    _date_format = "%m/%d/%Y"
    _transaction_date = ""
    _post_date = ""
    _description = ""
    _category = ""
    _type = ""
    _amount = ""
    _memo = ""
    _my_category = None

    def __init__(self, transDate, postDate, desc, category, type, amount, memo):
        self._unique_id  = str(uuid.uuid4())
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
    def id(self):
        return self._unique_id

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
    def description(self):
        return self._description

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
        self._my_category = value

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
    _transactions_by_id = None # turn to an ordered dictionary by date
    _total = 0

    def __init__(self):
        self._transactions_by_desc = {}
        self._transactions_by_date = {}
        self._transactions_by_id = {}

    #TODO: Rewrite this dicionary save to be 1 func where we pass the dictionary
    def _add_by_desc(self, desc: str, unique_id: str):
        if not desc in self._transactions_by_desc:
            self._transactions_by_desc[desc] = []
        self._transactions_by_desc[desc].append(unique_id)
    # 
    def _add_by_date(self, date: datetime, unique_id: str):
        if not date in self._transactions_by_date:
            self._transactions_by_date[date] = []
        self._transactions_by_date[date].append(unique_id)
    
    def update_trans(self, id: str, trans: Transaction):
        if not id in self._transactions_by_id:
            raise ValueError
        self._transactions_by_id[id] = trans

    def set_label_by_id(self, id, value):
        if not id in self._transactions_by_id:
            raise ValueError
        self._transactions_by_id[id].label = value
     
    def add(self, trans: Transaction):
        self._add_by_date(trans.transaction_date, trans.id)
        self._add_by_desc(trans.description, trans.id)
        self._transactions_by_id[trans.id] = trans
        self._total+=1 

    def get(self, key):
        if key in self._transactions_by_id:
            return self._transactions_by_id[key]
        raise ValueError

    def get_transactions_by_desc(self, key):
        if key in self._transactions_by_desc:
            return [self._transactions_by_id[x] for x in self._transactions_by_desc[key]]
        raise ValueError
    
    def get_keys_by_desc(self):
        return self._transactions_by_desc.keys()
    
    def get_keys_by_date(self):
        return self._transactions_by_date.keys()
    
    def get_keys(self):
        return self._transactions_by_id.keys()

    def get_transactions_by_date(self, key):
        if key in self._transactions_by_date:
            return [self._transactions_by_id[x] for x in self._transactions_by_date[key]]
        raise ValueError
    # maybe add an interator

def add_combine_transaction_mgr(out: Transaction_Mgr, combine: Transaction_Mgr):
    '''
    Desc: takes two transaction managers and combines it into one where out will contain all the data
    '''
    for trans_desc in combine.get_keys_by_desc():
        for trans in combine.get_transactions_by_desc(trans_desc):
            out.add(trans)
    return out

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

