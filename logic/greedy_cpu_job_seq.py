"""
Greedy CPU Logic (Job Sequencing Version)
=========================================
Alternative AI Player implementation using Job Sequencing with Deadlines.
Used for comparison with the standard Fractional Knapsack version.
"""

from logic.greedy_cpu import GreedyCPU
from daa.greedy_algos import job_sequencing_with_deadlines

class GreedyCPUJobSeq(GreedyCPU):
    """
    GreedyCPU variant that uses Job Sequencing with Deadlines
    instead of Fractional Knapsack for move selection.
    """
    def __init__(self, game_state):
        super().__init__(game_state)
        # No print here
        self.algorithm_name = "Job Sequencing"

    def decide_move(self):
        """
        Calculates and returns (candidates, best_move).
        Uses Job Sequencing with Deadlines to filter considered moves.
        Then sorts the result using BUBBLE SORT (inherited).
        """
        # 1. Get Candidate Moves (Raw)
        raw_candidates = self.get_ranked_moves()
        
        if not raw_candidates:
            return [], None
            
        # 2. FILTERING using JOB SEQUENCING
        # We give each move a "deadline" based on how good it is.
        # Better moves have tighter deadlines (we must do them now).
        
        # Prepare Jobs
        jobs = []
        # We need to map ID back to the move object
        # ID will be the index in raw_candidates
        
        for i, (move, score) in enumerate(raw_candidates):
            # Assign Deadline based on Score Tiers (Urgency)
            if score >= 100:
                deadline = 1 # CRITICAL: Do immediately
            elif score >= 50:
                deadline = 2 # HIGH: Do soon
            elif score > 0:
                deadline = 3 # MEDIUM
            else:
                deadline = 5 # LOW: Can wait (likely won't be picked if slot 4 is full)
            
            # Job ID = index, Profit = score, Deadline = deadline
            jobs.append({'id': i, 'deadline': deadline, 'profit': score})
            
        # Call Job Sequencing Algorithm
        # Returns: selected_job_ids, total_profit
        selected_indices, _ = job_sequencing_with_deadlines(jobs)
        
        # Map back to final_candidates
        final_candidates = []
        for idx in selected_indices:
            final_candidates.append(raw_candidates[idx])
            
        # Fallback if nothing selected (shouldn't happen with valid jobs but safety first)
        if not final_candidates:
            final_candidates = raw_candidates

        # 3. Select Best Move using BUBBLE SORT - DAA Requirement
        # (We use the inherited method to ensure fair comparison of the final sorting step)
        moves_to_sort = final_candidates[:] 
        
        # Sort by score in descending order using explicit Bubble Sort
        sorted_moves = self.bubble_sort_moves(moves_to_sort)
        
        # GREEDY CHOICE PROPERTY
        best_move = sorted_moves[0][0]
        return sorted_moves, best_move
