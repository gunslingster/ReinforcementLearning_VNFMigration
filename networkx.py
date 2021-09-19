import networkx as nx
from fat_tree import fatTree
import matplotlib.pyplot as plt

tree = fatTree(2)
G = nx.Graph()
G.add_nodes_from(tree.vertices)
G.add_edges_from(tree.edges)
subax1 = plt.subplot(121)
nx.draw(G)
nx.draw_shell(G)


