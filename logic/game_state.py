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
    def __init__(self, rows=5, cols=5, difficulty="Medium", game_mode="vs_cpu"):
        self.rows = rows
        self.cols = cols
        self.difficulty = difficulty
        self.game_mode = game_mode  # "vs_cpu", "two_player", "greedy_challenge"
        self.teacher_mode = False # DAA Feature: Teacher Mode
        
        self.graph = Graph(rows, cols)
        self.clues = {}
        # CPU is active in vs_cpu AND expert mode (Duel)
        self.cpu = GreedyCPU(self) if game_mode in ["vs_cpu", "expert"] else None
        self.stats_mgr = StatisticsManager()
        
        # Greedy Mode Mechanics
        self.edge_weights = {}
        self.energy = 100 
        self.max_energy = 100
        self.energy_cpu = 100
        self.max_energy_cpu = 100
        
        self._assign_weights()

        if game_mode == "expert":
            self.turn = "Player 1 (Human)" # Expert is now PvE
            self._generate_clues() # This sets self.energy based on solution
            # Give CPU same starting energy as player for fairness
            self.energy_cpu = self.energy
            self.max_energy_cpu = self.energy
        elif game_mode == "vs_cpu":
            self.turn = "Player 1 (Human)"
            self._generate_clues()
        else:
            self.turn = "Player 1"
            self._generate_clues()
        
        self.game_over = False
        self.winner = None
        self.message = "Game Start!"
        
        self.undo_stack = []
        self.redo_stack = []
        
        # self.solution_edges = set() # Set in _generate_clues

    def _assign_weights(self):
        # Assign random weights to all potential edges
        for r in range(self.rows + 1):
            for c in range(self.cols):
                u, v = (r, c), (r, c+1)
                self.edge_weights[tuple(sorted((u, v)))] = random.randint(1, 9)
                
        for r in range(self.rows):
            for c in range(self.cols + 1):
                u, v = (r, c), (r+1, c)
                self.edge_weights[tuple(sorted((u, v)))] = random.randint(1, 9)

    def _calculate_required_energy(self):
        return 100 # Placeholder

    def make_move(self, u, v, is_cpu=False):
        if self.game_over: return False
        
        # Validate Turn
        if self.game_mode in ["vs_cpu", "expert"]:
            if self.turn == "Player 2 (CPU)" and not is_cpu:
                return False # Human trying to move on CPU turn
            if self.turn == "Player 1 (Human)" and is_cpu:
                return False # CPU trying to move on Human turn
        
        edge = tuple(sorted((u, v)))
        cost = self.edge_weights.get(edge, 0)
        
        if edge in self.graph.edges:
            # Removing edge
            self.graph.remove_edge(u, v)
            action = "remove"
            self.message = "Edge Removed"
            
            # Refund energy in Expert mode
            if self.game_mode == "expert":
                if is_cpu:
                    self.energy_cpu += cost
                else:
                    self.energy += cost
        else:
            # Adding edge
            if self.game_mode == "expert":
                if not is_cpu:
                    # Human Energy Check
                    if self.energy < cost:
                        self.message = "Not enough Energy! You LOSE!"
                        self.game_over = True
                        self.winner = "Player 2 (CPU)"
                        return False
                else:
                    # CPU Energy Check
                    if self.energy_cpu < cost:
                        self.message = "CPU Out of Energy! You WIN!"
                        self.game_over = True
                        self.winner = "Player 1 (Human)"
                        return False
                    
            valid, reason = is_valid_move(self.graph, u, v, self.clues)
            if not valid:
                self.message = f"Invalid: {reason}"
                return False
            self.graph.add_edge(u, v)
            action = "add"
            
            if self.game_mode == "expert":
                self.message = f"Edge Added (Cost: {cost})"
                if is_cpu:
                    self.energy_cpu -= cost
                else:
                    self.energy -= cost
            else:
                self.message = "Edge Added"
            
        # Record for Undo (Clear redo stack on new move)
        self.undo_stack.append((u, v, action))
        self.redo_stack.clear()
        
        self._check_game_status()
        
        if not self.game_over:
            self.switch_turn()
            
        return True

    def get_hint(self):
        """
        Robust Hint System:
        1. Suggest adding a solution edge if valid.
        2. If solution edge is blocked, suggest removing the blocker.
        """
        if not self.solution_edges:
            return None, "No solution available."

        # 1. Look for missing solution edges
        for edge in self.solution_edges:
            if edge not in self.graph.edges:
                u, v = edge
                # Check if we CAN add it
                valid, reason = is_valid_move(self.graph, u, v, self.clues)
                if valid:
                    return (u, v), "Add this solution edge!"
                else:
                    # It's blocked! Find out why.
                    # Usually blocked by degree constraint (already has 2 edges)
                    # We need to remove one of the EXISTING edges at u or v that is NOT in solution.
                    
                    # Check u
                    for neighbor in self.graph.adj_list[u]:
                        existing_edge = tuple(sorted((u, neighbor)))
                        if existing_edge not in self.solution_edges:
                            return existing_edge, "Remove this incorrect edge!"
                            
                    # Check v
                    for neighbor in self.graph.adj_list[v]:
                        existing_edge = tuple(sorted((v, neighbor)))
                        if existing_edge not in self.solution_edges:
                            return existing_edge, "Remove this incorrect edge!"
                            
        # If all solution edges are present, we should have won.
        # If not, maybe we have EXTRA edges that are not in solution?
        for edge in self.graph.edges:
            if edge not in self.solution_edges:
                return edge, "Remove this extra edge!"
                
        return None, "Puzzle solved?"

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
                
        # 1.5. Post-processing: Fill holes to ensure single loop
        # A hole is a non-region cell not reachable from the boundary.
        # We flood fill from the boundary (outside). Any non-region cell not reached is a hole.
        
        # Create a set of all cells
        all_cells = set((r, c) for r in range(self.rows) for c in range(self.cols))
        non_region = all_cells - region
        
        if non_region:
            outside = set()
            queue = []
            
            # Start from boundary cells that are not in region
            for r in range(self.rows):
                for c in range(self.cols):
                    if (r == 0 or r == self.rows - 1 or c == 0 or c == self.cols - 1):
                        if (r, c) not in region:
                            queue.append((r, c))
                            outside.add((r, c))
            
            # BFS to find all "outside" cells
            head = 0
            while head < len(queue):
                curr = queue[head]
                head += 1
                r, c = curr
                
                neighbors = []
                if r > 0: neighbors.append((r-1, c))
                if r < self.rows - 1: neighbors.append((r+1, c))
                if c > 0: neighbors.append((r, c-1))
                if c < self.cols - 1: neighbors.append((r, c+1))
                
                for n in neighbors:
                    if n not in region and n not in outside:
                        outside.add(n)
                        queue.append(n)
            
            # Any non-region cell NOT in 'outside' is a hole. Fill it.
            holes = non_region - outside
            for hole in holes:
                region.add(hole)
                
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
        
        # Calculate Energy for Greedy Mode
        if self.game_mode == "expert":
            total_weight = 0
            for edge in self.solution_edges:
                total_weight += self.edge_weights.get(edge, 0)
            # Give a buffer of 20
            self.energy = total_weight + 20
            self.max_energy = self.energy



    def undo(self):
        if not self.undo_stack: return False
        
        u, v, action = self.undo_stack.pop()
        
        # Expert Mode: Handle Energy Undo
        cost = 0
        if self.game_mode == "expert":
             edge = tuple(sorted((u, v)))
             cost = self.edge_weights.get(edge, 0)

        # Reverse action
        if action == "add":
            self.graph.remove_edge(u, v)
            # Undo "Add" means we regain the cost we spent
            if self.game_mode == "expert":
                # Whose turn was it? The turn has NOT switched back yet.
                # So if it is currently CPU's turn, it means Human made this move.
                # Wait, undo() reverses turn at the END.
                
                # Check who made the move?
                # The stack only stores action. We assume turn switches strictly.
                
                # Current turn is NEXT player. So PREVIOUS player made the move.
                if "CPU" in self.turn: # Current is CPU, so Human made the move
                    self.energy += cost
                else: # Current is Human, so CPU made the move
                    self.energy_cpu += cost
                    
        else: # action == "remove"
            self.graph.add_edge(u, v)
            # Undo "Remove" means we lose the refund we got
            if self.game_mode == "expert":
                if "CPU" in self.turn:
                    self.energy -= cost
                else:
                    self.energy_cpu -= cost
            
        self.redo_stack.append((u, v, action))
        self.switch_turn() # Undo reverses turn too
        self.message = "Undo Successful"
        return True

    def redo(self):
        if not self.redo_stack: return False
        
        u, v, action = self.redo_stack.pop()
        
        # Expert Mode: Handle Energy Redo
        cost = 0
        if self.game_mode == "expert":
             edge = tuple(sorted((u, v)))
             cost = self.edge_weights.get(edge, 0)
        
        # Re-apply action
        if action == "add":
            self.graph.add_edge(u, v)
            # Redo "Add" means we spend cost again
            if self.game_mode == "expert":
                # Current turn is the one making the move
                if "Human" in self.turn:
                    self.energy -= cost
                else:
                    self.energy_cpu -= cost
        else:
            self.graph.remove_edge(u, v)
            # Redo "Remove" means we get refund again
            if self.game_mode == "expert":
                if "Human" in self.turn:
                    self.energy += cost
                else:
                    self.energy_cpu += cost
            
        self.undo_stack.append((u, v, action))
        self.switch_turn()
        self.message = "Redo Successful"
        return True

    def switch_turn(self):
        if self.game_mode in ["vs_cpu", "expert"]:
            if self.turn == "Player 1 (Human)":
                self.turn = "Player 2 (CPU)"
            else:
                self.turn = "Player 1 (Human)"
        else:  # two_player mode
            if self.turn == "Player 1":
                self.turn = "Player 2"
            else:
                self.turn = "Player 1"

    def get_all_valid_moves(self):
        moves = []
        # Horizontal
        for r in range(self.rows + 1):
            for c in range(self.cols):
                u, v = (r, c), (r, c+1)
                if tuple(sorted((u, v))) not in self.graph.edges:
                    valid, _ = is_valid_move(self.graph, u, v, self.clues)
                    if valid:
                        moves.append((u, v))
                        
        # Vertical
        for r in range(self.rows):
            for c in range(self.cols + 1):
                u, v = (r, c), (r+1, c)
                if tuple(sorted((u, v))) not in self.graph.edges:
                    valid, _ = is_valid_move(self.graph, u, v, self.clues)
                    if valid:
                        moves.append((u, v))
        return moves

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
        
        if not self.get_all_valid_moves():
            self.game_over = True
            self.winner = "Stalemate"
            self.message = "GAME OVER! No valid moves left. Stalemate."
            # Record as a draw or loss? Let's just not record it as a win.



