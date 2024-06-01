import csv

def csv_generator(file_path, delim=','):
    # read csv
    with open(file_path) as f:
        yield from csv.reader(f, delimiter=delim)