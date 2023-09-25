from neo4j import GraphDatabase
from py2neo import Graph
import sys
sys.path.append("/Users/lawrencejiang/Med-Predictions")
from config import Common

END_YEAR = 1
LABEL_YEAR = 1

metrics = [
    "cpp",
    "dcpp",
    "cpy",
    "max_citations",
    "author_rank",
    "total_citations",
    "dtotal_citations",
    "total_papers",
    "dtotal_papers",
    "citations",
    "adopters",
    "age",
    "h_index_",
    "dh_index_",
    "recent_coauthors",
    "dmean_journal_citations",
    "mean_journal_citations",
    "djournal_hindex",
    "journal_hindex",
    "journal_max_citations",
    "journal_rank",
    "journal_papers_delta",
    "num_journals",
    "papers_per_journal",
    "node2vec",
    "rescaled_pagerank",
    "uw_pagerank",
    "w_pagerank"
]

class NeoGraph:

    def __init__(self, uri, user, password):
        self.driver = Graph(uri, auth=(user, password))
        
    def export(self):
        query = f"WITH 'MATCH (pub:Publication) WHERE pub.year <= {Common.end_year-LABEL_YEAR-1} AND pub.int_chosen_date IS NOT NULL AND pub.invalid_rescaled IS NULL RETURN pub.high_impact{LABEL_YEAR} AS high_impact"
        end_query = f"' AS query CALL apoc.export.csv.query(query, 'p{END_YEAR}l{LABEL_YEAR}.csv', {{}}) YIELD file, source, format, nodes, relationships, properties, time, rows, batchSize, batches, done, data RETURN file, source, format, nodes, relationships, properties, time, rows, batchSize, batches, done, data;"
        for metric in metrics:
            for post_year in range(END_YEAR+1):
                metric_insert = metric + str(post_year)
                query += f", pub.{metric_insert} AS {metric_insert}"
        query += end_query
        self.driver.run(query)

if __name__ == "__main__":
    database = NeoGraph("bolt://localhost:7687", "neo4j", "asdfqwer")
    database.export()