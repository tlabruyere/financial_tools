import csv_parser
from transactions import Transaction_Mgr
from logger_config import setup_logger
from data_extraction import get_cat_from_flat
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
    _cat_order = []

    def _load_categories(self, filepath):
        self._categories = {}
        self._cat_order = []
        idx = 0
        for cat in csv_parser.csv_generator(filepath):
            self._categories[cat[0]] = Category(cat[0], cat[1], idx)
            self._cat_order.append(cat[0])
            idx+=1

    def __init__(self, filepath):
        self._load_categories(filepath)
   
    def cat_list(self):
        return self._cat_order

    def get(self, name):
        if name in self._categories:
            return self._categories[name]
        return None

def categorize_it(flat_data, trans_mgr):
    idx = 0
    for key in trans_mgr.get_keys_by_desc():
        for trans in trans_mgr.get_transactions_by_desc(key):
            if trans.label == None:
                try:
                    trans.label = get_cat_from_flat(flat_data, -1*trans._amount)
                except ValueError as e:
                    print("could not find transaction {} for amount: {}".format(trans._description, -1*trans._amount))
                    idx+=1
    # remove 0 from file
    while True:
        try:
            get_cat_from_flat(flat_data, 0.0)
        except:
            break
    return idx

def gen_category_from_transactions(trans_mgr: Transaction_Mgr):
    categorized = {}
    for key in trans_mgr.get_keys_by_desc():
        for trans in trans_mgr.get_transactions_by_desc(key):
            if trans.label not in categorized:
                categorized[trans.label] = []
            categorized[trans.label].append(trans._amount)
    return categorized
    
def print_cat_out(trans_mgr: Transaction_Mgr, cat_order: list):
    lines = []
    categorized = gen_category_from_transactions(trans_mgr)
    for cat in cat_order:
        if cat not in categorized:
            lines.append('{};=0'.format(cat))
        else:
            lines.append('{};='.format(cat) + '+'.join([str(-1*x) for x in categorized[cat]]))
    return lines
    

if __name__ == '__main__':
    cat_mgr = Category_Mgr('categories.csv')
    for cat in cat_mgr.cat_list():
        cur_cat = cat_mgr.get(cat)
        log.info( "key: {} {}".format(cat, cur_cat.print()))