import tkinter as tk
from ui.styles import *
from ui.components import HoverButton, CardFrame
from daa.sorting import heap_sort
import time

class MatchHistoryInspector(tk.Toplevel):
    def __init__(self, master, game_state):
        super().__init__(master, bg=BG_COLOR)
        self.title("Match History Inspector (Heap Sort)")
        self.geometry("700x500")
        self.game_state = game_state
        
        # Header
        tk.Label(self, text="Match History", font=FONT_TITLE, bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=10)
        tk.Label(self, text="Real game records sorted using O(N log N) Heap Sort", font=FONT_BODY, bg=BG_COLOR, fg=TEXT_DIM).pack(pady=(0, 20))
        
        # Toolbar
        toolbar = tk.Frame(self, bg=BG_COLOR)
        toolbar.pack(fill=tk.X, padx=20, pady=5)
        
        HoverButton(toolbar, text="Sort by Recent (Timestamp)", command=self.sort_by_recent, width=25).pack(side=tk.LEFT, padx=5)
        HoverButton(toolbar, text="Sort by Fastest (Duration)", command=self.sort_by_duration, width=25).pack(side=tk.LEFT, padx=5)
        HoverButton(toolbar, text="Sort by Moves", command=self.sort_by_moves, width=25).pack(side=tk.LEFT, padx=5)
        
        # Content Area
        container = CardFrame(self, padx=10, pady=10)
        container.pack(expand=True, fill=tk.BOTH, padx=20, pady=10)
        
        # Scrollable Text as List
        self.list_area = tk.Text(container, bg=BG_COLOR, fg=TEXT_COLOR, font=FONT_SMALL, bd=0, state=tk.DISABLED)
        self.list_area.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        
        scrollbar = tk.Scrollbar(container, command=self.list_area.yview, bg=BG_COLOR)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.list_area.config(yscrollcommand=scrollbar.set)
        
        # Close Button
        HoverButton(self, text="Close", command=self.destroy).pack(pady=20)
        
        # Load Data
        self.history_data = self.game_state.stats_mgr.stats.get("match_history", [])
        self.current_sort = "None"
        
        self.refresh_list()
        
    def refresh_list(self):
        self.list_area.config(state=tk.NORMAL)
        self.list_area.delete(1.0, tk.END)
        
        if not self.history_data:
            self.list_area.insert(tk.END, "\n   No matches recorded yet. Play a game to see stats!\n")
            self.list_area.config(state=tk.DISABLED)
            return
            
        header = f"{'Result':<20} | {'Duration':<15} | {'Moves':<10} | {'Date':<25}\n"
        header += "-" * 80 + "\n"
        self.list_area.insert(tk.END, header)
        
        for record in self.history_data:
            winner = record.get("winner", "Unknown")
            duration = record.get("duration", 0)
            moves = record.get("moves", 0)
            timestamp = record.get("timestamp", 0)
            
            date_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))
            res_str = "WIN" if "Human" in winner else "LOSS"
            
            line = f"{res_str:<20} | {duration:.2f}s{'':<9} | {moves:<10} | {date_str:<25}\n"
            self.list_area.insert(tk.END, line)
            
        self.list_area.config(state=tk.DISABLED)
        
    def sort_by_recent(self):
        # Sort by timestamp DESCENDING (Newest first)
        # Using heap_sort from daa.sorting
        self.history_data = heap_sort(self.history_data, key=lambda x: x.get("timestamp", 0), reverse=True)
        self.refresh_list()
        
    def sort_by_duration(self):
        # Sort by duration ASCENDING (Fastest first)
        self.history_data = heap_sort(self.history_data, key=lambda x: x.get("duration", float('inf')), reverse=False)
        self.refresh_list()

    def sort_by_moves(self):
         # Sort by moves ASCENDING (Fewest moves first)
        self.history_data = heap_sort(self.history_data, key=lambda x: x.get("moves", float('inf')), reverse=False)
        self.refresh_list()
