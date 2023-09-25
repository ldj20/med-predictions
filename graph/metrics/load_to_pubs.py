from neo4j import GraphDatabase
from py2neo import Graph
from datetime import datetime;
import sys
sys.path.append("/Users/lawrencejiang/Med-Predictions")
from config import Common

variables = [
]
curr_variables = [
    "journal_papers_delta"
]

#CURR_VAR = ""
finished_variables = [
    "cpp",
    "dcpp",
    "cpy",
    "max_citations",
    "author_rank",
    "total_citations",
    "dtotal_citations",
    "total_papers",
    "dtotal_papers",
    "citations",
    "adopters",
    "age",
    "h_index_",
    "dh_index_",
    "recent_coauthors",
    "dmean_journal_citations",
    "mean_journal_citations",
    "djournal_hindex",
    "journal_hindex",
    "journal_max_citations",
    "journal_rank",
    "num_journals",
    "papers_per_journal",
    "node2vec",
    "rescaled_pagerank",
    "uw_pagerank",
    "w_pagerank"
]

class NeoGraph:

    def __init__(self, uri, user, password):
        self.driver = Graph(uri, auth=(user, password))
        
    def transfer(self, year, property_key, authors_prop):
        query = "CALL apoc.periodic.iterate(\"MATCH (pub:Publication) WHERE pub.year=$year RETURN pub\", \""
        end_query = "\", {batchSize:1000, params:{year:$year}}) YIELD batches, total RETURN batches, total"
        #query = "MATCH (pub:Publication) WHERE p.lens_id=$pid MATCH (authors:Author)-[:AUTHORED]->(pub) WHERE authors[$authors_prop] IS NOT NULL SET pub[$prop_name] = 1.0*SUM(authors[$authors_prop])/COUNT(AUTHORS)"
        end = 6
        if year > Common.end_year-6:
            end = Common.end_year-year
        #build query
        for j in range(0, end):
            authors_insert = "'" + authors_prop + str(year+j) + "'"
            property_insert = "'" + property_key + str(j) + "'"
            if (j != 0):
                #need to use WITH between SET and MATCH clauses
                query += "WITH pub "
            query += f"OPTIONAL MATCH (authors:Author)-[:AUTHORED]->(pub) WHERE authors[{authors_insert}] IS NOT NULL WITH authors, pub, authors[{authors_insert}] AS metric, {{}} AS props WITH pub, props, CASE COUNT(authors) WHEN 0 THEN 0.0 ELSE 1.0*SUM(metric)/COUNT(authors) END AS value WITH pub, apoc.map.setKey(props, {property_insert}, value) as props SET pub += props "
        query += end_query
        self.driver.run(query, year=year)
        """end = 2
        if year > Common.end_year-2:
            end = Common.end_year-year
        for j in range(0, end):
            self.driver.run(query, year=year)"""

if __name__ == "__main__":
    database = NeoGraph("bolt://localhost:7687", "neo4j", "asdfqwer")
    for CURR_VAR in curr_variables:
        print(CURR_VAR)
        for year in range(Common.start_year, Common.end_year):
            print(year)
            database.transfer(year, CURR_VAR, CURR_VAR)