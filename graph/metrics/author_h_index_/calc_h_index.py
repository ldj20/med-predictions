from neo4j import GraphDatabase
from py2neo import Graph
import csv
from datetime import datetime

class NeoGraph:

    def __init__(self, uri, user, password):
        self.driver = Graph(uri, auth=(user, password))

    def h_index(self, yoi, aid):
        query = "MATCH (author:Author) WHERE id(author)=$aid RETURN author[$h_index]"
        res = self.driver.run(query, h_index="h_index_"+str(yoi), aid=aid)
        return res

if __name__ == "__main__":
    database = NeoGraph("bolt://localhost:7687", "neo4j", "asdfqwer")
    with open("../authors_age.csv", newline='\n') as file:
        reader = csv.reader(file, delimiter=' ', quotechar='|')
        with open("./author_h_index.csv", "w") as author_h_index:
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
                        res = database.h_index(year, aid)
                        w += " " + str(res.evaluate())
                author_h_index.write(w + "\n")