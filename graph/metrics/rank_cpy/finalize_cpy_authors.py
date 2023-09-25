from neo4j import GraphDatabase
from py2neo import Graph
import csv
import mysql.connector

class NeoGraph:

    def __init__(self, uri, user, password):
        self.driver = Graph(uri, auth=(user, password))

    def order_authors(self, yoi):
        query = "MATCH (author:Author) WHERE author.age<=$yoi RETURN id(author), author[$cpy] ORDER BY author[$cpy] DESC"
        res = self.driver.run(query, cpy="cpy"+str(yoi), yoi=yoi)
        return res

if __name__ == "__main__":
    cnx = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="RANKS"
    )
    cursor = cnx.cursor()
    database = NeoGraph("bolt://localhost:7687", "neo4j", "asdfqwer")
    for year in range(1980, 2021):
        print(year)
        res = database.order_authors(year)
        authors_arr = []
        curr_cpy = -1
        curr_rank = 0
        sql = "UPDATE authors SET rank_cpy" + str(year) + " = %s WHERE id = %s"
        while res.forward():
            author_cpy = res.current["author[$cpy]"]
            author = (curr_rank, res.current["id(author)"])
            if curr_cpy != author_cpy:
                if curr_cpy != -1:
                    #add all data to mysql
                    print("commited")
                    cursor.executemany(sql, authors_arr)
                    cnx.commit()
                curr_rank += 1
                author = (curr_rank, res.current["id(author)"])
                curr_cpy = author_cpy
                authors_arr = [author]
            else:
                authors_arr.append(author)
        cursor.executemany(sql, authors_arr)
        cnx.commit()
    cursor.close()
    cnx.close()