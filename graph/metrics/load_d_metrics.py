from neo4j import GraphDatabase
from py2neo import Graph
from datetime import datetime;
import sys
sys.path.append("/Users/lawrencejiang/Med-Predictions")
from config import Common

variables = [
]

CURR_VAR = "dpapers_per_journal"
BASE_STR = CURR_VAR[1:]

finished_variables = [
    "dcpp",
    "dtotal_citations",
    "dtotal_papers",
    "dh_index_",
    "dmean_journal_citations",
    "djournal_hindex"
]

class NeoGraph:

    def __init__(self, uri, user, password):
        self.driver = Graph(uri, auth=(user, password))
        
    def load(self, age, property_key, m1, m2):
        query = "CALL apoc.periodic.iterate(\"MATCH (author:Author) WHERE author.age<=$age RETURN author\", \"WITH author, {} AS props WITH author, apoc.map.setKey(props, $property_key, author[$m2]-author[$m1]) as props SET author += props\", {batchSize:1000, params:{age:$age, property_key:$property_key, m1:$m1, m2:$m2}}) YIELD batches, total RETURN batches, total"
        #query = "MATCH (author:Author) WHERE id(author)=$aid SET author[" + m_name + "] = (author[$m2]-author[$m1])"
        res = self.driver.run(query, age=age, property_key=property_key, m1=m1, m2=m2)
        return res

if __name__ == "__main__":
    database = NeoGraph("bolt://localhost:7687", "neo4j", "asdfqwer")
    for year in range(Common.start_year+2, Common.end_year):
        print(year)
        database.load(year-2, CURR_VAR+str(year), BASE_STR+str(year-2), BASE_STR+str(year))
    """with open("authors_age.csv", newline='\n') as file:
        reader = csv.reader(file, delimiter=' ', quotechar='|')
        counter = 0
        for row in reader:
            if (counter%1000 == 0):
                print(counter)
            counter += 1
            aid = int(row[0])
            age = int(row[1])
            for i in range(age+2, Common.end_year):
                database.load(aid, BASE_STR + str(i), BASE_STR + str(i-2), CURR_VAR + str(i))
                break
            break"""