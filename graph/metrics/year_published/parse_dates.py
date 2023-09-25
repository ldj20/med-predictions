import requests
import json
from neo4j import GraphDatabase
from py2neo import Graph
from dateutil.parser import parse as parseDate
import datetime

class NeoGraph:

    def __init__(self, uri, user, password):
        self.driver = Graph(uri, auth=(user, password))

    def parse_dates(self):
        query = "MATCH (pub:Publication) WHERE id(pub) = 43 RETURN pub.date_published"
        res = self.driver.run(query)
        while (res.forward()):
            date = res.current[0]
            print(type(parseDate(date)))
            #print(datetime.datetime.strptime(date, "%Y-%B-%dT%H:%M:%S-%H:%M").date())

if __name__ == "__main__":
    database = NeoGraph("bolt://localhost:7687", "neo4j", "asdfqwer")
    with open("./pub_identifiers2_1.csv", "r") as pub_identifiers:
        for row in pub_identifiers:    
            database.parse_dates()