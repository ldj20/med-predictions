from neo4j import GraphDatabase
from py2neo import Graph
import pymongo
import timeit

class NeoGraph:

    def __init__(self, uri, user, password):
        self.driver = Graph(uri, auth=(user, password))

    def add_publication(self, pub):
        issn = pub["issn"]
        year_published = pub["year"]
        lens_id = pub["lens_id"]
        query = "MATCH (publication:Publication{lens_id:$lens_id}) USING INDEX publication:Publication(lens_id) RETURN publication"
        res = self.driver.run(query, lens_id=lens_id)
        if (res.evaluate()):
            return True
        query = "MATCH (journal:Journal{issn:$issn}) USING INDEX journal:Journal(issn) MATCH(date:Year{year:$year_published}) USING INDEX date:Year(year) CREATE (a:Publication {lens_id:$lens_id}) SET a=$pub CREATE (a)-[:PUBLISHED_IN]->(journal) CREATE (a)-[:PUBLISHED_ON]->(date)"
        self.driver.run(query, pub=pub, issn=issn, year_published=year_published, lens_id=lens_id)
        return False

    def add_author(self, authors, lens_id, year_published):
        """
        MATCH (a:Author) WHERE (a.magid=$mag OR a.orcid=$orc) 
        WITH collect(a) as nodes 
        CALL apoc.refactor.mergeNodes(nodes, {properties: {
            collective_name:"discard",
            first_name:"discard",
            last_name:"discard",
            initials:"discard",
            affiliations:"combine"
        }, mergeRels:true}) 
        YIELD node RETURN node"""
        """orcid = ""
        magid = ""
        if (authors["orcid"]):
            orcid = authors["orcid"]
        if authors["magid"]:
            magid = authors["magid"]"""
        """MATCH (a:Author{is_first:1})-[rel:AUTHORED]->(:Publication) SET rel.is_first = 1"""
        """MATCH (a:Author{is_last:1})-[rel:AUTHORED]->(:Publication) SET rel.is_last = 1"""
        """MATCH (a:Author{is_second:1})-[rel:AUTHORED]->(:Publication) SET rel.is_second = 1"""
        #query = "UNWIND $authors AS authors CREATE (a:Author) SET a = authors"

        query = "MATCH (p:Publication{lens_id:$lens_id}) MATCH(date:Year{year:$year_published}) UNWIND $authors AS authors CREATE (a:Author)-[:AUTHORED]->(p) CREATE (a)-[:PUBLISHED_ON]->(date) SET a = authors"
        self.driver.run(query, authors=authors, lens_id=lens_id, year_published=year_published)
        
    """
    merge on magid and orcid
    relate all authors to each other
    look at instutions, create them and edges
    citations
    """

    def add_citations(self, lens_id):
        query = "MATCH (p:Publication{lens_id:$lens_id}) UNWIND p.citations AS citations MATCH (cited:Publication{lens_id:citations}) MERGE (p)-[:CITES]->(cited)"
        self.driver.run(query, lens_id=lens_id)
    
    def add_second(self, author, lens_id):
        params = []
        for key in author:
            params.append(key+":\""+str(author[key])+"\"")
        query = "MATCH (p:Publication{lens_id:$lens_id})<-[rel:AUTHORED]-(:Author{"+ ", ".join(params) + "}) SET rel.is_second = 1"
        #query = "UNWIND $author AS author MATCH (p:Publication{lens_id:$lens_id})<-[rel:AUTHORED]-(:Author{first_name:$first_name,last_name:$last_name}) SET rel.is_second = 1"
        self.driver.run(query, lens_id=lens_id)
    def add_third(self, author, lens_id):
        params = []
        for key in author:
            params.append(key+":\""+str(author[key])+"\"")
        query = "MATCH (p:Publication{lens_id:$lens_id})<-[rel:AUTHORED]-(:Author{"+ ", ".join(params) + "}) SET rel.is_third = 1"
        #query = "MATCH (p:Publication{lens_id:$lens_id})<-[rel:AUTHORED]-(:Author{first_name:$first_name,last_name:$last_name}) SET rel.is_third = 1"
        self.driver.run(query, lens_id=lens_id)

def process(database, doc):
    """lens_id = doc["_id"]
    title = doc["title"]
    authors = doc["authors"]
    citations = doc["citations"]
    year = doc["year"]
    source = doc["source"]
    issns = doc["issns"]
    source_issn = ""
    for issn in issns:
        if (issn['type'] == "print"):
            source_issn = issn['value']
            break
        elif (issn['type'] != "electronic"):
            source_issn = issn['value']
    publication_build = {
        "lens_id": lens_id,
        "title": title,
        "citations": citations,
        "year": year,
        "source": source,
        "issn": source_issn
    }
    already_in = database.add_publication(publication_build)
    if (already_in):
        return
    for i in range(len(authors)):
        author = authors[i]
        affiliations = []
        if ('affiliations' in author):
            for affiliation in author['affiliations']:
                if ('name' in affiliation):
                    affiliations.append(affiliation['name'])
            author.pop('affiliations')
            author['affiliations'] = affiliations
        if ('ids' in author):
            external_ids = author['ids']
            author.pop('ids')
            for id in external_ids:
                author[id['type']] = id['value']
        author['is_first'] = 0
        author['is_last'] = 0
        if (i == 0):
            author['is_first'] = 1
        if (i == len(authors)-1):
            author['is_last'] = 1
    database.add_author(authors, lens_id, year)"""
    lens_id = doc["_id"]
    authors = doc["authors"]
    if (len(authors) > 1):
        author = authors[1]
        if ('affiliations' in author):
            author.pop('affiliations')
        if ('ids' in author):
            external_ids = author['ids']
            author.pop('ids')
            for id in external_ids:
                author[id['type']] = id['value']
        database.add_second(author, lens_id)
    if (len(authors) > 2):
        author = authors[2]
        if ('affiliations' in author):
            author.pop('affiliations')
        if ('ids' in author):
            external_ids = author['ids']
            author.pop('ids')
            for id in external_ids:
                author[id['type']] = id['value']
        database.add_third(author, lens_id)
    

if __name__ == "__main__":
    mongo_str = ""
    client = pymongo.MongoClient(mongo_str)
    db = client.dataset
    collection = db.publications
    database = NeoGraph("bolt://localhost:7687", "neo4j", "asdfqwer")
    for num in range(1980, 2020):
        docs = collection.find({"year": num}).batch_size(40)
        overall = 0
        for doc in docs:
            process(database, doc)
        docs.close()