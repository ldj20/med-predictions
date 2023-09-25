from re import L
from neo4j import GraphDatabase
from py2neo import Graph
import sys
sys.path.append("/Users/lawrencejiang/Med-Predictions")
from config import Common

post_years = [
    2,3,4,5
]

class NeoGraph:

    def __init__(self, uri, user, password):
        self.driver = Graph(uri, auth=(user, password))

    def get_rescaled(self, year, all_pubs, post_year):
        query = "MATCH (pub:Publication) WHERE pub.year=$year AND EXISTS(pub.date_rank) AND NOT EXISTS(pub.invalid_rescaled) RETURN pub[$rescaled_str], id(pub)"
        res = self.driver.run(query, year=year, rescaled_str="rescaled_pagerank"+str(year+post_year))
        while (res.forward()):
            data = res.current
            pub_info = (data.get('pub[$rescaled_str]'), data.get('id(pub)'))
            all_pubs.append(pub_info)

    def initialize_high_impact(self):
        for i in range(2, 6):
            pub_insert = "high_impact" + str(i)
            #filter is papers that have valid dates from datasets and are not outside the initial sliding windows
            # WHERE pub.int_chosen_date IS NOT NULL AND pub.invalid_rescaled IS NULL
            query = f"CALL apoc.periodic.iterate('MATCH (pub:Publication) RETURN pub', 'SET pub.{pub_insert}=0', {{batchSize:10000}}) yield batches, total return batches, total"
            self.driver.run(query)

    def set_high_impact(self, pub_id, post_year):
        for i in range(0, post_year + 1):
            pub_insert = "high_impact" + str(i)
            query = f"MATCH(pub:Publication) WHERE id(pub)=$pub_id SET pub.{pub_insert}=1"
            self.driver.run(query, pub_id=pub_id)

if __name__ == "__main__":
    database = NeoGraph("bolt://localhost:7687", "neo4j", "asdfqwer")
    database.initialize_high_impact()
    all_pubs = [] 
    for post_year in post_years:
        print(post_year)
        for year in range(Common.start_year, Common.end_year-post_year):
            print(year)
            database.get_rescaled(year, all_pubs, post_year)
        all_pubs = sorted(all_pubs, key = lambda x: x[0], reverse = True)
        five_percent = int(len(all_pubs)/20)
        for i in range(0, five_percent):
            pub = all_pubs[i]
            database.set_high_impact(pub[1], post_year)
        all_pubs = []