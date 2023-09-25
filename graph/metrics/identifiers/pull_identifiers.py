import requests
import json
from neo4j import GraphDatabase
from py2neo import Graph

class NeoGraph:

    def __init__(self, uri, user, password):
        self.driver = Graph(uri, auth=(user, password))

    def insert_ids(self, lens_id, identifiers):
        query = "MATCH (pub:Publication) WHERE pub.lens_id = $lens_id WITH pub, {} AS props WITH pub, apoc.map.setKey(props, \"identifiers\", $identifiers) as props SET pub += props"
        self.driver.run(query, lens_id=lens_id, identifiers=identifiers)

def process(res_data, database):
    for entry in res_data:
        cont = (('authors' in entry) and ('title' in entry) and ('year_published' in entry))
        if (not cont):
            continue
        identifiers = entry['external_ids']
        lens_id = entry['lens_id']
        if (not identifiers):
            print(lens_id)
        insert_arr = []
        for i in range(len(identifiers)):
            id_name = identifiers[i]["type"]
            id_value = identifiers[i]["value"]
            insert_arr.append(id_name)
            insert_arr.append(id_value)
        database.insert_ids(lens_id, insert_arr)

url = 'https://api.lens.org/scholarly/search'

journals_done = ["source.issn:(0002953x)",
    "source.issn:(1073449x)",
    "source.issn:(00034819)",
    "source.issn:(09237534)",
    "source.issn:(00034967)",
    "source.issn:(00064971)",
    "source.issn:(00068950)",
    "source.issn:(09598138)",
    "source.issn:(00097322)",
    "source.issn:(00097330)",
    "source.issn:(01495992)",
    "source.issn:(0195668x)",
    "source.issn:(09031936)",
    "source.issn:(03022838)",
    "source.issn:(00165085)",
    "source.issn:(00175749)",
    "source.issn:(02709139)",
    "source.issn:(03424642)",
    "source.issn:(21686106)",
    "source.issn:(21686149)",
    "source.issn:(23742437)",
    "source.issn:(21686203)",
    "source.issn:(2168622x)",
    "source.issn:(00278874)",
    "source.issn:(00916749)",
    "source.issn:(0732183x)",
    "source.issn:(01688278)",
    "source.issn:(07351097)",
    "source.issn:(01406736)",
    "source.issn:(22138587)",
    "source.issn:(14733099)",
    "source.issn:(14744422)",
    "source.issn:(14702045)",
    "source.issn:(22150366)",
    "source.issn:(22132600)",
    "source.issn:(08876924)",
    "source.issn:(00284793)",
    "source.issn:(00987484)",
    "source.issn:(15491277)",
    "source.issn:(17238617)"]
journals_doing = [
]
journals_todo = [
]

if __name__ == "__main__":
    database = NeoGraph("bolt://localhost:7687", "neo4j", "asdfqwer")
    a = 1
    for query_string in journals_doing:
        print(a)
        print("______")
        counter = 0
        build_string = "(" + query_string + ") AND year_published:[1980 TO 2020]"
        data = json.dumps({
            "query": build_string,
            "scroll": "5m",
            "size": 900
        })
        token = ""
        headers = {f"Authorization": "Bearer {token}", "Accept-Encoding": "UTF-8", "Content-Type": "application/json", "Accept": "*/*"}
        res = requests.post(url, headers=headers, data=data)
        js = res.json()
        res_data = js["data"]
        res_scroll = js["scroll_id"]
        data = json.dumps({
            "query": build_string,
            "scroll_id": res_scroll,
            "scroll": "5m"
        })
        while (res_data):
            print(counter)
            counter += 1
            process(res_data, database)
            res = requests.post(url, headers=headers, data=data)
            js = res.json()
            res_data = js["data"]
            res_scroll = js["scroll_id"]
            data = json.dumps({
                "query": build_string,
                "scroll_id": res_scroll,
                "scroll": "5m"
            })
