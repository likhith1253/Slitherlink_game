"""
Greedy Algorithms Implementation
================================
Detailed implementations of standard greedy algorithms.
Includes:
1. Fractional Knapsack Problem
2. Dijkstra's Shortest Path Algorithm
3. Prim's Minimum Spanning Tree Algorithm
4. Huffman Coding

Each algorithm is implemented with detailed comments explaining the greedy choice property.
"""

import heapq
from collections import defaultdict

# -----------------------------------------------------------------------------
# 1. Fractional Knapsack Problem
# -----------------------------------------------------------------------------
def fractional_knapsack(capacity, weights, values):
    """
    Solves the Fractional Knapsack problem using a Greedy approach.
    
    Greedy Choice: Pick the item with the highest value-to-weight ratio.
    
    Args:
        capacity (float): Maximum weight the knapsack can hold.
        weights (list): List of weights of items.
        values (list): List of values of items.
        
    Returns:
        float: Maximum total value.
        list: List of chosen item indices (including partials).
    """
    n = len(weights)
    # Calculate value-to-weight ratio for each item
    items = []
    for i in range(n):
        ratio = values[i] / weights[i]
        items.append({'index': i, 'ratio': ratio, 'weight': weights[i], 'value': values[i]})
        
    # Sort items by ratio in descending order (Greedy Step)
    items.sort(key=lambda x: x['ratio'], reverse=True)
    
    total_value = 0.0
    current_weight = 0.0
    selected_indices = []
    
    for item in items:
        if current_weight + item['weight'] <= capacity:
            # Take the whole item
            current_weight += item['weight']
            total_value += item['value']
            selected_indices.append(item['index'])
        else:
            # Take fraction of the item
            remaining_capacity = capacity - current_weight
            fraction = remaining_capacity / item['weight']
            total_value += item['value'] * fraction
            current_weight += remaining_capacity
            selected_indices.append(item['index'])
            break # Knapsack is full
            
    return total_value, selected_indices

# -----------------------------------------------------------------------------
# 2. Dijkstra's Shortest Path Algorithm
# -----------------------------------------------------------------------------
def dijkstra(graph, start_node):
    """
    Finds the shortest paths from a start node to all other nodes in a weighted graph.
    
    Greedy Choice: Always expand the unvisited node with the smallest known distance.
    
    Args:
        graph (dict): Adjacency list where graph[u] = [(v, weight), ...].
        start_node: The starting node.
        
    Returns:
        dict: Shortest distances to each node.
        dict: Predecessors map for path reconstruction.
    """
    # Initialize distances to infinity
    distances = {node: float('infinity') for node in graph}
    distances[start_node] = 0
    predecessors = {node: None for node in graph}
    
    # Priority queue to store (distance, node), ordered by distance
    pq = [(0, start_node)]
    
    while pq:
        current_dist, current_node = heapq.heappop(pq)
        
        # If we found a shorter path to this node already, skip
        if current_dist > distances[current_node]:
            continue
            
        # Explore neighbors
        if current_node in graph:
            for neighbor, weight in graph[current_node]:
                distance = current_dist + weight
                
                # Relaxation step
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    predecessors[neighbor] = current_node
                    heapq.heappush(pq, (distance, neighbor))
                
    return distances, predecessors

# -----------------------------------------------------------------------------
# 3. Prim's Minimum Spanning Tree Algorithm
# -----------------------------------------------------------------------------
def prim_mst(graph, start_node, max_nodes=None):
    """
    Finds the Minimum Spanning Tree (MST) of a connected, undirected graph.
    
    Greedy Choice: Grow the MST by adding the cheapest edge connecting the tree to a non-tree vertex.
    
    Args:
        graph (dict): Adjacency list where graph[u] = [(v, weight), ...].
        start_node: Arbitrary starting node.
        max_nodes (int, optional): Stop after visiting this many nodes.
        
    Returns:
        list: List of edges (u, v, weight) in the MST.
        float: Total weight of the MST.
    """
    mst_edges = []
    total_weight = 0
    visited = set([start_node])
    
    # Priority queue: (weight, from_node, to_node)
    edges_pq = []
    if start_node in graph:
        for neighbor, weight in graph[start_node]:
            heapq.heappush(edges_pq, (weight, start_node, neighbor))
        
    while edges_pq:
        if max_nodes and len(visited) >= max_nodes:
            break
            
        weight, u, v = heapq.heappop(edges_pq)
        
        if v in visited:
            continue
            
        # Add edge to MST
        visited.add(v)
        mst_edges.append((u, v, weight))
        total_weight += weight
        
        # Add new edges from v to the queue
        if v in graph:
            for next_node, next_weight in graph[v]:
                if next_node not in visited:
                    heapq.heappush(edges_pq, (next_weight, v, next_node))
                
    return mst_edges, total_weight, visited



# -----------------------------------------------------------------------------
# 5. Huffman Coding
# -----------------------------------------------------------------------------
class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None
        
    def __lt__(self, other):
        return self.freq < other.freq

def huffman_coding(char_freqs):
    """
    Builds the Huffman Tree for optimal prefix coding.
    
    Greedy Choice: Repeatedly combine the two symbols with the lowest frequency.
    
    Args:
        char_freqs (dict): Dictionary mapping characters to frequencies.
        
    Returns:
        dict: Mapping of characters to their Huffman codes.
    """
    heap = [HuffmanNode(char, freq) for char, freq in char_freqs.items()]
    heapq.heapify(heap)
    
    while len(heap) > 1:
        # Extract two nodes with lowest frequency
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        
        # Create new internal node
        merged = HuffmanNode(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        
        heapq.heappush(heap, merged)
        
    root = heap[0]
    codes = {}
    
    def generate_codes(node, current_code):
        if node is None:
            return
        if node.char is not None:
            codes[node.char] = current_code
            return
        generate_codes(node.left, current_code + "0")
        generate_codes(node.right, current_code + "1")
        
    generate_codes(root, "")
    return codes

# -----------------------------------------------------------------------------
# 6. Job Sequencing with Deadlines
# -----------------------------------------------------------------------------
def job_sequencing_with_deadlines(jobs):
    """
    Solves the Job Sequencing with Deadlines problem using a Greedy approach.
    
    Greedy Choice: Always select the available job with the highest profit.
    
    Args:
        jobs (list): List of dicts, each with keys 'id', 'deadline', 'profit'.
                     Example: [{'id': 1, 'deadline': 2, 'profit': 100}, ...]
        
    Returns:
        list: Sequence of job IDs maximizing total profit.
        int: Total profit.
    """
    # 1. Sort all jobs in descending order of profit (Greedy Step)
    jobs.sort(key=lambda x: x['profit'], reverse=True)
    
    # 2. Find maximum deadline to determine total time slots available
    max_deadline = 0
    for job in jobs:
        if job['deadline'] > max_deadline:
            max_deadline = job['deadline']
            
    # Time slots: index i represents time slot [i, i+1]
    # Initialize slots as -1 (empty)
    # We use size max_deadline because deadlines are 1-based usually
    # e.g., deadline 2 means can be done in [0,1] or [1,2].
    result = [-1] * max_deadline
    slot_filled = [False] * max_deadline
    
    total_profit = 0
    job_sequence = []
    
    # 3. Iterate through sorted jobs
    for job in jobs:
        # Find a free time slot for this job (starting from its deadline - 1 down to 0)
        # Because deadline is the *latest* it can finish.
        # e.g. deadline 2 needs slot 0 or 1. We prefer 1 to save 0 for stricter deadlines.
        for j in range(min(max_deadline, job['deadline']) - 1, -1, -1):
            if not slot_filled[j]:
                result[j] = job['id']
                slot_filled[j] = True
                total_profit += job['profit']
                break
                
    # Filter empty slots and return results
    final_sequence = [job_id for job_id in result if job_id != -1]
    return final_sequence, total_profit
