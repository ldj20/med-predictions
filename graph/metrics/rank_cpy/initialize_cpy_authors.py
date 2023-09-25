import csv
import mysql.connector

if __name__ == "__main__":
    cnx = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="RANKS"
    )
    cursor = cnx.cursor()
    i = 0
    with open("../authors_age_load.csv", newline='\n') as file:
        reader = csv.reader(file, delimiter=' ', quotechar='|')
        for row in reader:
            aid=int(row[0])
            age=int(row[1])
            w = str(aid)
            author = {
                "id": aid,
                "age": age
            }
            for year in range(1980, 2021):
                if (year < age):
                    author["rank_cpy" + str(year)] = -1
                else:
                    break
            if (i%10000 == 0):
                print(i)
                cnx.commit()
            placeholder = ", ".join(["%s"] * len(author))
            stmt = "insert into `{table}` ({columns}) values ({values});".format(table="authors", columns=",".join(author.keys()), values=placeholder)
            cursor.execute(stmt, list(author.values()))
            i += 1
    cnx.commit()

    cursor.close()
    cnx.close()