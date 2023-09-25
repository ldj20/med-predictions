from neo4j import GraphDatabase
from py2neo import Graph
import csv
from datetime import datetime
import math

class NeoGraph:

    def __init__(self, uri, user, password):
        self.driver = Graph(uri, auth=(user, password))

    def cpp(self, yoi, stryoi, aid):
        query = "MATCH (author:Author) WHERE id(author)=$aid MATCH (author)-[AUTHORED]->(pubs:Publication) WHERE pubs.year <= $yoi WITH author, COUNT(pubs) AS total, SUM(pubs[$stryoi]) AS s RETURN 1.0*s/total"
        res = self.driver.run(query, yoi=yoi, stryoi=stryoi, aid=aid)
        return res

def truncate(number, digits) -> float:
    stepper = 10.0 ** digits
    return math.trunc(stepper * number) / stepper
    
if __name__ == "__main__":
    database = NeoGraph("bolt://localhost:7687", "neo4j", "asdfqwer")
    with open("../authors_age.csv", newline='\n') as file:
        reader = csv.reader(file, delimiter=' ', quotechar='|')
        with open("./cpp.csv", "w") as cpp:
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
                        res = database.cpp(year, str(year), aid)
                        w += " " + str(truncate(res.evaluate(), 3))
                cpp.write(w + "\n")