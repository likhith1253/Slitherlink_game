"""
Game Validators
===============
Functions to validate moves and check game state conditions.
Uses DAA graph algorithms for connectivity and cycle checks.
"""

from daa.graph_algos import count_connected_components, has_cycle

def is_valid_move(graph, u, v, clues, check_global=False):
    """
    Check if toggling edge u-v is valid.
    Returns: (bool, reason)
    """
    edge = tuple(sorted((u, v)))
    adding = edge not in graph.edges
    
    if adding:
        # Degree Constraint: No vertex > 2
        if graph.get_degree(u) >= 2 or graph.get_degree(v) >= 2:
            return False, "Degree > 2"
            
        # Clue Constraint
        if not check_clue_constraint(graph, u, v, clues, adding=True):
            return False, "Clue Violated"
            
    return True, "OK"

def check_clue_constraint(graph, u, v, clues, adding):
    """
    Check if adding/removing edge u-v violates any adjacent clues.
    """
    r1, c1 = u
    r2, c2 = v
    cells_to_check = []
    
    # Identify adjacent cells
    if r1 == r2: # Horizontal
        c_min = min(c1, c2)
        if r1 > 0: cells_to_check.append((r1-1, c_min))
        if r1 < graph.rows: cells_to_check.append((r1, c_min))
    else: # Vertical
        r_min = min(r1, r2)
        if c1 > 0: cells_to_check.append((r_min, c1-1))
        if c1 < graph.cols: cells_to_check.append((r_min, c1))
        
    for cell in cells_to_check:
        if cell in clues:
            current_edges = count_edges_around_cell(graph, cell)
            # If we are adding, we haven't added it to graph yet, so +1
            # If we are removing, we haven't removed it yet, so -1 (but usually removing is safe unless strict mode)
            
            potential_edges = current_edges + (1 if adding else -1)
            
            if potential_edges > clues[cell]:
                return False
    return True

def count_edges_around_cell(graph, cell):
    r, c = cell
    edges = [
        tuple(sorted(((r, c), (r, c+1)))),
        tuple(sorted(((r+1, c), (r+1, c+1)))),
        tuple(sorted(((r, c), (r+1, c)))),
        tuple(sorted(((r, c+1), (r+1, c+1))))
    ]
    count = 0
    for e in edges:
        if e in graph.edges:
            count += 1
    return count

def check_win_condition(graph, clues):
    """
    Check if the game is won.
    Conditions:
    1. All clues satisfied.
    2. Single connected loop (1 component, all degrees=2).
    """
    # 1. Clues
    for cell, val in clues.items():
        if count_edges_around_cell(graph, cell) != val:
            return False, "Clues not satisfied"
            
    # 2. Loop Structure
    active_vertices = [v for v in graph.vertices if graph.get_degree(v) > 0]
    if not active_vertices:
        return False, "Empty board"
        
    for v in active_vertices:
        if graph.get_degree(v) != 2:
            return False, "Not a closed loop"
            
    # 3. Connectivity
    num_components = count_connected_components(graph.adj_list, graph.vertices)
    if num_components != 1:
        return False, "Multiple loops detected"
        
    return True, "Winner"
