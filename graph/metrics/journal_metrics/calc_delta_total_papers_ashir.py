from neo4j import GraphDatabase
from py2neo import Graph
import csv
from datetime import datetime
import sys
sys.path.append("/Users/lawrencejiang/Med-Predictions")
from config import Common

class NeoGraph:

    def __init__(self, uri, user, password):
        self.driver = Graph(uri, auth=(user, password))
    
    def calc_delta(self, aid, age):
        query = "MATCH (author:Author) WHERE id(author)=$aid MATCH (author)-[:AUTHORED]->(pub:Publication)-[:PUBLISHED_IN]->(journals:Journal) WHERE pub.year <= $year WITH DISTINCT journals RETURN 1.0*SUM(journals[$journal_key])/COUNT(journals)"
        arr = []
        for i in range(age+2, Common.end_year):
            res1 = self.driver.run(query, aid=aid, year=i-2, journal_key="num_papers"+str(i-2))
            res2 = self.driver.run(query, aid=aid, year=i, journal_key="num_papers"+str(i))
            diff = res2.evaluate() - res1.evaluate()
            arr.append(diff)
        return arr
    
if __name__ == "__main__":
    database = NeoGraph("bolt://localhost:7687", "neo4j", "asdfqwer")
    with open("./authors_age.csv", newline='\n') as file:
        reader = csv.reader(file, delimiter=' ', quotechar='|')
        with open("./delta_total_papers.csv", "w") as delta_total_papers:
            i = 0
            for row in reader:
                if (i%1000 == 0):
                    print(i)
                i += 1
                aid=int(row[0])
                age=int(row[1])
                w = str(aid)
                for year in range(1980, 2021):
                    if (year < age):
                        w += " -1"
                    else:
                        break
                res = database.calc_delta(aid, age)
                for num in res:
                   w += " " + str(num)
                delta_total_papers.write(w + "\n")