from neo4j import GraphDatabase
from py2neo import Graph

class NeoGraph:

    def __init__(self, uri, user, password):
        self.driver = Graph(uri, auth=(user, password))

    def search(self):
        query = "MATCH (n:Publication) RETURN n.lens_id, n.year ORDER BY n.year"
        res = self.driver.run(query)
        with open("./ids.csv", "w") as new_file:
            while (res.forward()):
                new_file.write(res.current[0] + "|" +  str(res.current[1]) + "\n")

if __name__ == "__main__":
    database = NeoGraph("bolt://localhost:7687", "neo4j", "asdfqwer")
    database.search()