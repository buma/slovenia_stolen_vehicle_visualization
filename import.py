import csv
import dataset
db = dataset.connect('sqlite:///kraje.db')


with open("./data/kraje-avtomobilov_clean.csv", "r") as f, \
        db as tx:
    table = tx['kraje']
    reader = csv.DictReader(f)
    for row in reader:
        table.insert(row)
    print (len(table))

