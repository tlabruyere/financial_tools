import csv
import sys
from logger_config import setup_logger
from transactions import Chase_Transaction, read_chase_transaction_csv
from categorize import categorize_transactions
log = setup_logger(__name__)


if __name__ == '__main__':
    print(sys.argv)
    if len(sys.argv) != 2:
        log.error('Must provide the csv as the third parameter')
        sys.exit(1)
    f = sys.argv[1]
    transactions = read_chase_transaction_csv(f)
    out = categorize_transactions(transactions)

