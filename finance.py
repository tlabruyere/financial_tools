import sys
import argparse

from logger_config import setup_logger
from transactions import Transaction_Mgr, read_chase_transaction_csv
from categorize import Category_Mgr
from data_extraction import parse_extraction
log = setup_logger(__name__)

def categorize_transactions(
        trans_mgr: Transaction_Mgr, 
        cat_mgr: Category_Mgr,
        data: dict,
        ):
    for key in trans_mgr._transactions.keys():
        for item in trans_mgr._transactions[key]:
            print(item.print())

def main(transactions_file, training_file, categories_file):
    transactions_mgr = read_chase_transaction_csv(transactions_file)
    cat_data = parse_extraction(training_file)
    cat_mgr = Category_Mgr(categories_file)
    out = categorize_transactions(transactions_mgr, cat_mgr, cat_data)


if __name__ == '__main__':
    if len(sys.argv) <= 2:
        log.error('Must provide the csv as the third parameter')
        sys.exit(1)
    transactions_file = sys.argv[1]
    training_file = sys.argv[2]
    categories_file = sys.argv[3]
    main(transactions_file, training_file, categories_file)
