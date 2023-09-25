from py2neo import Graph

class NeoGraph:

    def __init__(self, uri, user, password):
        self.driver = Graph(uri, auth=(user, password))

    def add_year(self, year):
        query = "CREATE (year:Year{year:$year})"
        self.driver.run(query, year=year)

    def add_journal(self, journal_name, issn):
        query = "CREATE (journal:Journal{name:$journal_name, issn:$issn})"
        self.driver.run(query, journal_name=journal_name, issn=issn)

journals = [
    ("American Journal of Psychiatry", "0002953x"),
    ("American Journal of Respiratory and Critical Care Medicine", "1073449x"),
    ("Annals of Internal Medicine", "00034819"),
    ("Annals of Oncology", "09237534"),
    ("Annals of the Rheumatic Diseases", "00034967"),
    ("Blood", "00064971"),
    ("Brain", "00068950"),
    ("British Medical Journal", "09598138"),
    ("Circulation", "00097322"),
    ("Circulation Research", "00097330"),
    ("Diabetes Care", "01495992"),
    ("European Heart Journal", "0195668x"),
    ("European Respiratory Journal", "09031936"),
    ("European Urology", "03022838"),
    ("Gastroenterology", "00165085"),
    ("Gut", "00175749"),
    ("Hepatology", "02709139"),
    ("Intensive Care Medicine", "03424642"),
    ("JAMA Internal Medicine", "21686106"),
    ("JAMA Neurology", "21686149"),
    ("JAMA Oncology", "23742437"),
    ("JAMA Pediatrics", "21686203"),
    ("JAMA Psychiatry", "2168622x"),
    ("Journal of the National Cancer Institute", "00278874"),
    ("Journal of Allergy and Clinical Immunology", "00916749"),
    ("Journal of Clinical Oncology", "0732183x"),
    ("Journal of Hepatology", "01688278"),
    ("Journal of the American College of Cardiology", "07351097"),
    ("The Lancet", "01406736"),
    ("The Lancet Diabetes & Endocrinology", "22138587"),
    ("The Lancet Infectious Diseases", "14733099"),
    ("The Lancet Neurology", "14744422"),
    ("The Lancet Oncology", "14702045"),
    ("The Lancet Psychiatry", "22150366"),
    ("The Lancet Respiratory Medicine", "22132600"),
    ("Leukemia", "08876924"),
    ("The New England Journal of Medicine", "00284793"),
    ("JAMA", "00987484"),
    ("PLoS Medicine", "15491277"),
    ("World Psychiatry", "17238617")
]
if __name__ == "__main__":
    database = NeoGraph("bolt://localhost:7687", "neo4j", "asdfqwer")
    for year in range(1980, 2021):
        database.add_year(year)
    for journal in journals:
        database.add_journal(journal[0], journal[1])