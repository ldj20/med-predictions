from neo4j import GraphDatabase
from py2neo import Graph
import csv
from datetime import datetime
import math

class NeoGraph:

    def __init__(self, uri, user, password):
        self.driver = Graph(uri, auth=(user, password))
    
    def journal_citations(self, yoi, aid):
        query = "MATCH (author:Author) WHERE id(author)=$aid MATCH (author)-[:AUTHORED]->(pubs:Publication) WHERE pubs.year <= $yoi MATCH (pubs)-[:PUBLISHED_IN]->(journals:Journal) WITH DISTINCT journals AS journals WITH COUNT(journals) AS num_journals, SUM(1.0*journals[$str_total]/journals[$str_num]) AS cpp RETURN cpp/num_journals"
        res = self.driver.run(query, yoi=yoi, aid=aid, str_total="total"+str(yoi), str_num="num_papers"+str(yoi))
        return res

def truncate(number, digits) -> float:
    stepper = 10.0 ** digits
    return math.trunc(stepper * number) / stepper
    
if __name__ == "__main__":
    database = NeoGraph("bolt://localhost:7687", "neo4j", "asdfqwer")
    with open("../authors_age.csv", newline='\n') as file:
        reader = csv.reader(file, delimiter=' ', quotechar='|')
        with open("./mean_journal_citations.csv", "w") as journal_citations:
            i = 0
            for row in reader:
                print(i)
                i += 1
                aid=int(row[0])
                age=int(row[1])
                w = str(aid)
                for year in range(1980, 2021):
                    if (year < age):
                        w += " -1"
                    else:
                        res = database.journal_citations(year, aid)
                        w += " " + str(truncate(res.evaluate(), 3))
                journal_citations.write(w + "\n")