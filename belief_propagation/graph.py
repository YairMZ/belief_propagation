from __future__ import annotations
import networkx as nx
from .node import VNode, CNode
import numpy as np
import numpy.typing as npt


class TannerGraph:
    def __init__(self):
        self.v_nodes: dict[int, VNode] = {}
        self.c_nodes: dict[int, CNode] = {}
        self.edges = set()

    def add_v_node(self, name: str = "", node: VNode = None) -> VNode:
        """
        :param name: names must be unique.
        :param node: add an exiting node to graph. If not used a new node is created.
        """
        if node is None:
            node = VNode(name)
        self.v_nodes[node.uid] = node
        return node

    def add_c_node(self, name: str = "", node: CNode = None) -> CNode:
        """
        :param name: names must be unique
        :param node: add an exiting node to graph. If not used a new node is created.
        """
        if node is None:
            node = CNode(name)
        self.c_nodes[node.uid] = node
        return node

    def add_edge(self, vnode_uid: int, cnode_uid: int) -> None:
        if vnode_uid not in self.v_nodes:
            raise ValueError()
        if cnode_uid not in self.c_nodes:
            raise ValueError()
        self.c_nodes.get(cnode_uid).register_neighbor(self.v_nodes.get(vnode_uid))
        self.v_nodes.get(vnode_uid).register_neighbor(self.c_nodes.get(cnode_uid))
        self.edges.update({(vnode_uid, cnode_uid)})

    def add_edges_by_uid(self, edges_set: set[tuple[int, int]]) -> None:
        """
        :param edges_set: each element in the set is a tuple. In the tuple first element is a v-node uid and second is
        c-node uid
        """
        for v_uid, c_uid in edges_set:
            if v_uid not in self.v_nodes:
                raise ValueError("No v-node with uid " + str(v_uid) + " in graph")
            if c_uid not in self.c_nodes:
                raise ValueError("No c-node with uid " + str(c_uid) + " in graph")
            self.add_edge(v_uid, c_uid)

    def add_edges_by_name(self, edges_set: set[tuple[str, str]]) -> None:
        """
        :param edges_set: each element in the set is a tuple. In the tuple first element is a v-node name and second is
        c-node name
        """
        for v_name, c_name in edges_set:
            v_uid = [node.uid for node in self.v_nodes.values() if node.name == v_name]
            if not v_uid:
                raise ValueError("No v-node with name " + v_name + " in graph")
            c_uid = [node.uid for node in self.c_nodes.values() if node.name == c_name]
            if not c_uid:
                raise ValueError("No c-node with name " + c_name + " in graph")
            self.add_edge(v_uid[0], c_uid[0])

    def get_edges(self, by_name=False) -> set:
        """
        :param by_name: if true nodes are referred to by name, otherwise by uid. Default to false
        :return: returns a set of edges. if by_name each element is a tuple of node names, else it is a tuple of uid's.
        """
        if not by_name:
            return self.edges
        return {(self.v_nodes.get(vnode).name, self.c_nodes.get(cnode).name) for vnode, cnode in self.edges}

    def to_nx(self) -> nx.Graph:
        g = nx.Graph()
        for uid, node in self.c_nodes.items():
            g.add_node(uid, label=node.name, bipartite=0, color="blue")
        for uid, node in self.v_nodes.items():
            g.add_node(uid, label=node.name, bipartite=1, color="red")
        g.add_edges_from(self.edges)
        return g

    @classmethod
    def from_biadjacency_matrix(cls, h: npt.ArrayLike) -> TannerGraph:
        """
        :param h: parity check matrix, shape MXN with M check nodes and N variable nodes. assumed binary matrix.
        """
        g = TannerGraph()
        h = np.array(h)
        m, n = h.shape
        for i in range(n):
            g.add_v_node(name="v" + str(i))
        for j in range(m):
            g.add_c_node(name="c" + str(j))
            for i in range(n):
                if h[j, i] == 1:
                    g.add_edges_by_name({("v" + str(i), "c" + str(j))})
        return g

    def __str__(self) -> str:
        return "Graph with " + str(len(self.c_nodes) + len(self.v_nodes)) + " nodes and " + str(len(self.edges)) + \
               " edges"
