import csv_parser
from transactions import Transaction_Mgr, read_chase_transaction_csv
from logger_config import setup_logger
log = setup_logger(__name__)

class Category:
    _name = ""
    _type = None
    _load_order = None
    _p_category = None

    def __init__(self, name, type, load_order=None, parent=None):
        self._name = name
        self._type = type
        self._load_order = load_order
        self._p_category = parent
    
    def print(self, delim=" "):
        return "Name: {}{}Type: {}{}Idx: {}{}".format(
            self._name,
            delim,
            self._type, 
            delim,
            self._load_order,
            delim
        )

class Category_Mgr(object):
    _categories = None  # dictionary

    def __init__(self, filepath):
        self.load_categories(filepath)

    def load_categories(self, filepath):
        self._categories = {}
        idx = 0
        for cat in csv_parser.csv_generator(filepath):
            self._categories[cat[0]] = Category(cat[0], cat[1], idx)
            idx+=1
    
    def cat_list(self):
        return self._categories.keys()

    def get(self, name):
        if name in self._categories:
            return self._categories[name]
        return None

if __name__ == '__main__':
    cat_mgr = Category_Mgr('categories.csv')
    for cat in cat_mgr.cat_list():
        cur_cat = cat_mgr.get(cat)
        log.info( "key: {} {}".format(cat, cur_cat.print()))