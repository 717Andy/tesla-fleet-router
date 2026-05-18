import heapq

def manhattan_distance(p1, p2):
    """Heuristic calculation: h(n) estimation to the destination"""
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def get_neighbors(node, grid_size=5):
    """Returns valid adjacent orthogonal movements on our map layout"""
    x, y = node
    neighbors = []
    moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Right, Left, Down, Up
    
    for dx, dy in moves:
        nx, ny = x + dx, y + dy
        if 0 <= nx < grid_size and 0 <= ny < grid_size:
            # Enforce hard structural walls to create a narrow routing bottleneck
            # Wall blocks column 2 entirely, except rows 1 (bypass) and 2 (supercharger)
            if nx == 2 and ny not in [1, 2]:
                continue  
            neighbors.append((nx, ny))
    return neighbors

def run_fleet_router(start, goal, charger_multiplier):
    """
    Executes the A* pathfinding algorithm across the coordinate system.
    Dynamically weighs the Supercharger node based on the rule engine's output multiplier.
    """
    # Priority Queue stores tuples of: (f_score, current_node)
    open_set = []
    heapq.heappush(open_set, (0, start))
    
    # Tracks the optimal path trajectory mapping back to start
    came_from = {}
    
    # g_score[node] is the exact cost incurred to get from start to that node
    g_score = {start: 0}
    
    while open_set:
        current_f, current = heapq.heappop(open_set)
        
        if current == goal:
            # Reconstruct and return the finalized optimal path
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]
            
        for neighbor in get_neighbors(current):
            # Base movement cost to traverse any standard road tile
            step_cost = 1.0
            
            # If the vehicle evaluates moving onto the Supercharger station node (2, 2)
            if neighbor == (2, 2):
                step_cost = 1.0 * charger_multiplier
                
            tentative_g_score = g_score[current] + step_cost
            
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                # f(n) = g(n) + h(n)
                f_score = tentative_g_score + manhattan_distance(neighbor, goal)
                heapq.heappush(open_set, (f_score, neighbor))
                
    return None  # Returns None if path is entirely blocked