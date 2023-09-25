from neo4j import GraphDatabase
from py2neo import Graph
import requests
from lxml import etree as etree_lxml

class NeoGraph:

    def __init__(self, uri, user, password):
        self.driver = Graph(uri, auth=(user, password))

    def write_date(self, node_id, date):
        query = "MATCH (p:Publication) WHERE id(p)=$node_id SET p.elsevier_cover_date=$date RETURN p"
        self.driver.run(query, node_id=node_id, date=date)
        

def callElsevier(idString):
    url = "https://api.elsevier.com/content/article/" + idString
    try:
        res = requests.get(url, headers = {"Accept": "application/json", "X-ELS-APIKey": "49de9049ae631584607ca33d1b04dadb", "X-ELS-Insttoken": "847171c9fad83e14de530784b4b89f64"})
        data = res.json()
        if ('full-text-retrieval-response' in data):
            ft = data['full-text-retrieval-response']
            if ('coredata' in ft):
                coredata = ft['coredata']
                if ('prism:coverDate' in coredata):
                    return coredata['prism:coverDate']
    except:
        res = requests.get(url, headers = {"Accept": "application/json", "X-ELS-APIKey": "49de9049ae631584607ca33d1b04dadb", "X-ELS-Insttoken": "847171c9fad83e14de530784b4b89f64"})
        data = res.json()
        if ('full-text-retrieval-response' in data):
            ft = data['full-text-retrieval-response']
            if ('coredata' in ft):
                coredata = ft['coredata']
                if ('prism:coverDate' in coredata):
                    return coredata['prism:coverDate']
    """namespaces = {'': 'http://www.elsevier.com/xml/svapi/article/dtd', 'prism': 'http://prismstandard.org/namespaces/basic/2.0/'}
    tree = etree_lxml.fromstring(res.text)
    dateData = tree.find('coredata', namespaces).find('prism:coverDate', namespaces)
    if dateData is not None:
        return dateData.text""" 
    """soup = BeautifulSoup(res.content, "xml")
    date = soup.find("prism:coverDate")
    print(date)"""
    """root = ElementTree.fromstring(res.text)
    namespaces = {'': 'http://www.elsevier.com/xml/svapi/article/dtd', 'prism': 'http://prismstandard.org/namespaces/basic/2.0/'}
    tester = root.find('coredata', namespaces).find('prism:coverDate', namespaces)
    print(tester.text)"""
    """tester = root.find('full-text-retrieval-response')
    print(tester)"""
    """for child in tree.iter('{http://www.elsevier.com/xml/svapi/article/dtd}coredata'):
        print(child.attrib)"""
    """for child in root.iter('*'):
        print(child.tag, child.attrib)"""
    return ''

def searchElsevier(identifiers):
    for i in range(1, len(identifiers), 2):
        identifierType = identifiers[i]
        if (identifierType == "doi"):
            idString = "doi/" + identifiers[i+1]
            coverDate = callElsevier(idString)
            if (coverDate):
                return coverDate
        elif (identifierType == "pmid"):
            idString = "pubmed_id/" + identifiers[i+1]
            coverDate = callElsevier(idString)
            if (coverDate):
                return coverDate
    return None

if __name__ == "__main__":
    database = NeoGraph("bolt://localhost:7687", "neo4j", "asdfqwer")
    counter = 0
    with open("./pub_identifiers.csv", "r") as pub_identifiers:
        for row in pub_identifiers:
            if (counter%1000==0):
                print(counter)
            counter += 1
            arr = row.split()
            if (arr[1] == "none"):
                continue
            else:
                node_id = int(arr[0])
                #print(timeit.timeit(lambda: searchElsevier(arr), number=1))
                date = searchElsevier(arr)
                if (date):
                    database.write_date(node_id, date)