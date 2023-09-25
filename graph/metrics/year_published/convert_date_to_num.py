import requests
import json

from yaml import parse
from neo4j import GraphDatabase
from py2neo import Graph
from dateutil.parser import parse as parseDate
from datetime import datetime

class NeoGraph:

    def __init__(self, uri, user, password):
        self.driver = Graph(uri, auth=(user, password))

    def convert_date(self, pub_id):
        query = "MATCH (pub:Publication) WHERE pub.lens_id=$pub_id RETURN pub.chosen_date"
        res = self.driver.run(query, pub_id=pub_id)
        while (res.forward()):
            data = res.current
            chosen_date = data.get('pub.chosen_date')
            if (chosen_date):
                int_date = int(datetime.timestamp(parseDate(chosen_date)))
                set_int_date = "MATCH (pub:Publication) WHERE pub.lens_id=$pub_id SET pub.int_chosen_date=$int_date"
                self.driver.run(set_int_date, pub_id=pub_id, int_date=int_date)

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
            database.convert_date(pub_id)
            