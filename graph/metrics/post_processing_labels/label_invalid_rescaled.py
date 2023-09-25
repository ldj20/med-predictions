from neo4j import GraphDatabase
from py2neo import Graph

window_size = 1000

class NeoGraph:

    def __init__(self, uri, user, password):
        self.driver = Graph(uri, auth=(user, password))

    def set_invalid(self, starting_rank, final_rank):
        query = "MATCH (pub:Publication) WHERE pub.date_rank>=$starting_rank AND pub.date_rank<=$final_rank SET pub.invalid_rescaled=True"
        self.driver.run(query, starting_rank=starting_rank, final_rank=final_rank)

if __name__ == "__main__":
    database = NeoGraph("bolt://localhost:7687", "neo4j", "asdfqwer")
    database.set_invalid(1, 500)
    with open("./num_ranked.csv", "r") as num_ranked:
        for row in num_ranked:
            arr = row.split("|")
            final_rank = int(arr[0])
            starting_rank = final_rank-(window_size/2)+1
            database.set_invalid(starting_rank, final_rank)