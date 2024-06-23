import sys
import csv_parser
from logger_config import setup_logger
from  bisect import bisect_left
log = setup_logger(__name__)


def get_cols(row):
    return row[1:]

def split_transactions(row):
    def s2f(num):
        if num == '':
            return 0.0
        return float(num)
    # assume line starts with an equals
    data = row[1:]
    data = [x for x in data.split("+")]
    float_vec = []
    for item in data:
        minus_sp = item.split('-')
        float_vec.append(s2f(minus_sp[0]))
        if len(minus_sp) >1:
            float_vec.append(-1*s2f(minus_sp[1]))
    float_vec.sort()
    return float_vec

def parse_extraction(file_path, delim=';'):
    data = {}
    # pull columns
    csv_gen = csv_parser.csv_generator(file_path, ";")
    try:
        col_names = get_cols(next(csv_gen))
    except StopIteration as e: 
        return data
    # build columns
    for mon in col_names:
        if not mon in data:
            data[mon] = {}
    # parse data
    for row in csv_gen:
        for idx in range(len(col_names)):
            data[col_names[idx]][row[0]]=split_transactions(row[idx+1])
    return data 

def flatten_data(data, month):
    mon_expenses = []
    for cat in data[month].keys():
        [mon_expenses.append((expense, cat)) for expense in data[month][cat]]
    mon_expenses = sorted(mon_expenses, key=lambda x:x[0])
    return mon_expenses

def get_cat_from_flat(data, value):
    'Locate the leftmost value exactly equal to x'
    idx = bisect_left(data, (value, ""))
    if idx != len(data) and data[idx][0] == value:
        return data[idx][1] 
    raise ValueError

if __name__ == '__main__':
    if len(sys.argv) != 2:
        log.error('Must provide the csv as the third parameter')
        sys.exit(1)
    f = sys.argv[1]
    data = parse_extraction(f)
    mo_exp = flatten_data(data, 'May')
    print(mo_exp)


#    print(data)