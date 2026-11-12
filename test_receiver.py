import networkx as nx
import receiver_analysis

g = nx.DiGraph()

g.add_edges_from([
    ("A", "B"),
    ("B", "C"),
    ("C", "D"),
    ("B", "E"),
    ("A", "F"),
    ("F", "G"),
    ("G", "H"),
    ("A", "I"),
    ("I", "J")
])

result = receiver_analysis.rank_end_receivers(g, "A", 3)

print("Receivers found:", len(result))

for receiver in result:
    print(receiver)
