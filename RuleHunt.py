class Node:
    EMPTY = 0
    WOLF = 1
    SHEEP = 2
    def __init__(self, state=Node.EMPTY):
        self.state = state


def rule(state, neighbors):
    SHEEP = 2 # green
    WOLF = 1 # red
    
    wolfs_count = sum(filter(lambda x: x==WOLF, neighbors))
    sheeps_count = sum(filter(lambda x: x==SHEEP, neighbors))

    if state == WOLF:
        if red_neighbors_count == 3 and green_neighbors_count <= 1:
            return 2
        elif green_neighbors_count == 2 and 0 <= red_neighbors_count <= 0:
            return 2
        elif green_neighbors_count == 1 and red_neighbors_count == 0:
            return 1
        elif red_neighbors_count == 2 and green_neighbors_count == 0:
            return 1
        else:
            return 0
    elif state == 2:
        if green_neighbors_count == 2:
            return 2
        elif green_neighbors_count == 1 and (red_neighbors_count == 2):
            return 1
        else:
            return 0
    else:
        if 1 <= green_neighbors_count <= 2 and 1 <= red_neighbors_count <= 2:
            return 1
        else:
            return 0
        


    return count%3
