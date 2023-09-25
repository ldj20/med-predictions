from neo4j import GraphDatabase
from py2neo import Graph
from datetime import datetime;
import sys
sys.path.append("/Users/lawrencejiang/Med-Predictions")
from config import Common

class NeoGraph:

    def __init__(self, uri, user, password):
        self.driver = Graph(uri, auth=(user, password))
        
    def rename(self, year):
        query = "CALL apoc.periodic.iterate(\"MATCH (pub:Publication) WHERE pub.year=$year RETURN pub\", \""
        end_query = "\", {batchSize:1000, params:{year:$year}}) YIELD batches, total RETURN batches, total"
        #query = "MATCH (pub:Publication) WHERE p.lens_id=$pid MATCH (authors:Author)-[:AUTHORED]->(pub) WHERE authors[$authors_prop] IS NOT NULL SET pub[$prop_name] = 1.0*SUM(authors[$authors_prop])/COUNT(AUTHORS)"
        end = 6
        if year > Common.end_year-6:
            end = Common.end_year-year
        #build query
        for i in range(0, end):
            new_name_rp = "rescaled_pagerank" + str(i)
            old_name_rp = "rescaled_pagerank" + str(year + i)
            if (i != 0):
                #need to use WITH between SET and MATCH clauses
                query += "WITH pub "
            query += f"SET pub.{new_name_rp} = pub.{old_name_rp} "
        for i in range(0, end):
            new_name_nv = "node2vec" + str(i)
            old_name_nv = "node2vec" + str(year + i)
            query += f"WITH pub SET pub.{new_name_nv} = pub.{old_name_nv} "
        query += end_query
        self.driver.run(query, year=year)

if __name__ == "__main__":
    database = NeoGraph("bolt://localhost:7687", "neo4j", "asdfqwer")
    for year in range(Common.start_year, Common.end_year):
        print(year)
        database.rename(year)
