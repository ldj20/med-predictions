from neo4j import GraphDatabase
from py2neo import Graph
import pymongo
import csv

class NeoGraph:

    def __init__(self, uri, user, password):
        self.driver = Graph(uri, auth=(user, password))

    def find_year(self, aid):
        query = "MATCH (author:Author) WHERE id(author)=$aid MATCH (author)-[:AUTHORED]->(pubs:Publication) RETURN min(pubs.year)"
        res = self.driver.run(query, aid=aid)
        return res.evaluate()

    def cpp(self, yoi, strYoi, aid):
        query = "MATCH (author:Author) WHERE id(author)=$aid MATCH (author)-[AUTHORED]->(pubs:Publication) WHERE pubs.year <= $yoi WITH author, COUNT(pubs) AS total, SUM(pubs[$stryoi]) AS s RETURN 1.0*s/total"
        res = self.driver.run(query, yoi=yoi, strYoi=strYoi, aid=aid)

    def rank_cpy(self, yoi, strYoi, aid):
        query = "MATCH (author:Author) WHERE id(author)=$aid MATCH (author)-[:AUTHORED]->(pubs:Publication) WHERE pubs.year <= $yoi WITH pubs, pubs[$strYoi] AS s RETURN SUM(1.0*s/($yoi+1-pubs.year))/COUNT(pubs)"
        res = self.driver.run(query, yoi=yoi, strYoi=strYoi, aid=aid)

    def max_citations(self, yoi, strYoi, aid):
        query = "MATCH (author:Author) WHERE id(author)=$aid MATCH (author)-[:AUTHORED]->(pubs:Publication) WHERE pubs.year <= $yoi RETURN max(pubs[strYoi])"
        res = self.driver.run(query, yoi=yoi, strYoi=strYoi, aid=aid)

    def total_citations(self, yoi, strYoi, aid):
        query = "MATCH (author:Author) WHERE id(author)=$aid MATCH (author)-[:AUTHORED]->(pubs:Publication) WHERE pubs.year <= $yoi WITH pubs, pubs[$strYoi] AS s RETURN SUM(s)"
        res = self.driver.run(query, yoi=yoi, strYoi=strYoi, aid=aid) 

    #unfinished 
    def citations_rank(self, yoi, strYoi, aid):
        query = "MATCH (author:Author) RETURN id(author), author[$strYoi]"
        res = self.driver.run(query, yoi=yoi, strYoi=strYoi, aid=aid)

if __name__ == "__main__":
    mongo_str = ""
    client = pymongo.MongoClient(mongo_str)
    db = client.dataset
    collection = db.publications
    database = NeoGraph("bolt://localhost:7687", "neo4j", "asdfqwer")
    with open("./example_authors.csv", "r") as file:
        reader = csv.reader(file)
        i = 0
        for row in reader:
            print(i)
            i += 1
            aid=row[0]
            f_year = database.find_year(aid)
            author = {
                "_id":aid,
                "first_year":f_year,
                "cpp":{},
                "cpy":{},
                "max_citations":{},
                "citations_rank":{},
                "total_citations":{},
                "total_papers":{},
                "citations":{},
                "adopters":{},
                "h-index":{},
                "recent_coauthors":{},
                "mean_journal_citations_per_papers":{},
                "mean_journal_h-index":{},
                "mean_journal_max_citations":{},
                "mean_journal_rank_cpp":{},
                "mean_delta_journal_papers":{},
                "total_journals":{},
                "mean_journal_total_papers":{},
                "network_embedding":{},
                "node_centrality":{},
                "unweighted_pagerank":{},
                "weighted_pagerank":{}
            }
            for year in range(f_year, 2021):
                str_year = str(year)
                author["cpp"][str_year] = database.cpp(year, str_year, aid)
                author["cpy"][str_year] = database.cpy(year, str_year, aid)
                author["max_citations"][str_year] = database.max_citations(year, str_year, aid)
                author["citations_rank"][str_year] = database.citations_rank()
"""MATCH (author:Author) WHERE id(a) = $aid
MATCH (author)-[:AUTHORED]->(pubs:Publication) WHERE pubs.year >= $yoi
WITH pubs[$yoi] AS sum, COUNT(pubs) AS c SET author[$yoi] = (sum/c)"""