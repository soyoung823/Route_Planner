import numpy as np

class Node:
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

# path function
def return_path(current_node, maze):
    path = []
    no_rows, no_columns = np.shape(maze)

    result = [[-1 for i in range(no_columns)] for j in range(no_rows)]
    current = current_node
    while current is not None:
        path.append(current.position)
        current = current.parent
    
    path = path[::-1]
    start_value = 0

    for i in range(len(path)):
        result[path[i][0]][path[i][1]] = start_value
        start_value += 1
    return result

# search function
def search(maze, cost, start, end):
    start_node = Node(None, tuple(start))
    start_node.g = 0
    start_node.h = 0
    start_node.f = 0

    end_node = Node(None, tuple(start))
    end_node.g = 0
    end_node.h = 0
    end_node.f = 0

    yet_to_visit_list = []
    visited = []
    yet_to_visit_list.append(start_node)

    outer_iterations = 0
    max_iterations = (len(maze) // 2) ** 10

    move = [[-1, 0], 
            [0, -1],
            [1, 0], 
            [0, 1]]

    no_rows, no_columns = np.shape(maze)

    while len(yet_to_visit_list) > 0:
        outer_iterations += 1

    current_node = yet_to_visit_list[0]
    current_index = 0
    for index, item in enumerate(yet_to_visit_list):
        if item.f < current_node.f:
            current_node = item
            current_index = index

    if outer_iterations > max_iterations:
        print('giving up on pathfinding too many iterations')
        return return_path(current_node, maze)

    yet_to_visit_list.pop(current_index)
    visited.append(current_node)

    if current_node == end_node:
        return return_path(current_node, maze)

    # Generate children from all adjacent squares
    children = []
    
    for new_position in move:
        # get node position
        node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

        # Make sure within range (check if within maze boundary)
        if (node_position[0] > (no_rows - 1) or
            node_position[0] < 0 or
            node_position[1] > (no_columns - 1) or
            node_position[1] < 0):
            continue
            
        # Make sure walkable terrain
        if maze[node_position[0]][node_position[1]] != 0:
            continue

        # Create new node
        new_node = Node(current_node, node_position)

        # Append
        children.append(new_node)

    # Loop through children
    for child in children:
        # Child is on the visited list (search entire visited list)
        if len([visited_child for visited_child in visited if visited_child]) > 0:
            continue

        # Create the f, g, and h values
        child.g = current_node.g + cost
        ## Heuristic costs calculated here, this is using euclidean distance
        child.h = (((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2))

        child.f = child.g + child.h

        # Child is already in the yet_to_visit list and g cost is already lower.
        if len([i for i in yet_to_visit_list if child == i and child.g > i.g]) > 0:
            continue

        # Add the child to the yet_to_visit list
        yet_to_visit_list.append(child)


if __name__ == '__main__':

    maze = [[0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0], 
            [0, 1, 0, 1, 0, 0],
            [0, 1, 0, 0, 1, 0],
            [0, 0, 0, 0, 1, 0]]

    start = [0, 0] # starting position
    end = [4, 5] # ending position
    cost = 1 # cost per movement

    path = search(maze, cost, start, end)
    print(path)

