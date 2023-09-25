from neo4j import GraphDatabase
from py2neo import Graph
import csv
from datetime import datetime

class NeoGraph:

    def __init__(self, uri, user, password):
        self.driver = Graph(uri, auth=(user, password))
        
    def total_papers(self, yoi, aid):
        query = "MATCH (author:Author) WHERE id(author)=$aid MATCH (author)-[:AUTHORED]->(pubs:Publication) WHERE pubs.year <= $yoi RETURN COUNT(pubs)"
        res = self.driver.run(query, yoi=yoi, aid=aid) 
        return res

if __name__ == "__main__":
    database = NeoGraph("bolt://localhost:7687", "neo4j", "asdfqwer")
    with open("../authors_age.csv", newline='\n') as file:
        reader = csv.reader(file, delimiter=' ', quotechar='|')
        with open("./total_papers.csv", "w") as total_papers:
            i = 0
            for row in reader:
                print(i)
                i += 1
                aid=int(row[0])
                age=int(row[1])
                w = str(aid)
                for year in range(1980, 2021):
                    if (year < age):
                        w += " -1"
                    else:
                        res = database.total_papers(year, aid)
                        w += " " + str(res.evaluate())
                total_papers.write(w + "\n")