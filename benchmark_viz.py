import time
import random
import matplotlib.pyplot as plt

"""
Visual Benchmark Script
-----------------------
This script runs both algorithms on different grid sizes
and plots the results to compare them visually.
"""
from logic.game_state import GameState
from logic.greedy_cpu import GreedyCPU
from logic.greedy_cpu_job_seq import GreedyCPUJobSeq

def run_benchmark_and_plot():
    print("Running Benchmark for Visualization...")
    
    # Independent Variables
    grid_sizes = range(3, 11) # 3x3 to 10x10
    vertices = []
    edges = []
    
    # Dependent Variables
    times_knapsack = []
    times_jobseq = []
    
    for N in grid_sizes:
        rows, cols = N, N
        V = (rows + 1) * (cols + 1)
        E = (rows * (cols + 1)) + ((rows + 1) * cols)
        
        vertices.append(V)
        edges.append(E)
        
        # Run multiple iterations to get stable average
        iterations = 10
        total_k_time = 0
        total_j_time = 0
        
        for _ in range(iterations):
            seed = random.randint(0, 100000)
            
            # Test Knapsack
            random.seed(seed)
            game_k = GameState(rows=rows, cols=cols, game_mode="vs_cpu")
            cpu_k = GreedyCPU(game_k)
            t0 = time.perf_counter()
            cpu_k.decide_move()
            total_k_time += (time.perf_counter() - t0)
            
            # Test Job Seq
            random.seed(seed)
            game_j = GameState(rows=rows, cols=cols, game_mode="vs_cpu")
            cpu_j = GreedyCPUJobSeq(game_j)
            t0 = time.perf_counter()
            cpu_j.decide_move()
            total_j_time += (time.perf_counter() - t0)
            
        # Store Avg Time in Microseconds
        times_knapsack.append((total_k_time / iterations) * 1_000_000)
        times_jobseq.append((total_j_time / iterations) * 1_000_000)
        
        print(f"Size {N}x{N} ({V} Vertices, {E} Edges) -> K: {times_knapsack[-1]:.2f}µs, J: {times_jobseq[-1]:.2f}µs")

    # Plotting
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Plot 1: Time vs Vertices
    ax1.plot(vertices, times_knapsack, 'o-', label='Fractional Knapsack', color='blue')
    ax1.plot(vertices, times_jobseq, 's-', label='Job Sequencing', color='green')
    ax1.set_title('Execution Time vs Number of Vertices (V)')
    ax1.set_xlabel('Number of Vertices (V)')
    ax1.set_ylabel('Execution Time (µs)')
    ax1.legend()
    ax1.grid(True)
    
    # Plot 2: Time vs Edges
    ax2.plot(edges, times_knapsack, 'o-', label='Fractional Knapsack', color='blue')
    ax2.plot(edges, times_jobseq, 's-', label='Job Sequencing', color='green')
    ax2.set_title('Execution Time vs Number of Edges (E)')
    ax2.set_xlabel('Number of Edges (E)')
    ax2.set_ylabel('Execution Time (µs)')
    ax2.legend()
    ax2.grid(True)
    
    plt.tight_layout()
    print("Displaying graphs... Close the window to continue to the game.")
    plt.show()

if __name__ == "__main__":
    run_benchmark_and_plot()
