

import networkx as nx
import matplotlib.pyplot as plt

class Visualize:
    def __init__(self, G, city_positions):
        self.G = G
        self.city_positions = city_positions

    def vis(self, highlight_paths=None):
        plt.figure(figsize=(14, 10))

        # --- Draw the full board faintly ---
        nx.draw(
            self.G,
            self.city_positions,
            with_labels=True,
            node_size=500,
            node_color="lightgray",
            font_size=8,
            font_weight="bold",
            edge_color="lightgray",
        )

        # --- Highlight chosen paths (but only edges that exist in the graph) ---
        if highlight_paths:
            highlight_edges = []
            for path in highlight_paths:
                if not path:
                    continue
                for i in range(len(path) - 1):
                    u, v = path[i], path[i + 1]
                    if self.G.has_edge(u, v):  # ✅ only draw if edge exists
                        highlight_edges.append((u, v))

            nx.draw_networkx_edges(
                self.G,
                self.city_positions,
                edgelist=highlight_edges,
                edge_color="red",
                width=3,
            )
            nx.draw_networkx_nodes(
                self.G,
                self.city_positions,
                nodelist=set(sum(highlight_paths, [])),  # flatten all paths
                node_color="lightblue",
                node_size=600,
            )

        plt.axis("off")
        plt.show()
