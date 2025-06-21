from collections import Counter
import copy

from database.DAO import DAO
import networkx as nx

from model.sighting import Sighting


class Model:
    def __init__(self):
        self.grafo = None
        self.seqBest = None
        self.punteggioBest = 0

    def get_years(self):
        return DAO.get_years()

    def get_shapes_year(self, year: int):
        return DAO.get_shapes_year(year)

    def crea_grafo(self, year, shape):
        self.grafo = None
        self.grafo = nx.DiGraph()
        nodes = DAO.get_nodes(year, shape)
        edges = DAO.get_edges(year, shape)
        self.grafo.add_nodes_from(nodes.values())
        for edge in edges:
            self.grafo.add_edge(nodes[edge[0]], nodes[edge[1]], weight=edge[2])

    def get_top_5_edges(self, year, shape):
        "inutile jack, usa sorted edges"
        res = []
        for edge in DAO.get_top5_edges(year, shape):
            str = f"{edge[0]} -- {edge[1]} ----- peso: {edge[2]}"
            res.append(str)
        return res

    def get_top_edges(self):
        res=[]
        sorted_edges = sorted(self.grafo.edges(data=True), key=lambda edge: edge[2].get('weight'), reverse=True)
        for edge in sorted_edges[0:5]:
            str = f"{edge[0].id} --> {edge[1].id} | peso: {edge[2].get('weight')}"
            res.append(str)
        return res

    def best_percorso(self):
        for n in self.grafo.nodes():
            self.ricorsione(n, list(self.grafo.edges), [n])


    def is_ammissibile(self, parziale):
        if len(parziale) < 2:
            return True

        nodes_month = []
        for n in parziale:
            nodes_month.append(n.datetime.month)
        cnt = Counter(nodes_month) #restituisce un dizionario key=oggetto value=frequenza
        most_common = cnt.most_common(1) #restituisce lista con una tupla [(valore, frequenza)]

        if most_common[0][1] > 3: #prende la lista in 0 e la tupla in 1
            return False

        else:
            return True


    def ricorsione(self, nodoPrec, edges, parziale):
        if self.is_ammissibile(parziale) == False:
            print('stop')
            return
        else:
            punteggioAttuale = 100*len(parziale)

            if len(parziale) > 1:
                for i in range(1, len(parziale)):
                    if parziale[i].datetime.month == parziale[i-1].datetime.month:
                        punteggioAttuale += 200


            if punteggioAttuale > self.punteggioBest:
                self.punteggioBest = punteggioAttuale
                self.seqBest = parziale

            for edge in edges:
                if edge[0] == nodoPrec and edge[0].duration < edge[1].duration:
                    parziale.append(edge[1])
                    self.ricorsione(edge[1], edges, parziale)
                    parziale.pop()


if __name__ == "__main__":
    m = Model()
    m.crea_grafo(1996, "circle")
    nodes = list(m.grafo.nodes)
    m.best_percorso()
    for n in m.seqBest:
        print(n)
    print(m.punteggioBest)
    print(m.seqBest)




