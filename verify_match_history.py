
import tkinter as tk
import os
import json
import time
from ui.inspector import MatchHistoryInspector
from logic.game_state import GameState

# Mock GameState
class MockGameState:
    def __init__(self):
        from logic.statistics import StatisticsManager
        self.stats_mgr = StatisticsManager()

# Populate dummy data
def populate_dummy_data():
    stats_file = "data/statistics.json"
    data = {
        "games_played": 5,
        "wins_vs_cpu": 3,
        "losses": 2,
        "fastest_win": 45.5,
        "match_history": [
            {"timestamp": time.time() - 10000, "winner": "Player 1 (Human)", "duration": 120.5, "moves": 30},
            {"timestamp": time.time() - 5000, "winner": "Player 2 (CPU)", "duration": 80.2, "moves": 25},
            {"timestamp": time.time() - 100, "winner": "Player 1 (Human)", "duration": 45.5, "moves": 15},
            {"timestamp": time.time(), "winner": "Player 2 (CPU)", "duration": 200.0, "moves": 50},
        ]
    }
    
    os.makedirs("data", exist_ok=True)
    with open(stats_file, 'w') as f:
        json.dump(data, f)
    print("Dummy stats created.")

if __name__ == "__main__":
    populate_dummy_data()
    
    root = tk.Tk()
    root.withdraw() # Hide root
    
    game_state = MockGameState()
    
    print("Launching Match History Inspector...")
    inspector = MatchHistoryInspector(root, game_state)
    
    # Wait for user to close
    root.wait_window(inspector)
    print("Test Complete.")
