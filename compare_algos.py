"""
Compares our two algorithms:
1. Fractional Knapsack (Standard)
2. Job Sequencing (Variant)
"""

import time
import random
from logic.game_state import GameState
from logic.greedy_cpu import GreedyCPU
from logic.greedy_cpu_job_seq import GreedyCPUJobSeq

def benchmark():
    print("Initializing Benchmark...")
    print("-" * 60)
    print(f"{'Algorithm':<20} | {'Avg Time (ms)':<15} | {'Avg Score':<10} | {'Moves Selected'}")
    print("-" * 60)
    
    iterations = 50
    
    # 1. Test Fractional Knapsack
    total_time_fk = 0
    total_score_fk = 0
    total_candidates_fk = 0
    
    # Use fixed seed for reproducibility across algo runs if possible, 
    # but we will just run on same random states.
    
    # We will generate N random states and run BOTH algos on the SAME state
    seeds = [random.randint(0, 100000) for _ in range(iterations)]
    
    for seed in seeds:
         # Setup State
         random.seed(seed)
         game = GameState(rows=5, cols=5, game_mode="vs_cpu")
         cpu_fk = GreedyCPU(game)
         
         # Measure Time
         start = time.perf_counter()
         candidates, best = cpu_fk.decide_move()
         end = time.perf_counter()
         
         total_time_fk += (end - start) * 1000
         
         if candidates:
             total_score_fk += candidates[0][1] # Best move score
             total_candidates_fk += len(candidates)
             
    avg_time_fk = total_time_fk / iterations
    avg_score_fk = total_score_fk / iterations
    avg_cand_fk = total_candidates_fk / iterations
    
    print(f"{'Frac. Knapsack':<20} | {avg_time_fk:<15.4f} | {avg_score_fk:<10.2f} | {avg_cand_fk:.1f}")
    
    # 2. Test Job Sequencing
    total_time_js = 0
    total_score_js = 0
    total_candidates_js = 0
    
    for seed in seeds:
         # Setup State (Identical)
         random.seed(seed)
         game = GameState(rows=5, cols=5, game_mode="vs_cpu")
         cpu_js = GreedyCPUJobSeq(game)
         
         # Measure Time
         start = time.perf_counter()
         candidates, best = cpu_js.decide_move()
         end = time.perf_counter()
         
         total_time_js += (end - start) * 1000
         
         if candidates:
             total_score_js += candidates[0][1]
             total_candidates_js += len(candidates)

    avg_time_js = total_time_js / iterations
    avg_score_js = total_score_js / iterations
    avg_cand_js = total_candidates_js / iterations
    
    print(f"{'Job Sequencing':<20} | {avg_time_js:<15.4f} | {avg_score_js:<10.2f} | {avg_cand_js:.1f}")
    print("-" * 60)
    print("Benchmark Complete.")

if __name__ == "__main__":
    benchmark()
