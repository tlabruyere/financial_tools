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

    def __init__(self, transDate, postDate, desc, category, type, ammount, memo):

        #print(type(transDate))

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

def read_chase_transaction_csv(filePath):
    trans = []
    with open(filePath, newline='') as csvfile:
        transaction_reader = csv.reader(csvfile, delimiter=',')
        next(transaction_reader, None) #skip header
        for row in transaction_reader:
            trans.append(Chase_Transaction(row))
    return trans