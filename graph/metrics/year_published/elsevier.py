from neo4j import GraphDatabase
from py2neo import Graph
import requests

class NeoGraph:

    def __init__(self, uri, user, password):
        self.driver = Graph(uri, auth=(user, password))

    def search(self):
        query = "MATCH (p:Publication) RETURN id(p), p.identifiers"
        res = self.driver.run(query)
        with open("./pub_identifiers.csv", "w") as new_file:
            while (res.forward()):
                newline = str(res.current[0])
                if (res.current[1]):
                    for entry in res.current[1]:
                        newline += " " + entry
                else:
                    newline += " none"
                new_file.write(newline + "\n")

    def write_identifiers(self, yoi, num):
        query = "CALL apoc.periodic.iterate(\"MATCH (a:Author) RETURN author\", \"OPTIONAL MATCH (author)-[:AUTHORED]->(pubs:Publication) WHERE pubs.year >= $yoi WITH pubs[$yoi] AS sum, COUNT(pubs) AS c SET author[$yoi] = (sum/c)\""
        #MATCH (cited:Publication{year:p.year+1+$num})-[:CITES]->(p) WITH p, count(cited) AS total_citations, {} AS props WITH p, apoc.map.setKey(props, toString(p.year+1+$num), total_citations+p[toString(p.year+$num)]) as props SET p += props\", {batchSize:1000, params:{num:$num}}) YIELD batches, total RETURN batches, total"
        self.driver.run(query, yoi=yoi, num=num)

if __name__ == "__main__":
    database = NeoGraph("bolt://localhost:7687", "neo4j", "asdfqwer")
    database.search()
    #r = requests.get("https://api.elsevier.com/content/article/pubmed_id/26170136")
    #print(r.text)