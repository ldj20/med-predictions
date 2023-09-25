from neo4j import GraphDatabase
from py2neo import Graph
from datetime import datetime;
import sys
sys.path.append("/Users/lawrencejiang/Med-Predictions")
from config import Common

class NeoGraph:

    def __init__(self, uri, user, password):
        self.driver = Graph(uri, auth=(user, password))
        
    def load(self, age):
        query = "CALL apoc.periodic.iterate(\"MATCH (author:Author) WHERE author.age=$age RETURN author\", \""
        end_query = "\", {batchSize:1000, params:{age:$age}}) YIELD batches, total RETURN batches, total"
        first = True
        for i in range(age, Common.end_year):
            author_insert = "age" + str(i)
            curr_age = i-age
            if (not first):
                query += "WITH author "
            else:
                first = False
            query += f"SET author.{author_insert} = {curr_age} "
        query += end_query
        self.driver.run(query, age=age)

if __name__ == "__main__":
    database = NeoGraph("bolt://localhost:7687", "neo4j", "asdfqwer")
    for year in range(Common.start_year, Common.end_year):
        print(year)
        database.load(year)
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