from neo4j import GraphDatabase
from py2neo import Graph
import csv

class NeoGraph:

    def __init__(self, uri, user, password):
        self.driver = Graph(uri, auth=(user, password))

    #assumes ids.csv is sorted by year low to high
    def relate_authors(self):
        with open("./ids.csv", "r") as file:
            reader = csv.reader(file, delimiter='|')
            counter = 0
            for row in reader:
                query = "MATCH (pub1:Publication{lens_id:$lens_id})<-[:AUTHORED]-(authors1) MATCH (pub2:Publication{lens_id:$lens_id})<-[:AUTHORED]-(authors2) WHERE id(authors1)<>id(authors2) MERGE (authors1)-[coauthors1:COAUTHOR]->(authors2) MERGE (authors1)<-[coauthors2:COAUTHOR]-(authors2) SET coauthors1.year=COALESCE(coauthors1.year, $year) SET coauthors2.year=COALESCE(coauthors2.year, $year)"
                self.driver.run(query, lens_id=row[0], year=int(row[1]))
                print(counter)
                counter += 1

if __name__ == "__main__":
    database = NeoGraph("bolt://localhost:7687", "neo4j", "asdfqwer")
    database.relate_authors()