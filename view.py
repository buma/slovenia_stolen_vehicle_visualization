import dataset
db = dataset.connect('sqlite:///kraje.db')

table = db['kraje']
#naselja = table.distinct('tekst_ceste_naselja')
#Vse kraje iz Maribora:
#result = db.query('SELECT * FROM kraje WHERE tekst_ceste_naselja == "MARIBOR"')
#dataset.freeze(result, format='json', filename='maribor.json')

#Kraje iz maribora grupirane po ulicah
#result = db.query('SELECT leto_odtujitve, count(leto_odtujitve) as cnt,
        #tekst_odseka_ulice FROM kraje WHERE tekst_ceste_naselja == "MARIBOR"
        #GROUP BY tekst_odseka_ulice, leto_odtujitve')
#dataset.freeze(result, format='json', filename='maribor_group.json')

#all street names in MB
#result = db.query('SELECT distinct(tekst_odseka_ulice) FROM kraje WHERE
        #tekst_ceste_naselja == "MARIBOR"')
