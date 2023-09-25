from neo4j import GraphDatabase
from py2neo import Graph
import numpy as np

#THIS FUNCTION IS WRONG
def calc_h_index(citations):
    l = len(citations)
    h_index = 0
    for i in range(l):
        num_citations = citations[i]
        if (num_citations <= l-i):
            h_index = num_citations
    return h_index

def h_index_expert(citations):
    citations = np.array(citations)
    n = citations.shape[0]
    array = np.arange(1, n+1)
    # reverse sorting
    citations = np.sort(citations)[::-1]
    # intersection of citations and k
    h_idx = np.max(np.minimum(citations, array))
    return int(h_idx)

class NeoGraph:

    def __init__(self, uri, user, password):
        self.driver = Graph(uri, auth=(user, password))

    def initialize_age(self):
        query = "CALL apoc.periodic.iterate(\"MATCH (author:Author) RETURN author\", \"MATCH (author)-[:AUTHORED]->(pubs:Publication) WITH author, MIN(pubs.year) AS minimum SET author.age=minimum\", {batchSize:1000}) YIELD batches, total RETURN batches, total"
        res = self.driver.run(query)

    #mean citations per year per journal
    def initialize_citations(self, num):
        query = "CALL apoc.periodic.iterate(\"MATCH (author:Author) WHERE author.age <= $yoi RETURN author\", \"OPTIONAL MATCH (author)-[:AUTHORED]->(pubs:Publication) WHERE pubs.year <= $yoi WITH author, pubs, pubs[toString($yoi)] AS s, {} AS props WITH author, apoc.map.setKey(props, $property_key, SUM(1.0*s/($yoi+1-pubs.year))/COUNT(pubs)) as props SET author += props\", {batchSize:1000, params:{yoi:$yoi, property_key:$property_key}}) YIELD batches, total RETURN batches, total"
        res = self.driver.run(query, yoi=1980+num, property_key="cpy"+str(1980+num))

    def initialize_h_index(self, num):
        query = "CALL apoc.periodic.iterate(\"MATCH (a:Author) WHERE a.age<=1980+$num RETURN a\", \"MATCH (a)-[AUTHORED]->(p:Publication) WHERE p.year <= 1980+$num WITH a, p[$yoistr] AS numCitations, {} AS props WITH a, apoc.map.setKey(props, $property_key, metrics.h_index(COLLECT(numCitations))) as props SET a += props\", {batchSize:1000, params:{num:$num, yoistr:$yoistr, property_key:$property_key}}) YIELD batches, total RETURN batches, total"
        res = self.driver.run(query, num=num, yoistr=str(1980+num), property_key="h_index_"+str(1980+num))

    def initialize_num_coauthors(self, num):
        query = "CALL apoc.periodic.iterate(\"MATCH (a:Author) WHERE a.age<=1980+$num RETURN a\", \"OPTIONAL MATCH (a)-[r:COAUTHOR]->() WHERE r.year <= $yoistr WITH a, COUNT(r) AS num_incoming, {} AS props WITH a, apoc.map.setKey(props, $property_key, num_incoming) as props SET a += props\", {batchSize:1000, params:{num:$num, yoistr:$yoistr, property_key:$property_key}}) YIELD batches, total RETURN batches, total"
        res = self.driver.run(query, num=num, yoistr=str(1980+num), property_key="num_coauthors"+str(1980+num))

    #for all coauthors p, labels with the sum of coauthors for every p
    def initialize_secondary_coauthors(self, num):
        query = "CALL apoc.periodic.iterate(\"MATCH (a:Author) WHERE a.age<=1980+$num RETURN a\", \"OPTIONAL MATCH (a)-[r:COAUTHOR]->(p) WHERE r.year <= $yoistr WITH DISTINCT p, a, {} AS props WITH a, apoc.map.setKey(props, $property_key, SUM(p[$str_coauthors])) as props SET a += props\", {batchSize:1000, params:{num:$num, yoistr:$yoistr, property_key:$property_key, str_coauthors:$str_coauthors}}) YIELD batches, total RETURN batches, total"
        res = self.driver.run(query, num=num, yoistr=str(1980+num), property_key="secondary_coauthors"+str(1980+num), str_coauthors="num_coauthors"+str(1980+num))

if __name__ == "__main__":
    database = NeoGraph("bolt://localhost:7687", "neo4j", "asdfqwer")
    for num in range(0, 41):
        print(num)
        #database.initialize_citations(num)
        #database.initialize_h_index(num)
        database.initialize_num_coauthors(num)
        database.initialize_secondary_coauthors(num)
    """with open('authors_age.csv', newline='\n') as csvfile:
        reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in reader:
            aid = int(row[0])
            age = int(row[1])
            print(aid)
            for num in range(age-1980, 41):                
                database.initialize_h_index(num, aid)"""