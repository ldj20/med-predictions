from neo4j import GraphDatabase
from py2neo import Graph

class NeoGraph:

    def __init__(self, uri, user, password):
        self.driver = Graph(uri, auth=(user, password))

    def create_author_projections(self, num):
        query = "CALL gds.graph.create.cypher($name, 'MATCH (n:Author) WHERE n.age <= $year RETURN id(n) AS id', 'MATCH (n:Author)-[r:COAUTHOR]->(m:Author) WHERE r.year <= $stryear RETURN id(n) AS source, id(m) AS target', {parameters:{name: $name, year:$year, stryear:$stryear}}) YIELD graphName AS graph, nodeQuery, nodeCount AS nodes, relationshipQuery, relationshipCount AS rels"
        self.driver.run(query, name='coauthors'+str(num), year=num, stryear=str(num))
    
    def create_author_weighted_projections(self, num):
        query = "CALL gds.graph.create.cypher($name, 'MATCH (n:Author) WHERE n.age <= $year RETURN id(n) AS id', 'MATCH (n:Author)-[r:COAUTHOR]->(m:Author) WHERE r.year <= $stryear RETURN id(n) AS source, id(m) AS target, r[$weight] AS weight', {parameters:{name: $name, year:$year, stryear:$stryear, weight: $weight}}) YIELD graphName AS graph, nodeQuery, nodeCount AS nodes, relationshipQuery, relationshipCount AS rels"
        self.driver.run(query, name='coauthors'+str(num), year=num, stryear=str(num), weight='weight'+str(num))

    def create_citation_projections(self, num):
        query = "CALL gds.graph.create.cypher($name, 'MATCH (p:Publication) WHERE p.year <= $year RETURN id(p) AS id', 'MATCH (p:Publication)-[r:CITES]->(c:Publication) WHERE r.year <= $year RETURN id(p) AS source, id(c) AS target', {parameters:{name: $name, year:$year}}) YIELD graphName AS graph, nodeQuery, nodeCount AS nodes, relationshipQuery, relationshipCount AS rels"
        self.driver.run(query, name='citations'+str(num), year=num)

if __name__ == "__main__":
    database = NeoGraph("bolt://localhost:7687", "neo4j", "asdfqwer")
    for num in range(1980, 2021):
        print(num)
        database.create_author_projections(num)
        #database.create_citation_projections(num)

"""CALL gds.graph.create.cypher(
  'coauthors2019',
  'MATCH (n:Author) WHERE n.age <= 2019 RETURN id(n) AS id',
  'MATCH (n:Author)-[r:COAUTHOR]->(m:Author) WHERE r.year <= "2019" RETURN id(n) AS source, id(m) AS target')
YIELD graphName AS graph, nodeQuery, nodeCount AS nodes, relationshipQuery, relationshipCount AS rels"""