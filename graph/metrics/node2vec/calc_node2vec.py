from neo4j import GraphDatabase
from py2neo import Graph
import csv
import math

class NeoGraph:

    def __init__(self, uri, user, password):
        self.driver = Graph(uri, auth=(user, password))

    def create_projections(self, year):
        query = "CALL gds.graph.project.cypher($graph_name, 'MATCH (n:Publication) RETURN id(n) AS id', 'MATCH (n:Publication)-[r:CITES]->(m:Publication) WHERE n.year<=$year RETURN id(n) AS source, id(m) AS target', {parameters:{year:$year}}) YIELD graphName AS graph, nodeQuery, nodeCount AS nodes, relationshipQuery, relationshipCount AS rels"
        self.driver.run(query, graph_name="citations"+str(year), year=year)

    def write_node2vec(self, year):
        query = "CALL gds.beta.node2vec.write($projection_name, {embeddingDimension: 80, writeProperty: $vec_year}) YIELD nodePropertiesWritten"
        self.driver.run(query, projection_name="citations"+str(year), vec_year="node2vec"+str(year))

    def read_node2vec(self, lens_id, year):
        query = "MATCH (p:Publication) WHERE p.lens_id=$lens_id RETURN p[$vec]"
        res = self.driver.run(query, lens_id=lens_id, vec="node2vec"+str(year))
        return res

def truncate(number, digits) -> float:
    stepper = 10.0 ** digits
    return math.trunc(stepper * number) / stepper

if __name__ == "__main__":
    database = NeoGraph("bolt://localhost:7687", "neo4j", "asdfqwer")
    with open("../publication_ids.csv", newline='\n') as file:
        reader = csv.reader(file, delimiter='|', quotechar='|')
        for year in range(1980, 2021):
            #if graph projections are already created, comment below line out
            database.create_projections(year)
            database.write_node2vec(year)
        """with open("./node2vec.csv", "w") as node2vec:
            i = 0
            for row in reader:
                if (i%10000 == 0):
                    print(i)
                i += 1
                lens_id=row[0]
                age=int(row[1])
                w = lens_id
                for year in range(1980, 2021):
                    if (year < age) or (year > age+5):
                        w += " -1 -1 -1 -1"
                    else:
                        res = database.read_node2vec(lens_id, year)
                        vector = res.evaluate()
                        for num in vector:
                            w += " " + str(truncate(num, 3))
                node2vec.write(w + "\n")"""