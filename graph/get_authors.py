from neo4j import GraphDatabase
from py2neo import Graph

class NeoGraph:

    def __init__(self, uri, user, password):
        self.driver = Graph(uri, auth=(user, password))

    def search(self):
        query = "MATCH (a:Author) RETURN id(a), a.age"
        res = self.driver.run(query)
        with open("./authors_age.csv", "w") as new_file:
            while (res.forward()):
                new_file.write(str(res.current[0]) + " " + str(res.current[1]) + "\n")

if __name__ == "__main__":
    database = NeoGraph("bolt://localhost:7687", "neo4j", "asdfqwer")
    database.search()