"""
Loopy DAA Project - Phase 1
===========================
Entry point for the application.
"""

import ctypes
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass # Not on Windows or already set

from ui.main_window import MainWindow
import sys
from benchmark_viz import run_benchmark_and_plot

if __name__ == "__main__":
    print("="*60)
    print("      SLITHERLINK GAME - ALGORITHM SELECTION")
    print("="*60)
    print("1. Play with Fractional Knapsack (Standard)")
    print("2. Play with Job Sequencing (Experimental)")
    print("3. Run Benchmark & Comparison Graphs")
    print("="*60)
    
    choice = input("Select an option (1-3): ")
    
    algo_choice = "knapsack"
    
    if choice == '1':
        print("Selected: Fractional Knapsack")
        algo_choice = "knapsack"
    elif choice == '2':
        print("Selected: Job Sequencing")
        algo_choice = "job_seq"
    elif choice == '3':
        run_benchmark_and_plot()
        print("Now launching game with Job Sequencing for you to try...")
        algo_choice = "job_seq"
    else:
        print("Invalid choice, defaulting to Fractional Knapsack.")
        
    # We need to inject this choice into the MainWindow/GameState
    # Since MainWindow creates GameState internally or passes it,
    # let's check MainWindow.__init__.
    # Assuming MainWindow takes params to pass to GameState, or we can modify it.
    # For now, let's look at MainWindow in next step if needed, 
    # but based on file list, I should probably check it.
    # However, to avoid complexity, I will set a GLOBAL or ENV VAR, 
    # or pass it if constructor allows.
    
    # Let's inspect MainWindow first to do this cleanly.
    # But for this step I will assume I can modify MainWindow init call.
    # Actually, I haven't seen MainWindow code. 
    # Strategy: Pass it as a kwarg if possible, or modify MainWindow.
    
    # I'll modify MainWindow to accept it.
    app = MainWindow(cpu_algorithm=algo_choice)
    app.mainloop()
