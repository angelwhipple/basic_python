class Node():
    """Represents a node in the graph"""

    def __init__(self, name):
        """
        Initializes  an instance of Node object.

        Parameters:
        name - object representing the name of the node
        """
        self.name = str(name)

    def get_name(self):
        """
        Returns:
        str, representing the name of the node
        """
        return self.name

    def __str__(self):
        """
        This is the function that is called when print(node) is called.

        Returns:
        str, humanly readable reprsentation of the node
        """
        return self.name

    def __repr__(self):
        """
        Formal string representation of the node

        Returns:
        str, the name of the node.
        """
        return self.name

    def __eq__(self, other):
        """
        This is function called when you use the "==" operator on nodes

        Parameters:
        other - Node object to compare against

        Returns:
        bool, True is self == other, false otherwise
        """
        if not isinstance(other, Node):
            return False
        return self.name == other.name

    def __ne__(self, other):
        """
        This is function called when you used the "!=" operator on nodes

        Parameters:
        other - Node object to compare against

        Returns:
        bool, True is self != other, false otherwise
        """
        return not self.__eq__(other)

    def __hash__(self):
        """
        Returns:
        Hash of the node. This function is necessary so that Nodes can be
        used as keys in a dictionary, Nodes are immutable
        """
        return self.name.__hash__()



class DirectedRoad():
    """Represents a road (edge) with a travel time (weight)"""

    def __init__(self, src_node, dest_node, travel_time, road_type, traffic_multiplier):
        """
        Initialize src_node, dest_node, travel_time, and road_type for the DirectedRoad class

        Parameters:
        src_node: Node, representing the source node
        dest_node: Node, representing the destination node
        travel_time: float, representing the time travelled between the src and dest
        road_type: str, representing the type of road of the edge
        traffic_multiplier: float, representing how much to multiply travel_time in the case of traffic
        The traffic multiplier will always be at least 1.
        """
        self.src_node = src_node
        self.dest_node = dest_node
        self.travel_time = travel_time
        self.road_type = road_type
        self.traffic_multiplier = traffic_multiplier

    def get_source_node(self):
        """
        Getter method for DirectedRoad

        Returns:
        Node, representing the source node
        """
        return self.src_node

    def get_destination_node(self):
        """
        Getter method for DirectedRoad

        Returns:
        Node, representing the destination node
        """
        return self.dest_node

    def get_road_type(self):
        """
        Getter method for DirectedRoad

        Returns:
        str, representing the road type of the road
        """
        return self.road_type

    def get_travel_time(self, has_traffic=False):
        """
        Gets the travel_time for this road. If there is traffic,
        - multiply the time it takes to travel on a road by its traffic multiplier

        Parameter:
        has_traffic - bool, True if there is traffic, False otherwise

        Returns:
        float, representing the time to travel from the source node to the destination node
        """
        if has_traffic:
            return self.travel_time*self.traffic_multiplier
        return self.travel_time

    def get_traffic_multiplier(self):
        """
        Getter method for DirectedRoad

        Returns:
        float, representing the traffic multiplier
        """
        return self.traffic_multiplier

    def __str__(self):
        """
        Function that is called when print() is called on a DirectedRoad object.

        Returns:
        str, with the format 'src -> dest takes travel_time minute(s) via road_type road with traffic multiplier traffic_multiplier'

        Note: For the total time assume normal traffic conditions
        """
        return "%s -> %s takes %s minute(s) via %s road with traffic multiplier %s" % (self.src_node, self.dest_node, self.travel_time, self.road_type, self.traffic_multiplier)

    def __hash__(self):
        return self.__str__().__hash__()


class RoadMap():
    """Represents a road map -> a directed graph of Node and DirectedRoad objects"""

    def __init__(self):
        """
        Initalizes a new instance of RoadMap.
        """
        self.nodes = set()
        # must be a dictionary of Node -> list of roads starting at that node
        self.nodes_to_roads = {}

    def __str__(self):
        """
        Function that is called when print() is called on a RoadMap object.

        Returns:
        str, representation of the RoadMap.
        """
        road_strs = []
        for roads in self.nodes_to_roads.values():
            for road in roads:
                road_strs.append(str(road))
        road_strs = sorted(road_strs)  # sort alphabetically
        return '\n'.join(road_strs)  # concat road_strs with "\n"s between them

    def get_all_nodes(self):
        """
        Return:
        a COPY of all nodes in the RoadMap. Does not modify self.nodes
        """
        return self.nodes.copy()

    def contains_node(self, node):
        """
        Param:
        node Node object

        Return:
        True, if node is in the graph. False, otherwise.
        """
        if node in self.nodes:
            return True
        return False

    def insert_node(self, node):
        """
        Adds a Node object to the RoadMap.
        Raises a ValueError if it is already in the graph.

        Param:
        node object
        """
        if self.contains_node(node):
            raise ValueError("Node already exists in graph.")
        self.nodes.add(node)
        self.nodes_to_roads[node] = []

    def insert_road(self, road):
        """
        Adds a DirectedRoad instance to the RoadMap.
        Raises a ValueError if either of the nodes associated with the road is not in the graph.

        Param:
        road, DirectedRoad object
        """
        if not (self.contains_node(road.get_source_node()) and self.contains_node(road.get_destination_node())):
            raise ValueError("Source or destination node not in graph.")
        self.nodes_to_roads[road.get_source_node()].append(road)

    def get_reachable_roads_from_node(self, node, restricted_roads):
        """
        Get the roads out of Node node, excluding roads whose types are in restricted_roads
        Param:
            node: Node
            find reachable roads out of this node

            restricted_roads: List of strings (types of roads)
            road types that cannot be traveled on

        Return:
            A new list of all the roads that start at given node,
            whose types are not in restricted_roads.
            Empty list if the node is not in the graph.
        """
        reachable_roads = []
        if self.contains_node(node) and len(self.nodes_to_roads[node]) != 0:
            for road in self.nodes_to_roads[node]:
                if not road.get_road_type() in restricted_roads:
                    reachable_roads.append(road)
        return reachable_roads
