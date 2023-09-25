from neo4j import GraphDatabase
from py2neo import Graph
import csv
from datetime import datetime

class NeoGraph:

    def __init__(self, uri, user, password):
        self.driver = Graph(uri, auth=(user, password))
        
    def total_citations(self, yoi, strYoi, aid):
        query = "MATCH (author:Author)-[AUTHORED]->(pubs:Publication) WHERE id(author)=$aid RETURN SUM(pubs[$strYoi])"
        res = self.driver.run(query, yoi=yoi, strYoi=strYoi, aid=aid) 
        return res

if __name__ == "__main__":
    database = NeoGraph("bolt://localhost:7687", "neo4j", "asdfqwer")
    with open("../authors_age.csv", newline='\n') as file:
        reader = csv.reader(file, delimiter=' ', quotechar='|')
        with open("./total_citations.csv", "w") as total_citations:
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
                        res = database.total_citations(year, str(year), aid)
                        w += " " + str(res.evaluate())
                total_citations.write(w + "\n")