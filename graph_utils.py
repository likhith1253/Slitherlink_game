"""
Graph Utilities Module
======================
This module implements standard graph traversal algorithms required for the project.
It includes BFS, DFS, and helper functions to check graph properties like
connectivity and cycles.

Time Complexity:
- BFS/DFS: O(V + E)
"""

from collections import deque

def bfs(adj_list, start_node):
    """
    Perform Breadth-First Search (BFS) starting from start_node.
    
    Args:
        adj_list (dict): Adjacency list of the graph.
        start_node (tuple): Starting vertex (r, c).
        
    Returns:
        set: Set of visited nodes.
        
    Time Complexity: O(V + E)
    """
    visited = set()
    queue = deque([start_node])
    visited.add(start_node)
    
    while queue:
        u = queue.popleft()
        for v in adj_list.get(u, []):
            if v not in visited:
                visited.add(v)
                queue.append(v)
    return visited

def dfs(adj_list, start_node, visited=None):
    """
    Perform Depth-First Search (DFS) starting from start_node.
    
    Args:
        adj_list (dict): Adjacency list.
        start_node (tuple): Starting vertex.
        visited (set): Set of already visited nodes (for recursion).
        
    Returns:
        set: Set of visited nodes.
        
    Time Complexity: O(V + E)
    """
    if visited is None:
        visited = set()
    
    visited.add(start_node)
    for v in adj_list.get(start_node, []):
        if v not in visited:
            dfs(adj_list, v, visited)
    return visited

def count_connected_components(adj_list, vertices):
    """
    Count the number of connected components in the graph.
    
    Args:
        adj_list (dict): Adjacency list.
        vertices (list): List of all vertices in the graph.
        
    Returns:
        int: Number of connected components.
        
    Time Complexity: O(V + E)
    """
    visited = set()
    count = 0
    for v in vertices:
        if v not in visited:
            # If vertex has edges (degree > 0), it's part of the loop graph we care about.
            # Isolated vertices (degree 0) are usually ignored in Slitherlink loop checks
            # unless we consider them part of the "empty" space.
            # For this game, we only care about vertices with edges.
            if v in adj_list and adj_list[v]:
                bfs_visited = bfs(adj_list, v)
                visited.update(bfs_visited)
                count += 1
    return count

def has_cycle(adj_list, vertices):
    """
    Detect if the graph contains any cycle using DFS.
    
    Args:
        adj_list (dict): Adjacency list.
        vertices (list): List of vertices.
        
    Returns:
        bool: True if cycle exists, False otherwise.
        
    Time Complexity: O(V + E)
    """
    visited = set()
    
    def dfs_cycle(u, parent):
        visited.add(u)
        for v in adj_list.get(u, []):
            if v == parent:
                continue
            if v in visited:
                return True
            if dfs_cycle(v, u):
                return True
        return False
    
    for v in vertices:
        if v not in visited and v in adj_list and adj_list[v]:
            if dfs_cycle(v, None):
                return True
    return False

def is_valid_loop_structure(adj_list, vertices):
    """
    Check if the current active edges form a single simple loop (or partial loop).
    A valid completed Slitherlink loop must:
    1. Have exactly one connected component (of edges).
    2. Every vertex in that component must have degree 2.
    
    For Phase 1 "valid move" checks, we might just want to ensure no vertex > 2.
    """
    # Check degree constraint
    for v in vertices:
        if len(adj_list.get(v, [])) > 2:
            return False, "Degree > 2 detected"
            
    return True, "OK"
