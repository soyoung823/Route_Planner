import heapq
import math

# test heapify
a = [3, 5, 1, 2, 6, 8, 7]
heapq.heapify(a)
print(a)
print(list(a))

# Reference: https://leetcode.com/problems/shortest-path-in-binary-matrix/discuss/313347/A*-search-in-Python
# a priority queue using heapq.
class PriorityQueue:
    
    def __init__(self):
        self.elements = []

    def add(self, value, priority=0):
        heapq.heappush(self.elements, (priority, value))

    def pop(self):
        return heapq.heappop(self.elements)[1]

# test priority queue 
pq = PriorityQueue()
pq.add(1)
pq.add(2)
pq.add(3)
print(pq.elements)
print(pq.pop())
print(pq.elements)
print(pq.pop())
print(pq.elements)
print(pq.pop())
print(pq.elements)
pq1 = PriorityQueue()
print(pq1.elements)
pq1.add(1)
print(pq1.elements)

# make the path from to end using previous_intersections_dict dictionary
def make_path(previous_intersections_dict, start, end):
    '''
    previous_intersections_dict = {2: 1, 3: 1, 4: 3, 5: 4, 6: 4}
    make_path(previous_intersections_dict, 1, 5)
    ['1', '3', '4', '5']
    '''
    res = []
    res.append(end)
  
    while end != start:
        end = previous_intersections_dict[end]
        res.append(end)

    return list(reversed(res)) # return ['1', '3', '4', '5']

# return the shortest path for given a Map, a start intersection and a goal intersection
def shortest_path(M, start, goal):

    # dictionary of Map intersections [x, y] coordinates with ID
    # {0: [0.7798606835438107, 0.6922727646627362], ... , 9: [0.1285377678230034, 0.3285840695698353]}
    all_intersections_xy = M.intersections

    # goal intersection coordinates. [0.1285377678230034, 0.3285840695698353]
    goal_intersection_xy = all_intersections_xy[goal]

    # list of lists of adjacent neighbor intersections of each intersection
    # roads property is a list where, if i is an intersection, roads[] contains a list of the adjacent neighbor
    # intersections that intersection i connects to. [[7, 6, 5], [4, 3, 2], ..., [8]] List of lists.
    neighbor_intersections_list = M.roads

    # set to track the visited intersections in the search
    visited_intersections_list = set()

    # dictionary to track the previous_intersections_dict in the path
    previous_intersections_dict = dict()

    # set each intersection distance from start
    intersections_ids = all_intersections_xy.keys()  # keys list for a map's all intersections
    distance_from_start = dict()
    
    for intersection_id in intersections_ids:
        distance_from_start[intersection_id] = math.inf # set max integer
    distance_from_start[start] = 0 # distance from start to start

    # p_queue as PriorityQueue and add start to it
    p_queue = PriorityQueue()
    p_queue.add(start)

    # loop until p_queue is empty.
    while p_queue:

        # get the intersection with the lowest priority (cost) from p_queue.
        current_intersection = p_queue.pop()

        # if the current intersection has been vistied, ignore it.
        if current_intersection in visited_intersections_list:
            continue
        
        # if goal intersection found: stop searching and return the shortest path.
        if current_intersection == goal:
            print("shortest path called ")
            return make_path(previous_intersections_dict, start, current_intersection)

        # if goal intersection is not found, the current intersection is added to visited_intersections_list.
        visited_intersections_list.add(current_intersection)

        # check all neighbor intersections and update the distance function f for neighbor intersections near the intersection.
        current_intersection_xy = all_intersections_xy[current_intersection] # the current intersection's x, y coordinates

        for neighbor_intersection in neighbor_intersections_list[current_intersection]:
            neighbor_intersection_xy = all_intersections_xy[neighbor_intersection]    # neighbor's x, y coordinates

            # total distance from the intersection to the neighbor intersection =
            # (exact distance for start -> the intersection) + (heuristic Euclidean distance for the intersection -> the neighbor intersection)
            distance_g = distance_from_start[current_intersection] + math.sqrt(math.pow(current_intersection_xy[0] - neighbor_intersection_xy[0], 2) + math.pow(current_intersection_xy[1] - neighbor_intersection_xy[1], 2))

            # heuristic Euclidean distance for the neighbor intersection -> the goal intersection.
            distance_h = math.sqrt(math.pow(neighbor_intersection_xy[0] - goal_intersection_xy[0], 2) + math.pow(neighbor_intersection_xy[1] - goal_intersection_xy[1], 2))

            # estimated distance (cost) of the path from start to goal via the neighbor's position (x, y coordinates)
            distance_f = distance_g + distance_h

            # if the estimated distance is lower than the exact distance.
            if distance_g < distance_from_start[neighbor_intersection]:

                # update neighbor's distance, previous_intersections_dict and add it to the pp_queue with priority.
                distance_from_start[neighbor_intersection] = distance_g
                previous_intersections_dict[neighbor_intersection] = current_intersection
                p_queue.add(neighbor_intersection, priority=distance_f)

    # if the graph can't be traveled.
    print("if the graph can't be traveled, the shortest path is ")
    return None
