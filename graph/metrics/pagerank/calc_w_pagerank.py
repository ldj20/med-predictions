from neo4j import GraphDatabase
from py2neo import Graph
import csv
import math

class NeoGraph:

    def __init__(self, uri, user, password):
        self.driver = Graph(uri, auth=(user, password))

    def initialize_weights(self, year):
        query = "CALL apoc.periodic.iterate(\"MATCH ()-[r:COAUTHOR]->() WHERE r.year <= $str_year RETURN r\", \"WITH r, startNode(r) as v, endNode(r) as u WITH r, u[$str_coauthors] AS uIn, v[$str_secondaries] AS pIn, {} AS props WITH r, apoc.map.setKey(props, $weight_year, (1.0*uIn/pIn)^2) as props SET r += props\", {batchSize:1000, params:{year:$year, str_year:$str_year, str_coauthors:$str_coauthors, str_secondaries: $str_secondaries, weight_year:$weight_year}}) YIELD batches, total RETURN batches, total"
        self.driver.run(query, year=year, str_year=str(year), str_coauthors='num_coauthors'+str(year), str_secondaries='secondary_coauthors'+str(year), weight_year='weight'+str(year))

    def create_author_projections(self, num):
        query = "CALL gds.graph.create.cypher($name, 'MATCH (n:Author) WHERE n.age <= $year RETURN id(n) AS id', 'MATCH (n:Author)-[r:COAUTHOR]->(m:Author) WHERE r.year <= $stryear RETURN id(n) AS source, id(m) AS target, r[$weight] AS weight', {parameters:{name: $name, year:$year, stryear:$stryear, weight: $weight}}) YIELD graphName AS graph, nodeQuery, nodeCount AS nodes, relationshipQuery, relationshipCount AS rels"
        self.driver.run(query, name='coauthors'+str(num), year=num, stryear=str(num), weight='weight'+str(num))

    def write_w_pagerank(self, year):
        query = "CALL gds.pageRank.write($projection_name, {maxIterations: 20, dampingFactor: 0.85, writeProperty: $str_pagerank, relationshipWeightProperty: 'weight'}) YIELD nodePropertiesWritten, ranIterations"
        self.driver.run(query, projection_name="coauthors"+str(year), str_pagerank="w_pagerank"+str(year))

    def delete_weights(self, year):
        query = "CALL apoc.periodic.iterate(\"MATCH ()-[r:COAUTHOR]->() WHERE r.year<=$str_year RETURN r\", \"REMOVE r.weight" + str(year) + "\", {batchSize:10000, params:{str_year:$str_year}})"
        self.driver.run(query, str_year=str(year))

    def read_w_pagerank(self, year, aid):
        query = "MATCH (a:Author) WHERE id(a)=$aid RETURN a[$str_pagerank]"
        res = self.driver.run(query, aid=aid, str_pagerank="w_pagerank"+str(year))
        return res

    def delete_uw(self, year):
        query = "CALL apoc.periodic.iterate(\"MATCH (n:Author) RETURN n\", \"REMOVE n.uw_pagerank" + str(year) + "\", {batchSize:10000})"
        self.driver.run(query)

def truncate(number, digits) -> float:
    stepper = 10.0 ** digits
    return math.trunc(stepper * number) / stepper

if __name__ == "__main__":
    database = NeoGraph("bolt://localhost:7687", "neo4j", "asdfqwer")
    for year in range(1980, 2021):
        print(year)
        database.initialize_weights(year)
        database.create_author_projections(year)
        database.write_w_pagerank(year)
    with open("../authors_age.csv", newline='\n') as file:
        reader = csv.reader(file, delimiter=' ', quotechar='|')
        with open("./w_pagerank.csv", "w") as w_pagerank:
            i = 0
            for row in reader:
                print(i)
                i += 1
                aid=int(row[0])
                age=int(row[1])
                w = str(aid)
                for year in range(1980, 2021):
                    if (year < age):
                        w += " -1"
                    else:
                        res = database.read_w_pagerank(year, aid)
                        w += " " + str(truncate(res.evaluate(), 3))
                w_pagerank.write(w + "\n")