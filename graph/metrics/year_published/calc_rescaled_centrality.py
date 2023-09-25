from neo4j import GraphDatabase
from py2neo import Graph
import math
from collections import deque

#should always be even
window_size = 1000

class NeoGraph:

    def __init__(self, uri, user, password):
        self.driver = Graph(uri, auth=(user, password))

    def calc_centrality(self, year, starting_rank, num_nodes):
        #initialize window
        half_window = int(window_size/2)
        pagerank_string = "pub_pagerank" + str(year)
        start = starting_rank - half_window
        end = starting_rank + half_window
        q = deque()
        pageranks = []
        get_pagerank = "MATCH (pub:Publication) WHERE pub.date_rank=$curr_rank RETURN pub[$pagerank]"
        sum_pagerank = 0
        for i in range(start, end+1):
            res = self.driver.run(get_pagerank, curr_rank=i, pagerank=pagerank_string)
            if (res.forward()):
                data = res.current
                pagerank = data.get("pub[$pagerank]")
                sum_pagerank += pagerank
                q.append(pagerank)
                pageranks.append(pagerank)
        """left_res = self.driver.run(get_pagerank, curr_rank=start, pagerank=pagerank_string)
        left_pagerank = 0
        if (left_res.forward()):
            data = left_res.current
            left_pagerank = data.get("pub[$pagerank]")"""
        mean = sum_pagerank/(window_size+1)
        #calculate std dev
        difference_sum = 0
        for i in range(len(pageranks)):
            difference_sum += (pageranks[i]-mean) ** 2
        std_dev = math.sqrt(difference_sum/(window_size+1))
        #std_dev = statistics.stdev(pageranks)
        #we want the half_window+1th element to get the first publication with a valid window
        curr_pagerank = pageranks[half_window]
        #(pagerank of node - mean of window)/std dev of window
        #deal with the first post of the fencepost problem
        rescaled_pagerank = (curr_pagerank - mean)/std_dev
        set_rescaled = "MATCH (pub:Publication) WHERE pub.date_rank=$curr_rank SET pub += $rescaled_pagerank"
        self.driver.run(set_rescaled, curr_rank=half_window+1, rescaled_pagerank={"rescaled_pagerank" + str(year) : rescaled_pagerank})
        for i in range(half_window+2, num_nodes-half_window+1):
            #recalculate window
            sum_pagerank -= q.popleft()
            res = self.driver.run(get_pagerank, curr_rank=i+half_window, pagerank=pagerank_string)
            if (res.forward()):
                data = res.current
                pagerank = data.get("pub[$pagerank]")
                sum_pagerank += pagerank
                q.append(pagerank)
                pageranks.append(pagerank)
            mean = sum_pagerank/(window_size+1)
            difference_sum = 0
            for j in range(i-half_window-1, len(pageranks)):
                difference_sum += (pageranks[j]-mean) ** 2
            std_dev = math.sqrt(difference_sum/(window_size+1))
            #std_dev = statistics.stdev(pageranks)
            res = self.driver.run(get_pagerank, curr_rank=i, pagerank=pagerank_string)
            if (res.forward()):
                data = res.current
                curr_pagerank = data.get("pub[$pagerank]")
                rescaled_pagerank = (curr_pagerank - mean)/std_dev
                self.driver.run(set_rescaled, curr_rank=i, rescaled_pagerank={"rescaled_pagerank" + str(year) : rescaled_pagerank})

if __name__ == "__main__":
    database = NeoGraph("bolt://localhost:7687", "neo4j", "asdfqwer")
    starting_rank = int((window_size/2)+1)
    with open("./num_ranked.csv", "r") as num_ranked:
        for row in num_ranked:
            arr = row.split("|")
            year = int(arr[1])
            print(year)
            database.calc_centrality(year, starting_rank, int(arr[0]))