from neo4j import GraphDatabase
from py2neo import Graph
import csv
from datetime import datetime
import math
import sys
sys.path.append("/Users/lawrencejiang/Med-Predictions")
from config import Common

class NeoGraph:

    def __init__(self, uri, user, password):
        self.driver = Graph(uri, auth=(user, password))
    
    def calc_delta(self, aid, age):
        query = "MATCH (author:Author) WHERE id(author)=$aid MATCH (author)-[:AUTHORED]->(pub:Publication)-[:PUBLISHED_IN]->(journals:Journal) WHERE pub.year <= $year WITH DISTINCT journals RETURN 1.0*SUM(journals[$journal_key])/COUNT(journals)"
        for i in range(age+2, Common.end_year):
            res1 = self.driver.run(query, aid=aid, year=i-2, journal_key="num_papers"+str(i-2))
            res2 = self.driver.run(query, aid=aid, year=i, journal_key="num_papers"+str(i))
            author_insert = "journal_papers_delta" + str(i)
            diff = res2.evaluate() - res1.evaluate()
            set_delta = f"MATCH (author:Author) WHERE id(author)=$aid SET author.{author_insert} = {diff}"
            self.driver.run(set_delta, aid=aid)
        """for i in range(age, Common.end_year):
            author_insert = "djournal_papers" + str(i)
            query = f"MATCH (author:Author) WHERE id(author)=$aid MATCH (author)-[:AUTHORED]->(pub:Publication)-[:PUBLISHED_IN]->(journals:Journal) WHERE pub.year <= $year WITH DISTINCT journals RETURN 1.0*SUM(journals[$journal_key])/COUNT(journals)"        
            res = self.driver.run(query, aid=aid, year=i, journal_key = "num_papers"+str(i))
            val = res.evaluate()
            insert = f"MATCH (author:Author) WHERE id(author)=$aid SET author.{author_insert} = {val}"
            self.driver.run(insert, aid=aid)"""
    
if __name__ == "__main__":
    database = NeoGraph("bolt://localhost:7687", "neo4j", "asdfqwer")
    with open("../authors_age_load2.csv", newline='\n') as file:
        reader = csv.reader(file, delimiter=' ', quotechar='|')
        i = 0
        for row in reader:
            if (i%1000 == 0):
                print(i)
            i += 1
            aid=int(row[0])
            age=int(row[1])
            database.calc_delta(aid, age)