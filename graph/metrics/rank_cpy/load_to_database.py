from neo4j import GraphDatabase
from py2neo import Graph
import mysql.connector
import csv
import sys
sys.path.append("/Users/lawrencejiang/Med-Predictions")
from config import Common

class NeoGraph:

    def __init__(self, uri, user, password):
        self.driver = Graph(uri, auth=(user, password))

    def load_rank(self, aid, data):
        query = "MATCH (author:Author) WHERE id(author) = $aid "
        first = True
        for year in range(Common.start_year, Common.end_year):
            index = year-Common.start_year
            if (data[index] == -1):
                continue
            property_name = "author_rank" + str(year)
            value = data[index]
            if (not first):
                query += "WITH author "
            else:
                first = False
            query += f"SET author.{property_name} = {value} "
        self.driver.run(query, aid=aid)

if __name__ == "__main__":
    cnx = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="RANKS"
    )
    cursor = cnx.cursor()
    database = NeoGraph("bolt://localhost:7687", "neo4j", "asdfqwer")
    counter = 0
    with open("../authors_age_load.csv", newline='\n') as file:
        reader = csv.reader(file, delimiter=' ', quotechar='|')
        for row in reader:
            aid=int(row[0])
            age=int(row[1])
            if (counter % 1000 == 0):
                print(counter)
                print(aid)
            counter += 1
            author = {
                "id": aid,
                "age": age
            }
            cursor.execute(f"SELECT * FROM authors WHERE id={aid};")
            for row in cursor:
                aid = row[0]
                row = row[2:]
                database.load_rank(aid, row)
    cursor.close()
    cnx.close()