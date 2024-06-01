import sys
import json
import csv_parser
from logger_config import setup_logger
log = setup_logger(__name__)


def get_cols(row):
    return row[1:]

def parse_extraction(file_path, delim=','):
    data = {}
    # pull columns
    csv_gen = csv_parser.csv_generator(file_path, ";")
    try:
        col_names = get_cols(next(csv_gen))
    except StopIteration as e: 
        return data
    # parse data
    for row in csv_gen:
        data[row[0]] = {}
        for idx in range(len(col_names)):
            data[row[0]][col_names[idx]]=row[idx+1]
    return data 

if __name__ == '__main__':
    if len(sys.argv) != 2:
        log.error('Must provide the csv as the third parameter')
        sys.exit(1)
    f = sys.argv[1]
    data = parse_extraction(f, delim=";")