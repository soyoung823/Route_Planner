import heapq    # for using heap queue for priority queue
import math # for calculating distance

# Implement a min heap as a priority queue using heapq module.

class PriorityQueue:
    def __init__(self, array=[]):
        self.heap = []
        for value in array:
            heapq.heappush(self.heap, (0, value))

    def add(self, value, priority=0):
        heapq.heappush(self.heap, (priority, value))

    # The smallest priority node popped.
    def pop(self):
        (priority, value) = heapq.heappop(self.heap)
        return value

    def __len__(self):
        return len(self.heap)

# Helper functions
def make_path(predecessors, start, end):
    '''
    Given the dictionary of predecessors for each node on the map, an origin (start) and a destination (end)
    returns a path as we need to show from start to end.
    Args:
        (dict) predecessors: (int) keys: node ID. (int) values: node's predecessor
        (int) start: ID of the origin intersection
        (int) goal: ID of the destination intersection
    Returns:
        (float): Euclidean distance
    Example:
    >>> predecessors = {2: 1, 3: 1, 4: 3, 5: 4, 6: 4}
    >>> make_path(predecessors, 1, 5)
    ['1', '3', '4', '5']
    '''
    reversed_path = [end]

    while end != start:
        end = predecessors[end]
        reversed_path.append(end)

    return list(reversed(reversed_path)) # return ['1', '3', '4', '5']

# Euclidean distance h
def h_distance(xy1, xy2):
    '''
    Given the cartesian coordinates [x, y] of two points,
    returns the Euclidean distance.

    Args:
        (list) xy1: [float, float] first point
        (list) xy2: [float, float] second point
    Returns:
        (float): Euclidean distance
    '''
    x1 = xy1[0]
    y1 = xy1[1]

    x2 = xy2[0]
    y2 = xy2[1]

    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2) # get Euclidean distance

# return the shortest path by A* search algorithm
def shortest_path(M, start, goal):
    '''
    Given a map, an origin (start) and a destination (goal),
    returns the shortest path based on A* search algorithm.

    Args:
        (object) map: map of the 2D space
        (int) start: ID of the origin intersection
        (int) goal: ID of the destination intersection

    Returns:
        (list): list of integers representing a path from start (origin) to goal (destination)

    Note:
        The ID is a natural number in the interval [0 ... N - 1], 
        where N is the number of intersections (nodes) on the map.
    '''
    # dictionary of Map intersections coordinates [x, y]
    # {0: [0.7798606835438107, 0.6922727646627362], ... , 9: [0.1285377678230034, 0.3285840695698353]}
    nodes_xy = M.intersections

    # destination coordinates. [0.1285377678230034, 0.3285840695698353]
    goal_xy = nodes_xy[goal]

    # list of lists of neighbor nodes of each node
    # roads property is a list where, if i is an intersection, roads[] contains a list of the neighbor
    # intersections that intersection i connects to. [[7, 6, 5], [4, 3, 2], ..., [8]] List of lists.
    neighbors_list = M.roads

    # set to track the visited nodes in the search
    processed = set()

    # dictionary to track the predecessors in the path
    predecessors = dict()

    # initialize each node distance from start
    nodes_ids = nodes_xy.keys()  # keys list for M map's all intersections
    distance_start = dict()
    for node_id in nodes_ids:
        distance_start[node_id] = math.inf
    distance_start[start] = 0 # distance from start to start

    # p_queue as PriorityQueue and add start to it
    p_queue = PriorityQueue()
    p_queue.add(start)

    # loop until p_queue is empty.
    while p_queue:

        # get the node with the lowest priority (cost) from p_queue.
        node = p_queue.pop()

        # check if the node has been processed. ignore the processed node.
        if node in processed:
            continue
        
        # if goal node found: stop searching and recurse with the node.
        if node == goal:
            print("shortest path called ")
            return make_path(predecessors, start, node)

        # if goal node not found yet, the node is added to processed list.
        processed.add(node)

        # check all neighbors and update the cost function f for neighbor nodes near the node.
        node_xy = nodes_xy[node] # the node's x, y coordinates

        for neighbor in neighbors_list[node]:
            neighbor_xy = nodes_xy[neighbor]    # neighbor's x, y coordinates

            # total distance from the node to the neighbor node =
            # (exact distance for start -> the node) + (heuristic distance for the node -> the neighbor node)
            cost_g = distance_start[node] + h_distance(node_xy, neighbor_xy)

            # h_distance for the neighbor node -> the goal node.
            cost_h = h_distance(neighbor_xy, goal_xy)

            # estimated distance (cost) of the path from start to goal via the neighbor's position (x, y coordinates)
            cost_f = cost_g + cost_h

            # if the estimated distance is lower than the exact distance.
            if cost_g < distance_start[neighbor]:

                # update neighbor's distance, predecessor and add it to the pp_queue with priority.
                distance_start[neighbor] = cost_g
                predecessors[neighbor] = node
                p_queue.add(neighbor, priority=cost_f)

    # if the graph can't be traveled.
    print("if the graph can't be traveled, the shortest path is ")
    return None
