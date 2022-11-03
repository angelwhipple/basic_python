# Finding shortest paths to drive from home to work on a road network

from graph import DirectedRoad, Node, RoadMap


# Nodes represent locations: home, office, school, supermarket, etc
# Edges represent roads connecting connecting these locations on the map
# Travel times represented as an attribute of the edges, ex: a road (edge) may have 
# a travel time attribute dictating how long it takes to get from that edge's source to destination node

def load_map(map_filename):
    """
    Parses the map file and constructs a road map (graph).

    Travel time and traffic multiplier should be cast to a float.

    Parameters:
        map_filename : String
            name of the map file

    Assumes:
        Each entry in the map file consists of the following format, separated by spaces:
            source_node destination_node travel_time road_type traffic_multiplier

        Note: hill road types always are uphill in the source to destination direction and
              downhill in the destination to the source direction. Downhill travel takes
              half as long as uphill travel. The travel_time represents the time to travel
              from source to destination (uphill).

        e.g.
            N0 N1 10 highway 1
        This entry would become two directed roads; one from 'N0' to 'N1' on a highway with
        a weight of 10.0, and another road from 'N1' to 'N0' on a highway using the same weight.

        e.g.
            N2 N3 7 hill 2
        This entry would become two directed roads; one from 'N2' to 'N3' on a hill road with
        a weight of 7.0, and another road from 'N3' to 'N2' on a hill road with a weight of 3.5.

    Returns:
        a directed road map representing the inputted map
    """
    roads = []
    road_map = RoadMap()
    # Opening map file
    map_data = open(map_filename, 'r')
    # Reading each line of the map file
    for line in map_data:
        road_data = line.split(" ", 4)
        # Converting each map entry into 2 DirectedRoad objects
        # Appending both directed roads to a list of directed roads
        roads.append(DirectedRoad(Node(road_data[0]), Node(road_data[1]), float(road_data[2]), road_data[3], float(road_data[4])))
        if road_data[3] == 'hill':
            roads.append(DirectedRoad(Node(road_data[1]), Node(road_data[0]), float(road_data[2])/2, road_data[3], float(road_data[4])))
        else:    
            roads.append(DirectedRoad(Node(road_data[1]), Node(road_data[0]), float(road_data[2]), road_data[3], float(road_data[4])))
    # Adding each road to the directed road map
    for road in roads:
        try:
            road_map.insert_node(road.get_source_node())
            road_map.insert_node(road.get_destination_node())
        except ValueError:
            try:
                road_map.insert_node(road.get_destination_node())
            except ValueError:
                pass
        finally:
            road_map.insert_road(road)
    return road_map
    

# Testing load_map
# road_map = load_map("maps/test_load_map.txt")
# print(road_map)



# Finding the shortest path using optimized search method



# Problem 3a: Objective function
#
# What is the objective function for this problem? What are the constraints?
#
# Objective func: travel time between specified start and end nodes on directed road map
# Constraint(s): path found (if exists) must take least amount of total travel time

def find_optimal_path(roadmap, start, end, restricted_roads, has_traffic=False):
    """
    Finds the shortest path between start and end nodes on the road map,
    without using any restricted roads,
    following traffic conditions.
    Follows Dijkstra's algorithm.

    Param:
    roadmap - RoadMap
        The graph on which to carry out the search
    start - Node
        node at which to start
    end - Node
        node at which to end
    restricted_roads - list[string]
        Road Types not allowed on path
    has_traffic - boolean
        flag to indicate whether to get shortest path during traffic or not

    Returns:
    A tuple of the form (best_path, best_time).
        The first item is the shortest path from start to end, represented by
        a list of nodes (Nodes).
        The second item is a float, the length (time traveled)
        of the best path.

    If there exists no path that satisfies constraints, then return None.
    """
    # Checking for start node = end node to see if function body is necessary
    if start == end:
        return ([start], 0.0)
    else:
        # Marking all nodes in the road map as unvisited
        unvisited = roadmap.get_all_nodes()
        # Setting travel time to each node as inf, 0.0 for start node
        time_to = {node: float('inf') for node in unvisited}
        time_to[start] = 0.0
        # Marking all nodes as not yet having a predecessor node in path
        predecessor = {node: None for node in unvisited}
        while unvisited:
            # Setting current node as node with min travel time from start
            current = min(unvisited, key=lambda node: time_to[node])
            # Break out of loop if min travel time among unvisited nodes is inf
            if time_to[current] == float('inf'):
                break
            # Checking each road beginning at current node
            for road in roadmap.get_reachable_roads_from_node(current, restricted_roads):
                # Calculating travel time from current node to dest node through road
                alt_path_time = time_to[current] + road.get_travel_time(has_traffic)
                # Updating path travel time to dest node if newly calculated
                # travel time through current is less than saved travel time 
                if alt_path_time < time_to[road.get_destination_node()]:
                    time_to[road.get_destination_node()] = alt_path_time
                    # Update predecessor for dest node according to
                    # newly calculated path w/ shorter travel time
                    predecessor[road.get_destination_node()] = current
            # Marking current node as visited
            unvisited.remove(current)
        try:
            # Assembling an optimal path from end to start using predecessor
            best_path = []
            current = end
            while predecessor[current] != None:
                best_path.insert(0, current)
                current = predecessor[current]
            if best_path != []:
                best_path.insert(0, current)
            # Return None if an optimal path from start -> end doesn't exist
            else:
                return None
            # Set best time to shortest calculated travel time from start to end
            best_time = time_to[end]
            return (best_path, best_time)
        except KeyError:
            return None
    

def find_optimal_path_no_traffic(filename, start, end):
    """
    Finds the shortest path from start to end during conditions of no traffic.

    Uses find_optimal_path and load_map.

    Param:
    filename - name of the map file that contains the graph
    start - Node, node object at which to start
    end - Node, node object at which to end

    Returns:
    list of Node objects, the shortest path from start to end in normal traffic.
    If there exists no path, then return None.
    """
    # Creating the road map from map file
    road_map = load_map(filename)
    # Call to find_optimal_path with no restricted roads, no traffic
    optimal_path_and_time = find_optimal_path(road_map, start, end, [])
    return optimal_path_and_time[0]


def find_optimal_path_restricted(filename, start, end):
    """
    Finds the shortest path from start to end when local roads and hill roads cannot be used.

    Uses find_optimal_path and load_map.

    Param:
    filename - name of the map file that contains the graph
    start - Node, node object at which to start
    end - Node, node object at which to end

    Returns:
    list of Node objects, the shortest path from start to end given the aforementioned conditions,
    If there exists no path that satisfies constraints, then return None.
    """
    # Creating the road map from map file
    road_map = load_map(filename)
    # Call to find_optimal_path with local/hill roads restricted, no traffic
    optimal_path_and_time = find_optimal_path(road_map, start, end, ['local', 'hill'])
    return optimal_path_and_time[0]
    

def find_optimal_path_in_traffic_no_toll(filename, start, end):
    """
    Finds the shortest path from start to end when toll roads cannot be used and in traffic,
    i.e. when all roads' travel times are multiplied by their traffic multipliers.

    Uses find_optimal_path and load_map.

    Param:
    filename - name of the map file that contains the graph
    start - Node, node object at which to start
    end - Node, node object at which to end; you may assume that start != end

    Returns:
    The shortest path from start to end given the aforementioned conditions,
    represented by a list of nodes (Nodes).

    If there exists no path that satisfies the constraints, then return None.
    """
    # Creating the road map from map file
    road_map = load_map(filename)
    # Call to find_optimal_path with toll roads restricted and traffic
    optimal_path_and_time = find_optimal_path(road_map, start, end, ['toll'], True)
    return optimal_path_and_time[0]
    


if __name__ == '__main__':

    # rmap = load_map('./maps/small_map.txt')

    # start = Node('N0')
    # end = Node('N4')
    # restricted_roads = []

    # print(find_optimal_path(rmap, start, end, restricted_roads))
