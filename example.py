from belief_propagation import TannerGraph
from networkx.algorithms import bipartite

tg = TannerGraph()
# add 10 variable nodes
for i in range(10):
    tg.add_v_node(name="v"+str(i))
# add 5 check nodes
for i in range(5):
    tg.add_c_node(name="c"+str(i))

# add a bunch of edges
edges = {("v0", "c0"), ("v0", "c1"), ("v1", "c0"), ("v1", "c2"), ("v2", "c0"), ("v2", "c3"), ("v3", "c0"), ("v3", "c4"),
         ("v4", "c1"), ("v4", "c2"), ("v5", "c1"), ("v5", "c3"), ("v6", "c1"), ("v6", "c4"), ("v7", "c2"), ("v7", "c3"),
         ("v8", "c2"), ("v8", "c4"), ("v9", "c3"), ("v9", "c4")}
tg.add_edges_by_name(edges)

# turn to networkx graph
g = tg.to_nx()
H = bipartite.biadjacency_matrix(g, list(tg.c_nodes.keys()), column_order=tg.v_nodes.keys()).toarray()

# or construct from matrix
tg2 = TannerGraph.from_biadjacency_matrix(H)


import networkx as nx
import matplotlib.pyplot as plt
fig = plt.figure()
top = nx.bipartite.sets(g)[0]
labels = {node: d["label"] for node,d in g.nodes(data=True)}
nx.draw_networkx(g,
                 with_labels=True,
                 node_color=[d["color"] for d in g.nodes.values()],
                 pos=nx.bipartite_layout(g, top),
                 labels=labels)
fig.show()
fig.savefig("example_graph.png")
