"""
Game State Manager
==================
Central controller for the game.
Manages:
- Graph state
- Undo/Redo stack
- Player turns
- Difficulty settings
- Interaction with CPU and Validators
"""

import random
from logic.graph import Graph
from logic.validators import is_valid_move, check_win_condition
from logic.greedy_cpu import GreedyCPU
from logic.statistics import StatisticsManager

class GameState:
    def __init__(self, rows=5, cols=5, difficulty="Medium"):
        self.rows = rows
        self.cols = cols
        self.difficulty = difficulty
        
        self.graph = Graph(rows, cols)
        self.clues = {}
        self.cpu = GreedyCPU(self)
        self.stats_mgr = StatisticsManager()
        
        self.turn = "Player 1 (Human)"
        self.game_over = False
        self.winner = None
        self.message = "Game Start!"
        
        # Undo/Redo Stacks
        self.undo_stack = []
        self.redo_stack = []
        
        self.solution_edges = set()
        self._generate_clues()

    def _generate_clues(self):
        """
        Generate a solvable board by creating a random loop first,
        then deriving clues from it.
        """
        # 1. Generate a random connected region of cells
        # The boundary of this region will be our valid loop.
        region = set()
        start_cell = (random.randint(0, self.rows-1), random.randint(0, self.cols-1))
        region.add(start_cell)
        
        # Target size: 40% to 70% of the board
        target_size = int(self.rows * self.cols * random.uniform(0.4, 0.7))
        
        # Grow region using random BFS/DFS
        candidates = [start_cell]
        while len(region) < target_size and candidates:
            curr = random.choice(candidates) # Random pick = irregular shape
            
            # Get neighbors
            r, c = curr
            neighbors = []
            if r > 0: neighbors.append((r-1, c))
            if r < self.rows - 1: neighbors.append((r+1, c))
            if c > 0: neighbors.append((r, c-1))
            if c < self.cols - 1: neighbors.append((r, c+1))
            
            # Filter unvisited
            unvisited = [n for n in neighbors if n not in region]
            
            if unvisited:
                next_cell = random.choice(unvisited)
                region.add(next_cell)
                candidates.append(next_cell)
            else:
                candidates.remove(curr)
                
        # 2. Calculate boundary edges of this region
        # An edge is a boundary if exactly one of its cells is in the region
        solution_edges = set()
        
        # Horizontal edges
        for r in range(self.rows + 1):
            for c in range(self.cols):
                # Cells above and below this edge
                cell_above = (r-1, c) if r > 0 else None
                cell_below = (r, c) if r < self.rows else None
                
                in_above = cell_above in region
                in_below = cell_below in region
                
                if in_above != in_below: # XOR: Boundary
                    solution_edges.add(tuple(sorted(((r, c), (r, c+1)))))
                    
        # Vertical edges
        for r in range(self.rows):
            for c in range(self.cols + 1):
                # Cells left and right
                cell_left = (r, c-1) if c > 0 else None
                cell_right = (r, c) if c < self.cols else None
                
                in_left = cell_left in region
                in_right = cell_right in region
                
                if in_left != in_right:
                    solution_edges.add(tuple(sorted(((r, c), (r+1, c)))))
                    
        # 3. Generate Clues based on these solution edges
        # For every cell, count how many solution edges surround it
        temp_clues = {}
        for r in range(self.rows):
            for c in range(self.cols):
                # Count edges
                count = 0
                # Top
                if tuple(sorted(((r, c), (r, c+1)))) in solution_edges: count += 1
                # Bottom
                if tuple(sorted(((r+1, c), (r+1, c+1)))) in solution_edges: count += 1
                # Left
                if tuple(sorted(((r, c), (r+1, c)))) in solution_edges: count += 1
                # Right
                if tuple(sorted(((r, c+1), (r+1, c+1)))) in solution_edges: count += 1
                
                temp_clues[(r, c)] = count
                
        # 4. Filter clues based on difficulty
        # Easy: Show most clues (80%)
        # Medium: Show 60%
        # Hard: Show 40%
        keep_prob = 0.6
        if self.difficulty == "Easy": keep_prob = 0.8
        elif self.difficulty == "Hard": keep_prob = 0.4
        
        self.clues = {}
        for cell, val in temp_clues.items():
            if random.random() < keep_prob:
                self.clues[cell] = val
                
        # Store the solution for the AI/Hint system
        self.solution_edges = solution_edges

    def make_move(self, u, v, is_cpu=False):
        if self.game_over: return False
        
        edge = tuple(sorted((u, v)))
        if edge in self.graph.edges:
            # Removing edge
            self.graph.remove_edge(u, v)
            action = "remove"
            self.message = "Edge Removed"
        else:
            # Adding edge
            valid, reason = is_valid_move(self.graph, u, v, self.clues)
            if not valid:
                self.message = f"Invalid: {reason}"
                return False
            self.graph.add_edge(u, v)
            action = "add"
            self.message = "Edge Added"
            
        # Record for Undo (Clear redo stack on new move)
        self.undo_stack.append((u, v, action))
        self.redo_stack.clear()
        
        self._check_game_status()
        
        if not self.game_over:
            self.switch_turn()
            
        return True

    def undo(self):
        if not self.undo_stack: return False
        
        u, v, action = self.undo_stack.pop()
        
        # Reverse action
        if action == "add":
            self.graph.remove_edge(u, v)
        else:
            self.graph.add_edge(u, v)
            
        self.redo_stack.append((u, v, action))
        self.switch_turn() # Undo reverses turn too
        self.message = "Undo Successful"
        return True

    def redo(self):
        if not self.redo_stack: return False
        
        u, v, action = self.redo_stack.pop()
        
        # Re-apply action
        if action == "add":
            self.graph.add_edge(u, v)
        else:
            self.graph.remove_edge(u, v)
            
        self.undo_stack.append((u, v, action))
        self.switch_turn()
        self.message = "Redo Successful"
        return True

    def switch_turn(self):
        if self.turn == "Player 1 (Human)":
            self.turn = "Player 2 (CPU)"
        else:
            self.turn = "Player 1 (Human)"

    def _check_game_status(self):
        won, reason = check_win_condition(self.graph, self.clues)
        if won:
            self.game_over = True
            self.winner = self.turn
            self.message = f"GAME OVER! {self.winner} Wins!"
            self.stats_mgr.record_game(self.winner)
            return

        # Check for Stalemate (No valid moves left for the NEXT player)
        # Note: We just switched turns in make_move, but we call this before switching?
        # Actually, make_move calls _check_game_status BEFORE switching turns.
        # So we should check if the CURRENT player (who just moved) has left the board in a state
        # where the NEXT player has no moves.
        
        # However, let's just check if ANY valid moves exist.
        # If no valid moves exist for ANYONE (since edges are shared), it's a stalemate.
        # But wait, is_valid_move doesn't depend on whose turn it is.
        
        if not self.cpu.get_all_valid_moves():
            self.game_over = True
            self.winner = "Stalemate"
            self.message = "GAME OVER! No valid moves left. Stalemate."
            # Record as a draw or loss? Let's just not record it as a win.


    def get_hint(self):
        """
        Return a suggested move (u, v) and a reason.
        Uses CPU logic but explicitly looks for 'good' moves.
        """
        move = self.cpu.make_move()
        if move:
            # Generate a simple reason based on score
            score = self.cpu.calculate_score(move)
            if score >= 10:
                reason = "Completes a clue!"
            elif score >= 3:
                reason = "Extends the path safely."
            else:
                reason = "A valid move to consider."
            return move, reason
        return None, "No obvious moves."
