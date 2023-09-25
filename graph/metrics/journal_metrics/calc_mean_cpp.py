from neo4j import GraphDatabase
from py2neo import Graph
import csv
from datetime import datetime
import math

class NeoGraph:

    def __init__(self, uri, user, password):
        self.driver = Graph(uri, auth=(user, password))
    
    def journal_metrics(self, yoi, aid):
        query = "MATCH (author:Author) WHERE id(author)=$aid MATCH (author)-[:AUTHORED]->(pubs:Publication) WHERE pubs.year <= $yoi MATCH (pubs)-[:PUBLISHED_IN]->(journals:Journal) WITH DISTINCT journals AS journals WITH COUNT(journals) AS num_journals, SUM(journals[$str_journal_cpp])/COUNT(journals) AS mean_cpp RETURN mean_cpp"
        res = self.driver.run(query, yoi=yoi, aid=aid, str_journal_cpp="journal_cpp"+str(yoi))
        return res

def truncate(number, digits) -> float:
    stepper = 10.0 ** digits
    return math.trunc(stepper * number) / stepper
    
if __name__ == "__main__":
    database = NeoGraph("bolt://localhost:7687", "neo4j", "asdfqwer")
    with open("./place.csv", newline='\n') as file:
        reader = csv.reader(file, delimiter=' ', quotechar='|')
        with open("./journal_cpp2.csv", "w") as journal_cpp:
            i = 0
            for row in reader:
                print(i)
                i += 1
                aid=int(row[0])
                age=int(row[1])
                w_journal_cpp = str(aid)
                for year in range(1980, 2021):
                    if (year < age):
                        w_journal_cpp += " -1"
                    else:
                        res = database.journal_metrics(year, aid)
                        for record in res:
                            w_journal_cpp += " " + str(truncate(record['mean_cpp'], 3))
                journal_cpp.write(w_journal_cpp + "\n")