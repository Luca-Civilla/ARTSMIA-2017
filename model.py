import copy

import networkx as nx
from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self.idMap = {}
        self.oggetti = DAO.getAllObjects()
        for o in self.oggetti:
            self.idMap[o.object_id] = o
        self.bestPath = []
        self.pesoMax = 0

    def getPath(self,lunghezza,nodo):
        self.bestPath = []
        self.pesoMax = 0
        vertice = self.idMap[nodo]
        print(vertice.classification)
        parziale = [vertice]
        for v in self._grafo.neighbors(vertice):
            if v.classification == vertice.classification:
                parziale.append(v)
                self._ricorsione(parziale, lunghezza)
                parziale.pop()
        #self._ricorsione(parziale, lunghezza)
        return self.bestPath,self.pesoMax

    def _ricorsione(self,parziale,lunghezza):
        if len(parziale) == lunghezza:#VEDO SE NUOVO PARZIALE E' MIGLIORE DEL VECCHIO
            #CONDIZIONE DA RISPETTARE
            if self.calcolaPeso(parziale)>self.pesoMax:
                self.pesoMax = self.calcolaPeso(parziale)
                self.bestPath = copy.deepcopy(parziale)
            return
        print(parziale[-1].object_id)
        #CONDIZIONE PER AGGIUNGERE NUOVI ARCHI
        for c in self._grafo.neighbors(parziale[-1]):
            if c not in parziale and c.classification == parziale[0].classification:
                parziale.append(c)
                self._ricorsione(parziale,lunghezza)
                parziale.pop()

    def calcolaPeso(self,listOfNodes):
        pesoMax = 0
        for i in range(0,len(listOfNodes)+1):
            peso = self._grafo[listOfNodes[i]][listOfNodes[i+1]]["weight"]
            pesoMax += peso
        return pesoMax



    def buildGraph(self):
        self._grafo.clear()
        self._grafo.add_nodes_from(self.oggetti)
        self._creaArchi()

    def _creaArchi(self):
        self._grafo.clear_edges()
        # for u in self._grafo.nodes:
        #     for v in self._grafo.nodes:
        #         if u!=v:
        #             result = DAO.getArchiPeso(u.object_id,v.object_id)
        #             if result:
        #                 peso = int(result[0])
        #                 self._grafo.add_edge(u,v,weight= peso)
        connessioni = DAO.getArchi2(self.idMap)
        for c in connessioni:
            self._grafo.add_edge(c.obj1,c.obj2,weight= c.peso)

    def getComponente(self,nodo):
        n = self.idMap[nodo]
        componente = nx.node_connected_component(self._grafo,n)
        numero = len(componente)
        return componente,numero






    def graphDetails(self):
        return len(self._grafo.nodes),len(self._grafo.edges)