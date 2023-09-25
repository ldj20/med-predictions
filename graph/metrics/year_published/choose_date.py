import requests
import json

from yaml import parse
from neo4j import GraphDatabase
from py2neo import Graph
from dateutil.parser import parse as parseDate
import datetime
import pytz

def convert_date_parts(date_parts):
    str_date = str(date_parts[0]) + "-" + str(date_parts[1])
    if (len(date_parts) == 3):
        str_date += "-" + str(date_parts[2])
    else:
        str_date += "-1"
    return parseDate(str_date)

utc=pytz.UTC

class NeoGraph:

    def __init__(self, uri, user, password):
        self.driver = Graph(uri, auth=(user, password))

    def choose_date(self, pub_id):
        query = "MATCH (pub:Publication) WHERE pub.lens_id=$pub_id RETURN pub.date_published, pub.date_published_parts, pub.elsevier_cover_date"
        res = self.driver.run(query, pub_id=pub_id)
        while (res.forward()):
            data = res.current
            date_published = data.get('pub.date_published')
            elsevier_cover_date = data.get('pub.elsevier_cover_date')
            date_published_parts = data.get('pub.date_published_parts')
            parts_arr_len = 0
            if (date_published):
                date_published = parseDate(date_published)
            if (elsevier_cover_date):
                elsevier_cover_date = utc.localize(parseDate(elsevier_cover_date))
            if (date_published_parts and len(date_published_parts) > 1):
                date_published_parts = utc.localize(convert_date_parts(date_published_parts))
            else:
                #should the date parts only have the year, that is too unspecific so the data is excluded
                date_published_parts = None
            chosen_date = date_published
            if (elsevier_cover_date):
                if (not chosen_date or (elsevier_cover_date < chosen_date)):
                    chosen_date = elsevier_cover_date
            if (date_published_parts):
                if (not chosen_date or (date_published_parts < chosen_date)):
                    chosen_date = date_published_parts 

            if (chosen_date):
                chosen_date_str = chosen_date.strftime('%Y-%m-%d')
                set_date = "MATCH (pub:Publication) WHERE pub.lens_id=$pub_id SET pub.chosen_date=$chosen_date"
                self.driver.run(set_date, pub_id=pub_id, chosen_date=chosen_date_str)
            """chosen_date = None
            for date in data:
                print(date)
                print(type(date))
                #print(type(parseDate(date)))
                #print(datetime.datetime.strptime(date, "%Y-%B-%dT%H:%M:%S-%H:%M").date())"""

if __name__ == "__main__":
    database = NeoGraph("bolt://localhost:7687", "neo4j", "asdfqwer")
    counter = 0
    with open("./ids.csv", "r") as pub_identifiers:
        for row in pub_identifiers:
            if (counter%2000 == 0):
                print(counter)
            counter += 1
            arr = row.split("|")
            pub_id = arr[0]
            database.choose_date(pub_id)
            