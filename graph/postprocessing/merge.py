from neo4j import GraphDatabase
from py2neo import Graph
import timeit

class NeoGraph:

    def __init__(self, uri, user, password):
        self.driver = Graph(uri, auth=(user, password))

    def merge_authors(self, limit):
        query =  "MATCH (n:Author) WHERE n.orcid IS NOT NULL WITH n.orcid as orcid, COLLECT(n) AS ns WHERE size(ns) > 1 CALL apoc.refactor.mergeNodes(ns, {mergeRels:true, properties:{affiliations:\"combine\",first_name:\"discard\",last_name:\"discard\",initials:\"discard\",orcid:\"discard\"}}) YIELD node RETURN node"
        self.driver.run(query)

if __name__ == "__main__":
    database = NeoGraph("bolt://localhost:7687", "neo4j", "asdfqwer")
    for limit in range(0, 100):
        print(limit)
        #database.merge_authors(1000)
        print(timeit.timeit(lambda: database.merge_authors(15000), number=1))