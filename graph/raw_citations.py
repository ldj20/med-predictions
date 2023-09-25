from neo4j import GraphDatabase
from py2neo import Graph
import timeit
import csv

class NeoGraph:

    def __init__(self, uri, user, password):
        self.driver = Graph(uri, auth=(user, password))

    def calc(self, lens_id, publish_year):
        for i in range(publish_year, 2021):
            print(i)
            query = "MATCH (p:Publication{lens_id:$lens_id}) MATCH (cited:Publication{year:$yoi})-[:CITES]->(p) RETURN cited"
            res = self.driver.run(query, lens_id=lens_id, yoi=i)
            while (res.forward()):
                print(res.current)

if __name__ == "__main__":
    database = NeoGraph("bolt://localhost:7687", "neo4j", "asdfqwer")
    with open("./ids3.csv", "r") as file:
        reader = csv.reader(file, delimiter='|')
        counter = 0
        overall = 0
        for row in reader:
            overall += timeit.timeit(lambda: database.calc(row[0],int(row[1])), number=1)
            counter += 1
            if (counter == 100):
                break
        print(overall)