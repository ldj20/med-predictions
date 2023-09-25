from neo4j import GraphDatabase
from py2neo import Graph
import csv
from datetime import datetime;
import sys
sys.path.append("/Users/lawrencejiang/Med-Predictions")
from config import Common

variables = [
]

CURR_VAR = "delta_total_papers"


finished_variables = [
    "cpp",
    "cpy",
    "max_citations",
    "total_citations",
    "adopters",
    "total_papers",
    "recent_coauthors",
    "author_h_index_",
    "mean_journal_citations",
    "journal_hindex",
    "journal_rank",
    "journal_max_citations",
    "papers_per_journal",
    "num_journals",
    "citations",
    "w_pagerank",
    "uw_pagerank"
]

class NeoGraph:

    def __init__(self, uri, user, password):
        self.driver = Graph(uri, auth=(user, password))
        
    def load(self, aid, build_str):
        query = "MATCH (author:Author) WHERE id(author)=$aid SET author+=" + build_str
        res = self.driver.run(query, aid=aid)
        return res

class NeoGraph:

    def __init__(self, uri, user, password):
        self.driver = Graph(uri, auth=(user, password))
        
    def load(self, aid, build_str):
        query = "MATCH (author:Author) WHERE id(author)=$aid SET author+=" + build_str
        res = self.driver.run(query, aid=aid)
        return res

if __name__ == "__main__":
    database = NeoGraph("bolt://localhost:7687", "neo4j", "asdfqwer")
    #with open("./pagerank" + "/" + CURR_VAR + ".csv", newline='\n') as file:
    #with open("./" + CURR_VAR + "/" + CURR_VAR + ".csv", newline='\n') as file:
    with open("./journal_metrics" + "/" + CURR_VAR + ".csv", newline='\n') as file:
        reader = csv.reader(file, delimiter=' ', quotechar='|')
        counter = 0
        for row in reader:
            if (counter%1000 == 0):
                print(counter)
            counter += 1
            aid = int(row[0])
            build_str = "{"
            for i in range(Common.num_years+1):
                val = row[i+1]
                if (int(float(val)) == -1):
                    continue
                prop_name = CURR_VAR + str(Common.start_year+i)
                build_str += prop_name + ":" + val + ","
            build_str = build_str[:-1] + "}"
            database.load(aid, build_str)