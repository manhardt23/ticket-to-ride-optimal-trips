

import networkx as nx
from networkx import contracted_nodes


class Board:

    def __init__(self):
        self.G = Board.build_graph()
        self.hash = {}
        self.reverse_hash = {}
        self.trains_left = 45

    @staticmethod
    def get_trips():
        fd = open('trips.txt', 'r')
        lines = fd.readlines()
        lines = [i[:-1] for i in lines]
        lines = [i.split() for i in lines]
        lines = [(edge[0], edge[1], (int(edge[2]))) for edge in lines]
        return lines

    @staticmethod
    def get_nodes() -> list:
        fd = open('cities.txt', 'r')
        lines = fd.readlines()
        lines = [i[:-1] for i in lines]
        return lines

    @staticmethod
    def get_edges():
        fd = open('tracks.txt', 'r')
        lines = fd.readlines()
        lines = [i[:-1] for i in lines]
        lines = [i.split() for i in lines]
        lines = [(edge[0], edge[1], (int(edge[2]), int(edge[3]))) for edge in lines]
        #(int(edge[2]), int(edge[3]))
        return lines

    @staticmethod
    def build_graph():
        nodes = Board.get_nodes()
        edges = Board.get_edges()
        #print(nodes)
        G = nx.Graph()
        G.add_nodes_from(nodes)
        #G.add_edges_from((u, v) for (u, v) in edges)

        G.add_edges_from((u, v, {'weight': w, 'trains': t, 'ratio' : (w/t)}) for (u, v, (w, t)) in edges)
        #print(list (G.nodes))
        return G
    def get_graph(self):
        return self.G
    
    def set_mapping(self, old, new):
        # the old node is the key while the new node will be the value
        if new not in self.reverse_hash:
            self.reverse_hash[new] = [old]
        else:
            self.reverse_hash[new].append(old)
        self.hash[old] = new
        
    def get_mapping_for(self, old):
        #getting the new location of the node
        return self.hash.get(old)

    def get_mapping_reverse(self, new):
        return self.reverse_hash.get(new)
    
    def unmap_path(self, path):
        """
        Try to find the original names for each node in a condensed path.
        If the node is an original, leave it. If it's a representative node,
        attempt to find a unique reverse mapping from the original nodes.
        """
        unmapped = []

        for node in path:
            # Check if this node was ever used as a "new" mapping target
            original_names = [old for old, new in self.hash.items() if new == node]

            if not original_names:
                # This node is likely not a contraction target — it's original
                unmapped.append(node)
            else:
                # Include the node itself if it was the rep
                if node not in original_names:
                    original_names.insert(0, node)

                # Best guess: pick the one that hasn’t been used yet in the path
                for candidate in original_names:
                    if candidate not in unmapped:
                        unmapped.append(candidate)
                        break
                else:
                    # fallback
                    unmapped.append(original_names[0])
        
        #print("Input path:", path)
        #print("Unmapped path:", unmapped)
        return unmapped



    def collapse(self, path):
        # Condensing the already determined path down to one node
        # this is done so that we are not spending trains or recounting the points
        H = self.G
        for i in range(len(path)):
            #print(H)
            if i + 1 < len(path):
                Board.set_mapping(self, path[i + 1], path[0])
                H = contracted_nodes(H, path[0], path[i + 1], False, False)

        self.G = H
    
    def sub_trains(self, used_trains):
        self.trains_left = self.trains_left - used_trains

    def get_trains_left(self):
        return self.trains_left




