import networkx as nx
import matplotlib.pyplot as plt

graph = {
    '5': [('3', 10), ('7', 15)],
    '3': [('2', 20), ('4', 25)],
    '7': [('8', 30)],
    '4': [('8', 35)],
    '2': [('4', 40)],
    '8': [('9', 0)],
}

G = nx.Graph()
G.add_nodes_from(graph.keys())

for node, neighbors in graph.items():
    for neighbor, weight in neighbors:
        G.add_edge(node, neighbor, weight=weight)

pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True)
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

plt.show()
