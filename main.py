

from visualize import Visualize
import pathing
import graphCreate
import time
import os
import json


def main():
    start = time.time()
    save_file = "results.json"

    if os.path.exists(save_file):
        print("Loading saved results...\n")
        with open(save_file, "r") as f:
            data = json.load(f)
        points, paths, trips = data["points"], data["paths"], data["trips"]
    else:
        print("Running expensive calculation, please wait...\n")
        board = graphCreate.Board()
        path_find = pathing.PathFinder(board)
        points, paths, trips = path_find.max_set_trips()

        # Save results for next time
        with open(save_file, "w") as f:
            json.dump({"points": points, "paths": paths, "trips": trips}, f)
    
    print(f"Total Points Scored: {points}\n")
    print()
    
    print("Paths Taken:")
    count = 1
    for path in paths:
        if path:  # skip empty lists
            print(f"  {count}. " + " → ".join(path))
            count += 1
    print()
    
    print("Trip Cards Used:")
    for trip in trips:
        start_city, end_city, score = trip
        print(f"  - {start_city} → {end_city} ({score} points)")
    print()
    
    end = time.time()
    print(f"Elapsed Time: {end - start:.2f} seconds")


    from city_positions import city_positions
    board_vis = graphCreate.Board()
    vis = Visualize(board_vis.G, city_positions)
    vis.vis(highlight_paths=paths)


    

    


    

if __name__ == '__main__':
    main()