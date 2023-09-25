from neo4j import GraphDatabase
from py2neo import Graph
from datetime import datetime;
import sys
sys.path.append("/Users/lawrencejiang/Med-Predictions")
from config import Common

CURR_VAR = "journal_rank"

class NeoGraph:

    def __init__(self, uri, user, password):
        self.driver = Graph(uri, auth=(user, password))
        
    def transfer(self, year, property_key, rank_key):
        query = f"CALL apoc.periodic.iterate(\"MATCH (pub:Publication) WHERE pub.year=$year RETURN pub\", \"MATCH (pub)-[:PUBLISHED_IN]->(n:Journal) "
        end_query = "\", {batchSize:1000, params:{year:$year}}) YIELD batches, total RETURN batches, total"
        #query = "MATCH (pub:Publication) WHERE p.lens_id=$pid MATCH (authors:Author)-[:AUTHORED]->(pub) WHERE authors[$authors_prop] IS NOT NULL SET pub[$prop_name] = 1.0*SUM(authors[$authors_prop])/COUNT(AUTHORS)"
        end = 6
        if year > Common.end_year-6:
            end = Common.end_year-year
        #build query
        for j in range(0, end):
            property_insert = property_key + str(j)
            rank_insert = rank_key + str(year+j)
            if (j != 0):
                #need to use WITH between SET and MATCH clauses
                query += "WITH pub, n "
            query += f"SET pub.{property_insert} = n.{rank_insert} "
        query += end_query
        self.driver.run(query, year=year)
        """end = 2
        if year > Common.end_year-2:
            end = Common.end_year-year
        for j in range(0, end):
            self.driver.run(query, year=year)"""

if __name__ == "__main__":
    database = NeoGraph("bolt://localhost:7687", "neo4j", "asdfqwer")
    for year in range(Common.start_year, Common.end_year):
        print(year)
        database.transfer(year, CURR_VAR, CURR_VAR)
    """with open("./publication_ids.csv", newline='\n') as file:
        reader = csv.reader(file, delimiter=' ', quotechar='|')
        counter = 0
        for row in reader:
            if (counter % 1000 == 0):
                print(counter)
            counter += 1
            lens_id = row[0]
            pub_year = int(row[1])
            database.transfer(lens_id, pub_year, CURR_VAR, CURR_VAR)"""