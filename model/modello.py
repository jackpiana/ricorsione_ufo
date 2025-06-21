import copy

from database.DAO import DAO
import networkx as nx

from model.sighting import Sighting


class Model:
    def __init__(self):
        self.grafo = None


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

if __name__ == "__main__":
    m = Model()
    m.crea_grafo(1995, "triangle")
    for r in m.get_top_edges():
        print(r)

