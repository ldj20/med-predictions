from neo4j import GraphDatabase
from py2neo import Graph

class NeoGraph:

    def __init__(self, uri, user, password):
        self.driver = Graph(uri, auth=(user, password))

    #initialize total citations a publication recieved up to and including current year
    def initialize_weights(self, year):
        #CALL apoc.periodic.iterate("MATCH ()-[r:COAUTHOR]->() WHERE r.year <= $str_year RETURN r", "WITH r, startNode(r) as v, endNode(r) as u WITH r, u[$str_coauthors] AS uIn, v[$str_secondaries] AS pIn, {} AS props WITH r, apoc.map.setKey(props, $weight_year, (1.0*uIn/pIn))^2) as props SET r += props", {batchSize:1000, params:{year:$year, str_year:$str_year, str_coauthors:$str_coauthors, str_secondaries:$str_secondaries, weight_year:$weight_year}}) YIELD batches, total RETURN batches, total
        query = "CALL apoc.periodic.iterate(\"MATCH ()-[r:COAUTHOR]->() WHERE r.year <= $str_year RETURN r\", \"WITH r, startNode(r) as v, endNode(r) as u WITH r, u[$str_coauthors] AS uIn, v[$str_secondaries] AS pIn, {} AS props WITH r, apoc.map.setKey(props, $weight_year, (1.0*uIn/pIn)^2) as props SET r += props\", {batchSize:1000, params:{year:$year, str_year:$str_year, str_coauthors:$str_coauthors, str_secondaries: $str_secondaries, weight_year:$weight_year}}) YIELD batches, total RETURN batches, total"
        #query = "CALL apoc.periodic.iterate(\"MATCH (v:Author)-[r:COAUTHOR]->(u:Author) WHERE r.year <= $year RETURN v,r,u\", \" MATCH (u_in:Author)-[:COAUTHOR]->(u) MATCH (v)-[:COAUTHOR]->(references:Author) MATCH (v_in:Author)-[:COAUTHOR]->(references) WITH r, DISTINCT u_in, DISTINCT v_in, {} AS props WITH p, apoc.map.setKey(props, $weight_year, 1.0*u_in/v_in) as props SET r += props\", {batchSize:1000, params:{year:$year, weight_year:$weight_year}}) YIELD batches, total RETURN batches, total"
        self.driver.run(query, year=year, str_year=str(year), str_coauthors='num_coauthors'+str(year), str_secondaries='secondary_coauthors'+str(year), weight_year='weight'+str(year))

if __name__ == "__main__":
    database = NeoGraph("bolt://localhost:7687", "neo4j", "asdfqwer")
    for year in range(1980, 2021):
        print(year)
        database.initialize_weights(year)