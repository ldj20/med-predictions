from neo4j import GraphDatabase
from py2neo import Graph
import requests

class NeoGraph:

    def __init__(self, uri, user, password):
        self.driver = Graph(uri, auth=(user, password))

    def pull_num_ranked(self, year):
        query = "MATCH (pub:Publication) WHERE pub.year>=1980 AND pub.year<=$ending_year AND exists(pub.date_rank) RETURN COUNT(pub)"
        res = self.driver.run(query, ending_year=year)
        while (res.forward()):
            data = res.current
            return data.get("COUNT(pub)")

if __name__ == "__main__":
    database = NeoGraph("bolt://localhost:7687", "neo4j", "asdfqwer")
    with open("./num_ranked.csv", "w") as num_ranked:
        for year in range(1980, 2021):
            n = database.pull_num_ranked(year)
            num_ranked.write(str(n) + "|" + str(year) + "\n")
        
    #r = requests.get("https://api.elsevier.com/content/article/pubmed_id/26170136")
    #print(r.text)