from neo4j import GraphDatabase
from py2neo import Graph
import csv
import math

class NeoGraph:

    def __init__(self, uri, user, password):
        self.driver = Graph(uri, auth=(user, password))

    def write_pub_pagerank(self, year):
        query = "CALL gds.pageRank.write($projection_name, {maxIterations: 20, dampingFactor: 0.85, writeProperty: $str_pagerank}) YIELD nodePropertiesWritten, ranIterations"
        self.driver.run(query, projection_name="citations"+str(year), str_pagerank="pub_pagerank"+str(year))

def truncate(number, digits) -> float:
    stepper = 10.0 ** digits
    return math.trunc(stepper * number) / stepper

if __name__ == "__main__":
    database = NeoGraph("bolt://localhost:7687", "neo4j", "asdfqwer")
    for year in range(1980, 2021):
        print(year)
        database.write_pub_pagerank(year)
    