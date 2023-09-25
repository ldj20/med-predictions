import requests
import json

from yaml import parse
from neo4j import GraphDatabase
from py2neo import Graph
from dateutil.parser import parse as parseDate
import random

class NeoGraph:

    def __init__(self, uri, user, password):
        self.driver = Graph(uri, auth=(user, password))

    def rank_pubs(self, year, curr_rank):
        query = "MATCH (pub:Publication) WHERE pub.year=$year AND exists(pub.int_chosen_date) RETURN pub.lens_id, pub.int_chosen_date ORDER BY pub.int_chosen_date"
        res = self.driver.run(query, year=year)
        curr_pubs = []
        curr_date = None
        while (res.forward()):
            data = res.current
            int_chosen_date = data.get("pub.int_chosen_date")
            lens_id = data.get("pub.lens_id")
            if (not curr_date or (int_chosen_date == curr_date)):
                curr_pubs.append(lens_id)
            else:
                random.shuffle(curr_pubs)
                for randomized_id in curr_pubs:
                    set_rank = "MATCH (pub:Publication) WHERE pub.lens_id=$lens_id SET pub.date_rank=$rank"
                    self.driver.run(set_rank, lens_id=randomized_id, rank=curr_rank)
                    curr_rank += 1
                curr_pubs = [lens_id]
            curr_date = int_chosen_date
        random.shuffle(curr_pubs)
        for randomized_id in curr_pubs:
            set_rank = "MATCH (pub:Publication) WHERE pub.lens_id=$lens_id SET pub.date_rank=$rank"
            self.driver.run(set_rank, lens_id=randomized_id, rank=curr_rank)
            curr_rank += 1
        return curr_rank

if __name__ == "__main__":
    database = NeoGraph("bolt://localhost:7687", "neo4j", "asdfqwer")
    curr_rank = 811914
    for year in range (2011, 2021):
        print("year:" + str(year))
        curr_rank = database.rank_pubs(year, curr_rank)
        print(curr_rank)