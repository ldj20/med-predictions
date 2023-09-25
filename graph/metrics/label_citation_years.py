from neo4j import GraphDatabase
from py2neo import Graph

class NeoGraph:

    def __init__(self, uri, user, password):
        self.driver = Graph(uri, auth=(user, password))

    #assumes ids.csv is sorted by year low to high
    def label_citations(self):
        query = "CALL apoc.periodic.iterate(\"MATCH (a:Publication)-[r:CITES]->(b:Publication) RETURN a,r\", \"WITH a, r, {} AS props WITH r, apoc.map.setKey(props, 'year', a.year) as props SET r += props\", {batchSize:1000}) YIELD batches, total RETURN batches, total"
        self.driver.run(query)

if __name__ == "__main__":
    database = NeoGraph("bolt://localhost:7687", "neo4j", "asdfqwer")
    database.label_citations()