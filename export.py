from sqlalchemy import engine_from_config
from settings import get_config_dict
from mapping import DBSession, PlanetOsmLine, PlanetOsmPolygon
from geojson import Feature, FeatureCollection, dump, dumps
from sqlalchemy.sql import func
import json

settings = get_config_dict()

engine = engine_from_config(settings, 'sqlalchemy.', echo=True)
planet_engine = engine_from_config(settings, 'osm.', echo=False)
DBSession.configure(binds={
    PlanetOsmLine:planet_engine,
    PlanetOsmPolygon:planet_engine
    })
ses = DBSession


def group(inputfile, outputfile):
    """This reads exported file from dataset.freeze

    Data consists of all the streets in Maribor grouped by streets and years
    Data looks like {"results": [ {"leto_odtujitve":string, "cnt":number,
    "tekst_odseka_ulice": ""}]}

    Output is JSON file with streets in first layer and years with counts in
    second: { "street name":{"year": number of occurences}} 
    """

    d = defaultdict(lambda: defaultdict(int))
    maxSteals = 0
    with open(inputfile, "r") as f:
        json_data = json.load(f)
        for result in json_data["results"]:
            ulica = result["tekst_odseka_ulice"]
            leto = result["leto_odtujitve"]
            stevilo_kraj = result["cnt"]
            d[ulica][leto]=stevilo_kraj
            if stevilo_kraj > maxSteals:
                maxSteals = stevilo_kraj
        d["max_steals"] = maxSteals
    json.dump(d, open(outputfile, "w"))

def get_street_geometries(cache_file):
    """Gets distinct list of all street names from DB

    And for each of street those streets search for same named street in OSM DB

    If it is found geometry geojson part is saved in file based dict keyed as
    street name
    """
    found,missing = (0,0)
    with shelve.open(cache_file) as streets_geo_db:
        db = dataset.connect('sqlite:///kraje.db')
        streets = db.query('SELECT distinct(tekst_odseka_ulice) FROM kraje WHERE ' +
            'tekst_ceste_naselja == "MARIBOR"')
        for street in streets:
            street_name = street["tekst_odseka_ulice"]
            #Skips already inserted streets
            if street_name in streets_geo_db:
                continue
            geo_streets = PlanetOsmLine.get_street(street_name)
            geo = {
                    "type": "GeometryCollection",
                    "geometries": []
                    }
            name = None
            #Geometry collection of all the parts of street with same name in
            #OSM
            for geo_street in geo_streets:
                name = geo_street.name
                geo["geometries"].append(json.loads(geo_street.geodata));
            if (found+missing)%100 == 0:
                print ("O")
            elif (found+missing)%20 == 0:
                print (".")
            #Skips streets which weren't found in geo_streets
            if name is not None:
                streets_geo_db[street_name] = geo
                found +=1
            else:
                missing += 1
        print ("Found {}/{} {.2f}% streets".format(found, found+missing,
            found/(found+missing)*100))

if __name__ == "__main__":
    #from collections import defaultdict
    #group("./maribor_group.json", "./kraje_tmp.json")
    #import dataset
    import shelve
    cache_file = "./streets_maribor_geo"
    #get_street_geometries(cache_file)
    min_year = 2008
    max_year = 2014
    range_years = range(min_year, max_year+1)
    with shelve.open(cache_file) as streets_geo_db, \
            open("./kraje_tmp.json", "r") as city_grouped:
        data = json.load(city_grouped);
        max_steals = data["max_steals"]
        del data["max_steals"]
        features = []
        for street_name, years in data.items():
            geo = None
            if street_name in streets_geo_db:
                geo = streets_geo_db[street_name]
            else:
                continue
            prop = {'name': street_name}
            for year in range_years:
                if str(year) in years:
                    value = years[str(year)]/max_steals*8
                    value_normal = years[str(year)]
                else:
                    value = 0
                    value_normal = 0
                prop["{}_class".format(year)] = value
                prop[year] = value_normal
            print(prop)
            fet = Feature(geometry=geo, properties=prop)
            features.append(fet)
        vse = FeatureCollection(features)
        dump(vse, open("maribor_class.geojson", "w"))
