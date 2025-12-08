"""
Algorithms Module
=================
This module implements:
1. Sorting algorithms (Bubble, Insertion, Selection) as per Unit 2 requirements.
2. Greedy strategy helper for the CPU player.

Time Complexity:
- Sorting: O(N^2)
- Greedy Choice: O(M) where M is number of moves.
"""

# --- Sorting Algorithms ---

def bubble_sort(items, key=lambda x: x):
    """
    Bubble Sort implementation.
    Time Complexity: O(N^2)
    """
    n = len(items)
    for i in range(n):
        for j in range(0, n-i-1):
            if key(items[j]) < key(items[j+1]): # Descending order for greedy score
                items[j], items[j+1] = items[j+1], items[j]
    return items

def insertion_sort(items, key=lambda x: x):
    """
    Insertion Sort implementation.
    Time Complexity: O(N^2)
    """
    for i in range(1, len(items)):
        key_item = items[i]
        j = i - 1
        while j >= 0 and key(items[j]) < key(key_item): # Descending
            items[j + 1] = items[j]
            j -= 1
        items[j + 1] = key_item
    return items

def selection_sort(items, key=lambda x: x):
    """
    Selection Sort implementation.
    Time Complexity: O(N^2)
    """
    for i in range(len(items)):
        max_idx = i
        for j in range(i+1, len(items)):
            if key(items[j]) > key(items[max_idx]): # Descending
                max_idx = j
        items[i], items[max_idx] = items[max_idx], items[i]
    return items

# --- Greedy Strategy ---

def evaluate_move(game_state, move):
    """
    Calculate a greedy score for a potential move.
    
    Args:
        game_state: Current state object.
        move: Tuple ((r1, c1), (r2, c2)) representing the edge.
        
    Returns:
        int: Score (higher is better).
    """
    score = 0
    
    # Simulate move
    # Note: This requires game_state to have methods to peek at effects
    # For now, we'll assume we can check neighbors and clues.
    
    # 1. Reward completing a clue
    # 2. Penalize violating a clue (though valid_moves should filter this)
    # 3. Reward extending a path
    
    # Placeholder logic - will be refined when integrated with GameState
    return score
