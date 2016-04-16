import csv
import re

def slugify(value):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to underscores.
    """
    import unicodedata
    value = unicodedata.normalize('NFKD', value).encode('ascii',
            'ignore').decode("utf-8")
    value = re.sub('[^\w\s-]', '', value, flags=re.U).lower()
    value = re.sub('[-\s]+', '_', value, flags=re.U)
    return value

#Reads file and stripps whitespace at the end
#It also slugifies header
with open("./data/kraje-avtomobilov.csv", "r") as f, \
    open("./data/kraje-avtomobilov_clean.csv", "w") as w:
    #reader = csv.DictReader(f)
    reader = csv.reader(f)
    writer = csv.writer(w, quoting=csv.QUOTE_NONNUMERIC)
    first = True
    for row in reader:
        #print (row)
        stripped = [x.strip() for x in row]
        if first:
            stripped = [slugify(x) for x in stripped]
        writer.writerow(stripped)
        first = False
        #break


