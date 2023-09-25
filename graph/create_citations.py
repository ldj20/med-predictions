from neo4j import GraphDatabase
from py2neo import Graph
import csv

class NeoGraph:

    def __init__(self, uri, user, password):
        self.driver = Graph(uri, auth=(user, password))

    def create_citations(self):
        with open("./ids.csv", "r") as file:
            reader = csv.reader(file)
            i = 0
            for row in reader:
                print(i)
                i += 1
                query = "MATCH (p:Publication{lens_id:$lens_id}) UNWIND p.citations AS citations MATCH (cited:Publication{lens_id:citations}) MERGE (p)<-[:CITES]-(cited)"
                self.driver.run(query, lens_id=row[0])

if __name__ == "__main__":
    database = NeoGraph("bolt://localhost:7687", "neo4j", "asdfqwer")
    database.create_citations()
    """for limit in range(0, 50):
        print(limit)
        #database.merge_authors(1000)
        print(timeit.timeit(lambda: database.merge_authors(15000), number=1))"""