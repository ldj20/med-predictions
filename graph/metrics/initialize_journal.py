from neo4j import GraphDatabase
from py2neo import Graph
from scipy.stats import rankdata

class NeoGraph:

    def __init__(self, uri, user, password):
        self.driver = Graph(uri, auth=(user, password))

    #total citations publications in journal has recieved
    def initialize_journal_total(self, num):
        query = "CALL apoc.periodic.iterate(\"MATCH (j:Journal) RETURN j\", \"OPTIONAL MATCH (published_in:Publication)-[:PUBLISHED_IN]->(j) WHERE published_in.year <=1980+$num WITH j, SUM(published_in[toString(1980+$num)]) AS total_citations, {} AS props WITH j, apoc.map.setKey(props, $property_key, total_citations) as props SET j += props\", {batchSize:1, params:{num:$num, property_key:$property_key}}) YIELD batches, total RETURN batches, total"
        self.driver.run(query, num=num, property_key="total"+str(1980+num))
    
    #max number of citations any publication in journal has recieved
    def initialize_journal_max(self, num):
        query = "CALL apoc.periodic.iterate(\"MATCH (j:Journal) RETURN j\", \"OPTIONAL MATCH (published_in:Publication)-[:PUBLISHED_IN]->(j) WHERE published_in.year <=1980+$num WITH j, MAX(published_in[toString(1980+$num)]) AS max_citations, {} AS props WITH j, apoc.map.setKey(props, $property_key, COALESCE(max_citations,0)) as props SET j += props\", {batchSize:1, params:{num:$num, property_key:$property_key}}) YIELD batches, total RETURN batches, total"
        self.driver.run(query, num=num, property_key="max"+str(1980+num))

    #total number of papers journal has
    def initialize_num_papers(self, num):
        query = "CALL apoc.periodic.iterate(\"MATCH (j:Journal) RETURN j\", \"OPTIONAL MATCH (published_in:Publication)-[:PUBLISHED_IN]->(j) WHERE published_in.year <=1980+$num WITH j, COUNT(published_in) AS num_papers, {} AS props WITH j, apoc.map.setKey(props, $property_key, num_papers) as props SET j += props\", {batchSize:1, params:{num:$num, property_key:$property_key}}) YIELD batches, total RETURN batches, total"
        self.driver.run(query, num=num, property_key="num_papers"+str(1980+num))

    def initialize_h_index(self, num):
        query = "CALL apoc.periodic.iterate(\"MATCH (j:Journal) RETURN j\", \"MATCH (p:Publication)-[:PUBLISHED_IN]->(j) WHERE p.year <= 1980+$num WITH j, p[$yoistr] AS numCitations, {} AS props WITH j, apoc.map.setKey(props, $property_key, metrics.h_index(COLLECT(numCitations))) as props SET j += props\", {batchSize:1000, params:{num:$num, yoistr:$yoistr, property_key:$property_key}}) YIELD batches, total RETURN batches, total"
        #query = "CALL apoc.periodic.iterate(\"MATCH (j:Journal) RETURN j\", \"MATCH (a)-[AUTHORED]->(p:Publication) WHERE p.year <= 1980+$num WITH a, p[$yoistr] AS numCitations, {} AS props WITH a, apoc.map.setKey(props, $property_key, metrics.h_index(COLLECT(numCitations))) as props SET a += props\", {batchSize:1000, params:{num:$num, yoistr:$yoistr, property_key:$property_key}}) YIELD batches, total RETURN batches, total"
        self.driver.run(query, num=num, yoistr=str(1980+num), property_key="h_index_"+str(1980+num))
    
    def initialize_mean_cpp(self, num):
        query = "CALL apoc.periodic.iterate(\"MATCH (j:Journal) RETURN j\", \"WITH j, 1.0*j[$total]/j[$num_papers] AS cpp, {} AS props WITH j, apoc.map.setKey(props, $property_key, cpp) as props SET j += props\", {batchSize:1, params:{total:$total, num_papers:$num_papers, property_key:$property_key}}) YIELD batches, total RETURN batches, total"
        self.driver.run(query, total="total"+str(1980+num), num_papers="num_papers"+str(1980+num), property_key="journal_cpp"+str(1980+num))

    #rank of journal in a year based on number of citations per paper, rank 1 has highest cpp
    def initialize_journal_rank(self, num):
        query = "MATCH (j:Journal)<-[:PUBLISHED_IN]-(p:Publication) WHERE p.year<=1980+$num WITH DISTINCT id(j) AS id, 1.0*j[$property_key]/COUNT(p) AS cpp RETURN id, cpp"
        res = self.driver.run(query, num=num, property_key="total"+str(1980+num))
        ids = []
        cpp = []
        for record in res:
            ids.append(record['id'])
            cpp.append(record['cpp'])
        num_journals = len(cpp)
        ranks = rankdata(cpp, method='max')
        for i in range(num_journals):
            ranks[i] = num_journals+1-ranks[i]
            query = "MATCH (j:Journal) WHERE id(j)=$jid WITH j, {} AS props WITH j, apoc.map.setKey(props, $property_key, $rank) as props SET j += props"
            self.driver.run(query, jid=ids[i], property_key="rank"+str(1980+num), rank=int(ranks[i]))
        
if __name__ == "__main__":
    database = NeoGraph("bolt://localhost:7687", "neo4j", "asdfqwer")
    for num in range(0, 41):
        print(num)
        """database.initialize_journal_total(num)
        database.initialize_journal_max(num)
        database.initialize_num_papers(num)
        database.initialize_h_index(num)"""
        database.initialize_mean_cpp(num)
        #database.initialize_journal_rank(num)