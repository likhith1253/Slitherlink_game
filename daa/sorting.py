"""
DAA Unit 2: Sorting Algorithms
==============================
This module implements standard sorting algorithms required by the syllabus.
These are used by the CPU player to sort candidate moves based on greedy scores.

Algorithms:
1. Bubble Sort - O(N^2)
2. Insertion Sort - O(N^2)
3. Selection Sort - O(N^2)
"""

def bubble_sort(items, key=lambda x: x, reverse=False):
    """
    Bubble Sort implementation.
    Args:
        items: List to sort.
        key: Function to extract comparison key.
        reverse: If True, sort descending.
    Time Complexity: O(N^2)
    """
    n = len(items)
    for i in range(n):
        swapped = False
        for j in range(0, n-i-1):
            val_a = key(items[j])
            val_b = key(items[j+1])
            
            should_swap = val_a < val_b if reverse else val_a > val_b
            
            if should_swap:
                items[j], items[j+1] = items[j+1], items[j]
                swapped = True
        if not swapped:
            break
    return items

def insertion_sort(items, key=lambda x: x, reverse=False):
    """
    Insertion Sort implementation.
    Time Complexity: O(N^2)
    """
    for i in range(1, len(items)):
        key_item = items[i]
        key_val = key(key_item)
        j = i - 1
        
        while j >= 0:
            curr_val = key(items[j])
            should_move = curr_val < key_val if reverse else curr_val > key_val
            
            if should_move:
                items[j + 1] = items[j]
                j -= 1
            else:
                break
        items[j + 1] = key_item
    return items

def selection_sort(items, key=lambda x: x, reverse=False):
    """
    Selection Sort implementation.
    Time Complexity: O(N^2)
    """
    n = len(items)
    for i in range(n):
        extreme_idx = i
        extreme_val = key(items[i])
        
        for j in range(i+1, n):
            curr_val = key(items[j])
            should_update = curr_val > extreme_val if reverse else curr_val < extreme_val
            
            if should_update:
                extreme_idx = j
                extreme_val = curr_val
                
        items[i], items[extreme_idx] = items[extreme_idx], items[i]
    return items
