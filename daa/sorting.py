"""
DAA Unit 2: Sorting Algorithms
==============================
This module implements advanced sorting algorithms required for the project refactor.
These are used by the CPU player, Hint System, and Save/Load components.

Algorithms:
1. Merge Sort - O(N log N) - Used for Hint System
2. Quick Sort (3-way Partition) - O(N log N) - Used for CPU Move Selection
3. Heap Sort - O(N log N) - Used for Save/Load Optimization
"""

def merge_sort(items, key=lambda x: x, reverse=False):
    """
    Merge Sort implementation.
    Stable sort, good for linked lists or when random access is expensive.
    
    Args:
        items: List to sort.
        key: Function to extract comparison key.
        reverse: If True, sort descending.
        
    Time Complexity: O(N log N)
    Space Complexity: O(N)
    """
    if len(items) <= 1:
        return items
        
    mid = len(items) // 2
    left = merge_sort(items[:mid], key, reverse)
    right = merge_sort(items[mid:], key, reverse)
    
    return _merge(left, right, key, reverse)

def _merge(left, right, key, reverse):
    merged = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        val_l = key(left[i])
        val_r = key(right[j])
        
        # Stability: <= for ascending, >= for descending
        should_pick_left = val_l >= val_r if reverse else val_l <= val_r
        
        if should_pick_left:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
            
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged

def quick_sort_3way(items, key=lambda x: x, reverse=False):
    """
    Quick Sort implementation using 3-way Partitioning (Dutch National Flag).
    Efficient for arrays with many duplicate keys.
    
    Args:
        items: List to sort.
        key: Function to extract comparison key.
        reverse: If True, sort descending.
        
    Time Complexity: O(N log N) average, O(N^2) worst case
    Space Complexity: O(log N) stack space (recursive)
    """
    if len(items) <= 1:
        return items
        
    pivot = items[len(items) // 2]
    pivot_val = key(pivot)
    
    less = []
    equal = []
    greater = []
    
    for item in items:
        val = key(item)
        if val == pivot_val:
            equal.append(item)
        elif val < pivot_val:
            less.append(item)
        else:
            greater.append(item)
            
    if reverse:
        return quick_sort_3way(greater, key, reverse) + equal + quick_sort_3way(less, key, reverse)
    else:
        return quick_sort_3way(less, key, reverse) + equal + quick_sort_3way(greater, key, reverse)

def heap_sort(items, key=lambda x: x, reverse=False):
    """
    Heap Sort implementation.
    Sorts in-place (simulated here with list reconstruction for API consistency).
    
    Args:
        items: List to sort.
        key: Function to extract comparison key.
        reverse: If True, sort descending.
        
    Time Complexity: O(N log N)
    Space Complexity: O(1) auxiliary (if truly in-place), O(N) here for simplicity of returns.
    """
    n = len(items)
    # Build max heap (or min heap depending on reverse)
    # To sort Ascending: Build Max Heap, swap root to end.
    # To sort Descending: Build Min Heap, swap root to end.
    
    # Copy items to avoid modifying original list in place unexpectedly if users expect a new list return
    # (Though standard python sort is in-place, our functions return the list)
    arr = items[:] 
    
    # Build heap (rearrange array)
    for i in range(n // 2 - 1, -1, -1):
        _heapify(arr, n, i, key, reverse)
        
    # One by one extract an element from heap
    for i in range(n - 1, 0, -1):
        # Move current root to end
        arr[i], arr[0] = arr[0], arr[i]
        
        # call max heapify on the reduced heap
        _heapify(arr, i, 0, key, reverse)
        
    return arr

def _heapify(arr, n, i, key, reverse):
    """
    Heapify subtree rooted at index i.
    n is size of heap.
    """
    largest = i  # Initialize largest as root
    l = 2 * i + 1     # left = 2*i + 1
    r = 2 * i + 2     # right = 2*i + 2
    
    # The logic below builds a Max Heap if we want Ascending sort (reverse=False)
    # Because in Heap Sort, we pop the max to the end to build the sorted array from back to front.
    # So:
    # If reverse=False (Ascending): End array should be large elements. We pop Max. So Max Heap.
    # If reverse=True (Descending): End array should be small elements. We pop Min. So Min Heap.
    
    root_val = key(arr[largest])
    
    if l < n:
        l_val = key(arr[l])
        
        compare = l_val > root_val if not reverse else l_val < root_val
        if compare:
            largest = l
            root_val = l_val # Update root_val for next comparison
            
    if r < n:
        r_val = key(arr[r])
        # Compare with the NEW largest
        largest_val = key(arr[largest])
        
        compare = r_val > largest_val if not reverse else r_val < largest_val
        if compare:
            largest = r
            
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]  # swap
        
        # Heapify the root.
        _heapify(arr, n, largest, key, reverse)
