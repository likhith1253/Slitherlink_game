"""
Game Logic Module
=================
This module handles the core state of the Loopy game.
It manages the grid, graph representation, clues, and player turns.

Time Complexity:
- Move Validation: O(1) local checks + O(V+E) for global loop checks.
- CPU Move: O(M * K) where M is moves.
"""

import random
from graph_utils import is_valid_loop_structure, count_connected_components, has_cycle
from algorithms import bubble_sort, evaluate_move

class Graph:
    """
    Represents the game board as a graph.
    Vertices are grid points (r, c).
    Edges are lines drawn between points.
    """
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.vertices = []
        self.adj_list = {}
        self.edges = set() # Stores tuples of ((r1, c1), (r2, c2))
        
        # Initialize vertices
        for r in range(rows + 1):
            for c in range(cols + 1):
                v = (r, c)
                self.vertices.append(v)
                self.adj_list[v] = []

    def add_edge(self, u, v):
        """Add an edge between u and v."""
        # Ensure consistent ordering for set storage
        edge = tuple(sorted((u, v)))
        if edge not in self.edges:
            self.edges.add(edge)
            self.adj_list[u].append(v)
            self.adj_list[v].append(u)
            return True
        return False

    def remove_edge(self, u, v):
        """Remove an edge between u and v."""
        edge = tuple(sorted((u, v)))
        if edge in self.edges:
            self.edges.remove(edge)
            if v in self.adj_list[u]: self.adj_list[u].remove(v)
            if u in self.adj_list[v]: self.adj_list[v].remove(u)
            return True
        return False

    def get_degree(self, v):
        return len(self.adj_list.get(v, []))

class GameState:
    """
    Manages the overall game state.
    """
    def __init__(self, rows=4, cols=4):
        self.rows = rows
        self.cols = cols
        self.graph = Graph(rows, cols)
        self.clues = {} # (r, c) -> number (0-3)
        self.turn = "Player 1 (Human)"
        self.game_over = False
        self.winner = None
        self.message = "Game Start! Player 1's Turn."
        
        # Generate random clues
        self._generate_clues()

    def _generate_clues(self):
        """Randomly place clues on the board."""
        # Density of clues
        for r in range(self.rows):
            for c in range(self.cols):
                if random.random() < 0.4: # 40% chance of a clue
                    self.clues[(r, c)] = random.randint(0, 3)

    def is_valid_move(self, u, v, check_global=False):
        """
        Check if toggling edge u-v is valid.
        
        Args:
            u, v: Vertices
            check_global: If True, checks for premature loops (not strictly required for move validity in all variants, 
                          but good for strict play). For Phase 1, we mainly check local degree constraints.
        """
        # If edge exists, we are removing it -> always valid locally (unless we enforce "cannot break loop")
        # If edge doesn't exist, we are adding it -> check degrees
        
        edge = tuple(sorted((u, v)))
        adding = edge not in self.graph.edges
        
        if adding:
            if self.graph.get_degree(u) >= 2 or self.graph.get_degree(v) >= 2:
                return False, "Vertex degree would exceed 2."
        
        # Check Clues (Immediate fail if we exceed clue number)
        # We need to find which cells share this edge.
        # Edge is either horizontal or vertical.
        r1, c1 = u
        r2, c2 = v
        
        cells_to_check = []
        if r1 == r2: # Horizontal
            # Edge is between (r1, c1) and (r1, c2). Assumes |c1-c2|=1
            c_min = min(c1, c2)
            # Cell above: (r1-1, c_min), Cell below: (r1, c_min)
            if r1 > 0: cells_to_check.append((r1-1, c_min))
            if r1 < self.rows: cells_to_check.append((r1, c_min))
        else: # Vertical
            r_min = min(r1, r2)
            # Cell left: (r_min, c1-1), Cell right: (r_min, c1)
            if c1 > 0: cells_to_check.append((r_min, c1-1))
            if c1 < self.cols: cells_to_check.append((r_min, c1))
            
        if adding:
            for cell in cells_to_check:
                if cell in self.clues:
                    current_edges = self._count_edges_around_cell(cell)
                    if current_edges >= self.clues[cell]:
                        return False, f"Clue at {cell} would be violated."
        
        return True, "OK"

    def _count_edges_around_cell(self, cell):
        r, c = cell
        # 4 edges around (r,c):
        # Top: (r,c)-(r,c+1)
        # Bottom: (r+1,c)-(r+1,c+1)
        # Left: (r,c)-(r+1,c)
        # Right: (r,c+1)-(r+1,c+1)
        edges = [
            tuple(sorted(((r, c), (r, c+1)))),
            tuple(sorted(((r+1, c), (r+1, c+1)))),
            tuple(sorted(((r, c), (r+1, c)))),
            tuple(sorted(((r, c+1), (r+1, c+1))))
        ]
        count = 0
        for e in edges:
            if e in self.graph.edges:
                count += 1
        return count

    def make_move(self, u, v):
        """Execute a move (toggle edge). Returns success bool."""
        if self.game_over:
            return False

        edge = tuple(sorted((u, v)))
        if edge in self.graph.edges:
            self.graph.remove_edge(u, v)
            action = "Removed"
        else:
            valid, reason = self.is_valid_move(u, v)
            if not valid:
                self.message = f"Invalid Move: {reason}"
                return False
            self.graph.add_edge(u, v)
            action = "Added"
            
        self.message = f"{action} edge {u}-{v}."
        self.check_win_condition()
        
        if not self.game_over:
            self.switch_turn()
            
        return True

    def switch_turn(self):
        if self.turn == "Player 1 (Human)":
            self.turn = "Player 2 (CPU)"
            # In GUI, we will trigger CPU move
        else:
            self.turn = "Player 1 (Human)"

    def check_win_condition(self):
        # 1. Check if all clues are satisfied
        all_clues_ok = True
        for cell, val in self.clues.items():
            if self._count_edges_around_cell(cell) != val:
                all_clues_ok = False
                break
        
        if not all_clues_ok:
            return

        # 2. Check if it's a single simple loop
        # - All vertices with degree > 0 must have degree 2 (already enforced by is_valid_move mostly, but check again)
        # - Must be 1 connected component
        
        # Filter vertices that are part of the graph (degree > 0)
        active_vertices = [v for v in self.graph.vertices if self.graph.get_degree(v) > 0]
        
        if not active_vertices:
            return # Empty board

        for v in active_vertices:
            if self.graph.get_degree(v) != 2:
                return # Not a loop yet
        
        # Check connected components
        num_components = count_connected_components(self.graph.adj_list, self.graph.vertices)
        
        if num_components == 1:
            self.game_over = True
            self.winner = self.turn
            self.message = f"GAME OVER! {self.winner} Wins!"

    def cpu_move(self):
        """Greedy CPU implementation."""
        possible_moves = []
        
        # Identify all potential edges (horizontal and vertical)
        # Horizontal
        for r in range(self.rows + 1):
            for c in range(self.cols):
                u, v = (r, c), (r, c+1)
                if tuple(sorted((u, v))) not in self.graph.edges:
                    valid, _ = self.is_valid_move(u, v)
                    if valid:
                        possible_moves.append((u, v))
                        
        # Vertical
        for r in range(self.rows):
            for c in range(self.cols + 1):
                u, v = (r, c), (r+1, c)
                if tuple(sorted((u, v))) not in self.graph.edges:
                    valid, _ = self.is_valid_move(u, v)
                    if valid:
                        possible_moves.append((u, v))
        
        if not possible_moves:
            self.message = "CPU has no moves! Stalemate."
            self.game_over = True
            return

        # Score moves
        scored_moves = []
        for move in possible_moves:
            score = self._calculate_greedy_score(move)
            scored_moves.append((move, score))
            
        # Sort using one of our sorting algos
        # We want descending score
        sorted_moves = bubble_sort(scored_moves, key=lambda x: x[1])
        sorted_moves.reverse() # Bubble sort was ascending in algorithms.py? Let's check. 
        # algorithms.py bubble_sort: if key(items[j]) < key(items[j+1]): swap. 
        # This pushes larger elements to the end (Ascending). 
        # So last element is max.
        
        best_move = sorted_moves[-1][0]
        self.make_move(best_move[0], best_move[1])

    def _calculate_greedy_score(self, move):
        u, v = move
        score = 0
        
        # 1. Does it complete a clue?
        # Temporarily add edge
        self.graph.add_edge(u, v)
        
        # Check adjacent cells
        r1, c1 = u
        r2, c2 = v
        cells_to_check = []
        if r1 == r2: # Horizontal
            c_min = min(c1, c2)
            if r1 > 0: cells_to_check.append((r1-1, c_min))
            if r1 < self.rows: cells_to_check.append((r1, c_min))
        else: # Vertical
            r_min = min(r1, r2)
            if c1 > 0: cells_to_check.append((r_min, c1-1))
            if c1 < self.cols: cells_to_check.append((r_min, c1))
            
        for cell in cells_to_check:
            if cell in self.clues:
                current = self._count_edges_around_cell(cell)
                target = self.clues[cell]
                if current == target:
                    score += 10 # Big reward for satisfying a clue
                elif current > target:
                    score -= 50 # Penalty (shouldn't happen due to is_valid_move)
                else:
                    score += 1 # Small reward for adding to a clue
                    
        # 2. Does it extend a line? (Degree becomes 2)
        if self.graph.get_degree(u) == 2: score += 2
        if self.graph.get_degree(v) == 2: score += 2
        
        # Remove edge
        self.graph.remove_edge(u, v)
        
        return score
