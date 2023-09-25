from neo4j import GraphDatabase
from py2neo import Graph
import csv
from datetime import datetime
import math

class NeoGraph:

    def __init__(self, uri, user, password):
        self.driver = Graph(uri, auth=(user, password))
    
    def journal_metrics(self, yoi, aid):
        query = "MATCH (author:Author) WHERE id(author)=$aid MATCH (author)-[:AUTHORED]->(pubs:Publication) WHERE pubs.year <= $yoi MATCH (pubs)-[:PUBLISHED_IN]->(journals:Journal) WITH DISTINCT journals AS journals WITH COUNT(journals) AS num_journals, SUM(1.0*journals[$str_hindex])/COUNT(journals) AS hindex, SUM(1.0*journals[$str_max])/COUNT(journals) AS max_citations, SUM(1.0*journals[$str_rank])/COUNT(journals) AS rank, SUM(1.0*journals[$str_num_papers])/COUNT(journals) AS num_papers RETURN num_journals, hindex, max_citations, rank, num_papers"
        res = self.driver.run(query, yoi=yoi, aid=aid, str_hindex="h_index_"+str(yoi), str_max="max"+str(yoi), str_rank="rank"+str(yoi), str_num_papers="num_papers"+str(yoi))
        return res

def truncate(number, digits) -> float:
    stepper = 10.0 ** digits
    return math.trunc(stepper * number) / stepper
    
if __name__ == "__main__":
    database = NeoGraph("bolt://localhost:7687", "neo4j", "asdfqwer")
    with open("../authors_age.csv", newline='\n') as file:
        reader = csv.reader(file, delimiter=' ', quotechar='|')
        with open("./num_journals.csv", "w") as num_journals:
            with open("./journal_hindex.csv", "w") as hindex:
                with open("./journal_max_citations.csv", "w") as max_citations:
                    with open("./journal_rank.csv", "w") as rank:
                        with open("./papers_per_journal.csv", "w") as num_papers:
                            i = 0
                            for row in reader:
                                print(i)
                                i += 1
                                aid=int(row[0])
                                age=int(row[1])
                                w_num_journals = str(aid)
                                w_hindex = str(aid)
                                w_max_citations = str(aid)
                                w_rank = str(aid)
                                w_num_papers = str(aid)
                                for year in range(1980, 2021):
                                    if (year < age):
                                        w_num_journals += " -1"
                                        w_hindex += " -1"
                                        w_max_citations += " -1"
                                        w_rank += " -1"
                                        w_num_papers += " -1"
                                    else:
                                        res = database.journal_metrics(year, aid)
                                        for record in res:
                                            w_num_journals += " " + str(record['num_journals'])
                                            w_hindex += " " + str(truncate(record['hindex'], 3))
                                            w_max_citations += " " + str(truncate(record['max_citations'], 3))
                                            w_rank += " " + str(truncate(record['rank'], 3))
                                            w_num_papers += " " + str(truncate(record['num_papers'], 3))
                                num_journals.write(w_num_journals + "\n")
                                hindex.write(w_hindex + "\n")
                                max_citations.write(w_max_citations + "\n")
                                rank.write(w_rank + "\n")
                                num_papers.write(w_num_papers + "\n")
