class Node():
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        
        self.f = 0
        self.g = 0
        self.h = 0
        

def shortest_path(M, start, goal):
    start_node = Node(None, start)
    start_node.g = 0
    start_node.h = 0
    start_node.f = 0
    
    end_node = Node(None, goal)
    end_node.g = 0
    end_node.h = 0
    end_node.f = 0
    
    open_list = []
    closed_list = []
    
    open_list.append(start_node)
    
    while len(open_list) > 0:
        current_node = open_list[0]
        current_index = 0
        
        for i, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = i
                
        open_list.pop(current_node)
        closed_list.append(current_node)
        
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1]
        
        # generate children
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
            node_position = (
                current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            if node_position[0] > (len(M) - 1) or (node_position[0] < 0) or \
                (node_position[1] > (len(M[len(M) - 1]) - 1)) or node_position[1] < 0:  
                continue

            if M[node_position[0]][node_position[1]] != 0:
                continue

            new_node = Node(current_node, node_position)

            children.append(new_node)

        for child in children:

            for closed_child in closed_list:
                if child == closed_child:
                    continue

                        
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.posiion[0]) ** 2) \
                 + ((child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            open_list.append(child)


path = shortest_path(map_40, 5, 34)
if path == [5, 16, 37, 12, 34]:
    print('Great! your code works for these inputs!')
else:
    print('Something is wrong, your code produced the following:')
    print(path)