from neo4j import GraphDatabase
from py2neo import Graph
import csv
from datetime import datetime;
import sys
sys.path.append("/Users/lawrencejiang/Med-Predictions")
from config import Common

variables = [
]

CURR_VAR = "journal_papers_delta"

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
        
if __name__ == "__main__":
    database = NeoGraph("bolt://localhost:7687", "neo4j", "asdfqwer")
    #with open("./pagerank" + "/" + CURR_VAR + ".csv", newline='\n') as file:
    #with open("./" + CURR_VAR + "/" + CURR_VAR + ".csv", newline='\n') as file:
    with open("./authors_age_delta.csv", newline='\n') as age_file:
        with open("./journal_metrics" + "/" + "delta_total_papers_final" + ".csv", newline='\n') as file:
            reader1 = csv.reader(age_file, delimiter=' ', quotechar='|')
            reader2 = csv.reader(file, delimiter=' ', quotechar='|')
            counter = 0
            for age_row in reader1:
                row = reader2.__next__()
                if (counter%1000 == 0):
                    print(counter)
                counter += 1
                aid = int(row[0])
                age = int(age_row[1])
                if (age >= 2019):
                    continue
                build_str = "{"
                start_index = 0
                continue_searching = True
                while (continue_searching):
                    start_index += 1
                    curr_num = float(row[start_index])
                    if (not curr_num == -1):
                        continue_searching = False
                for i in range(start_index, len(row)):
                    years_from_age = i - start_index
                    val = row[i]
                    curr_year = age + years_from_age + 2
                    prop_name = CURR_VAR + str(curr_year)
                    build_str += prop_name + ":" + val + ","
                build_str = build_str[:-1] + "}"
                database.load(aid, build_str)