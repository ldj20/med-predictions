from neo4j import GraphDatabase
from py2neo import Graph
import csv
import math

class NeoGraph:

    def __init__(self, uri, user, password):
        self.driver = Graph(uri, auth=(user, password))

    def write_uw_pagerank(self, year):
        query = "CALL gds.pageRank.write($projection_name, {maxIterations: 20, dampingFactor: 0.85, writeProperty: $str_pagerank}) YIELD nodePropertiesWritten, ranIterations"
        self.driver.run(query, projection_name="coauthors"+str(year), str_pagerank="uw_pagerank"+str(year))

    def read_uw_pagerank(self, year, aid):
        query = "MATCH (a:Author) WHERE id(a)=$aid RETURN a[$str_pagerank]"
        res = self.driver.run(query, aid=aid, str_pagerank="uw_pagerank"+str(year))
        return res

def truncate(number, digits) -> float:
    stepper = 10.0 ** digits
    return math.trunc(stepper * number) / stepper

if __name__ == "__main__":
    database = NeoGraph("bolt://localhost:7687", "neo4j", "asdfqwer")
    with open("../authors_age.csv", newline='\n') as file:
        reader = csv.reader(file, delimiter=' ', quotechar='|')
        for year in range(1980, 2021):
            database.write_uw_pagerank(year)
        with open("./uw_pagerank.csv", "w") as uw_pagerank:
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
                        res = database.read_uw_pagerank(year, aid)
                        w += " " + str(truncate(res.evaluate(), 3))
                uw_pagerank.write(w + "\n")