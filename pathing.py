

import networkx as nx
from itertools import combinations
import graphCreate


class PathFinder:

    def __init__(self, board):
        self.board = board
        self.G = self.board.get_graph()
        
    def resolve_mapping(self, node, max_depth=10):
        """
        Follows the mapping until it either finds a node in the graph or hits max depth.
        """
        visited = set()
        for _ in range(max_depth):
            if node in self.G:
                return node
            if node in visited:
                break  # Prevent infinite loops
            visited.add(node)
            node = self.board.get_mapping_for(node)
            if node is None:
                break
        return None



    def check_in_graph(self, trip):
        start_orig, end_orig = trip[0], trip[1]

        start = self.resolve_mapping(start_orig)
        end = self.resolve_mapping(end_orig)

        if start and end:
            #print(f"Resolved start: {start_orig} ➝ {start}")
            #print(f"Resolved end:   {end_orig} ➝ {end}")

            if start in self.G and end in self.G:
                if nx.has_path(self.G, start, end):
                    paths = list(nx.all_shortest_paths(self.G, start, end))
                    return paths
                else:
                    print(f"No path between {start} and {end}")
                    return 0, []
        else:
            raise ValueError(f"Could not find nodes in graph after remapping: start={start}, end={end}")


    def path_finder_max(self, trip):
        '''
            Params: 
                G: Graph networkx of the ticket to ride map
                trip: Tuple of starting and ending

            This function is finding all of the shortest path and taking the one with the max amount of points

            Returns a tuple of the points scored by placed trains and the list of the path from node to node
        '''
        the_path1 = ''
        max_weight = 0
        paths = PathFinder.check_in_graph(self, trip)
        for path in paths:
            weighted = []
            for i in range(len(paths[0]) - 1):
                data = self.G.get_edge_data(path[i], path[i + 1])
                weighted.append(data.get("weight"))
            if max_weight < sum(weighted):
                max_weight = sum(weighted)
                the_path1 = path
        return max_weight, the_path1

    def get_trains_used(self, path):
        #gets the trains used for each path made 

        train = 0
        for i in range(len(path) - 1):
            data = self.G.get_edge_data(path[i], path[i + 1])
            if data == None:
                #print(f"this is the path i {path[i]}")
                #print(f"this is the path i + 1 {path[i + 1]}")
                b = self.board.get_mapping_reverse(str(path[i]))
                c = self.board.get_mapping_reverse(str(path[i + 1]))
                #print(f"reverse map of path i {b}")
                #print(f"reverse map of path i + 1 {c}")
            else:
                train += data.get("trains")
        self.board.sub_trains(train)

    def one_path(self, trips):
        # connecting multiple trips on one board
        return None
    
    def max_set_trips(self):
        the_path3 = []
        max_comb = 0
        count = 10
        trips = graphCreate.Board.get_trips()
        comb = combinations(trips, count)
        for trip in comb:
            #print(f"this is the current set {trip}")
            points = 0
            for i in range(len(trip)):
                points += trip[i][2]
            if points < 150:
                continue
            board1 = graphCreate.Board()
            path_finder1 = PathFinder(board1)
            set_value = 0
            current_path = []
            for t in trip:
                #print(f"this is the current trip {t}")
                value, path = path_finder1.path_finder_max(t)
                value += t[2]
                path_finder1.get_trains_used(path)
                board1.collapse(path)
                current_path.append(path)
                set_value += value
                if board1.get_trains_left() <= 0:
                    current_path = []
                    set_value = 0
                    break
            if set_value > max_comb:
                max_comb = set_value
                best_set_trips = trip
                the_path3 = [board1.unmap_path(p) for p in current_path]
        
        return max_comb, the_path3, best_set_trips




                



    def max_trip(self):
        '''
            Params:
                G: Graph networkx of the ticket to ride map
            
            This iterates through all of the trips and finds the one with the max point from both trains and ticket points
            It uses the path_finder_max function to find the shortest path with the most amount of points
            
            This returns a tuple with the trip used the total points scored and the path taken
        '''
        max_value = 0
        trips = graphCreate.Board.get_trips()
        for trip in trips:
            (weight, path) = PathFinder.path_finder_max(self, trip)
            print(weight)
            print(path)
            if max_value < weight + trip[2]:
                max_value = weight + trip[2]
                the_path2 = path
                the_trip = trip
        PathFinder.get_trains_used(self, list(the_path2))
        print(f"trip {the_trip} and the path {the_path2}")
        return the_trip, max_value, the_path2

