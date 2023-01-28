from collections import defaultdict
from itertools import combinations
class Matrix:
    # https://www.geeksforgeeks.org/tarjan-algorithm-find-strongly-connected-components/
    def __init__(self):
        self.graph = defaultdict(set)
        self.Time = 0
        self.cycles = []

    def addEdge(self, u, v):
        self.graph[u] |= set((v,))
        self.graph[v] |= set()

    def SCCUtil(self, u, low, disc, stackMember, st):
        disc[u] = self.Time
        low[u] = self.Time
        self.Time += 1
        stackMember[u] = True
        st.append(u)
        for v in self.graph[u]:
            if disc[v] == -1:
                self.SCCUtil(v, low, disc, stackMember, st)
                low[u] = min(low[u], low[v])
            elif stackMember[v] == True:
                low[u] = min(low[u], disc[v])
        w = -1
        if low[u] == disc[u]:
            tmp = []
            while w != u:
                w = st.pop()
                tmp.append(w)
                stackMember[w] = False
            self.cycles.append(tmp[::-1])

    def SCC(self):
        V = len(self.graph)
        disc = [-1] * (V)
        low = [-1] * (V)
        stackMember = [False] * (V)
        st = []
        for i in range(V):
            if disc[i] == -1:
                self.SCCUtil(i, low, disc, stackMember, st)
        self.cycles = [c for c in self.cycles if len(c) > 1]
    def sub_SCC(self):
        self.sub_cycles = {tuple(c):set() for c in self.cycles}
        for cycle in self.sub_cycles:
            for i in range(2,len(cycle)):
                for test_cycle in combinations(cycle,r=i):
                    test_m = Matrix()
                    test_cycle = set(test_cycle)
                    mapping = {v:idx for idx,v in enumerate(test_cycle)}
                    reverse_mapping = {idx:v for idx,v in enumerate(test_cycle)}
                    for v in test_cycle:
                        test_m.graph[mapping[v]] = set(mapping[e] for e in (self.graph[v] & test_cycle))
                    test_m.SCC()
                    self.sub_cycles[cycle] |= set(tuple(reverse_mapping[v] for v in test_m_cycle) for test_m_cycle in test_m.cycles)
if __name__ == "__main__":

    m = Matrix()
    m.addEdge(0,1)
    m.addEdge(1,2)
    m.addEdge(1,3)
    m.addEdge(2,4)
    m.addEdge(3,0)
    m.addEdge(3,1)
    m.addEdge(4,2)
    m.addEdge(1,5)
    m.addEdge(5,0)

    m.SCC()
    m.sub_SCC()
    print(m.cycles)
    print(m.sub_cycles)