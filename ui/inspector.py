import tkinter as tk
from ui.styles import *
from ui.components import HoverButton, CardFrame
from daa.sorting import heap_sort

class SaveInspector(tk.Toplevel):
    def __init__(self, master, game_state):
        super().__init__(master, bg=BG_COLOR)
        self.title("Save File Inspector (Heap Sort)")
        self.geometry("600x500")
        self.game_state = game_state
        
        tk.Label(self, text="Heap Sort Inspector", font=FONT_TITLE, bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=10)
        tk.Label(self, text="Visualizing how Heap Sort organizes data for saving.", font=FONT_BODY, bg=BG_COLOR, fg=TEXT_DIM).pack(pady=(0, 20))
        
        # Split View
        container = tk.Frame(self, bg=BG_COLOR)
        container.pack(expand=True, fill=tk.BOTH, padx=20)
        
        # Left: Unsorted
        frame_left = CardFrame(container, padx=10, pady=10)
        frame_left.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=5)
        
        tk.Label(frame_left, text="Raw Undo Stack", font=FONT_BODY, bg=CARD_BG, fg=ERROR_COLOR).pack()
        self.txt_left = tk.Text(frame_left, height=15, width=30, bg=BG_COLOR, fg=TEXT_COLOR, font=FONT_SMALL, bd=0)
        self.txt_left.pack(pady=10)
        
        # Right: Sorted
        frame_right = CardFrame(container, padx=10, pady=10)
        frame_right.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH, padx=5)
        
        tk.Label(frame_right, text="Heap Sorted (By Time)", font=FONT_BODY, bg=CARD_BG, fg=SUCCESS_COLOR).pack()
        self.txt_right = tk.Text(frame_right, height=15, width=30, bg=BG_COLOR, fg=TEXT_COLOR, font=FONT_SMALL, bd=0)
        self.txt_right.pack(pady=10)
        
        HoverButton(self, text="Close", command=self.destroy).pack(pady=20)
        
        self.populate_data()
        
    def populate_data(self):
        # 1. Get Raw Data
        stack = self.game_state.undo_stack[:]
        
        # To make it interesting, let's pretend it's shuffled or show indices
        # Actually, let's just show the stack as is vs re-sorted explicitly
        
        items_to_sort = []
        raw_text = ""
        for i, item in enumerate(stack):
            u, v, action = item
            raw_text += f"Idx {i}: {action.upper()} {u}-{v}\n"
            items_to_sort.append({'index': i, 'data': item})
            
        self.txt_left.insert(tk.END, raw_text if raw_text else "Empty Stack")
        
        # 2. Sort using Heap Sort (Showcase)
        sorted_items = heap_sort(items_to_sort, key=lambda x: x['index'])
        
        sorted_text = ""
        for item in sorted_items:
             idx = item['index']
             u, v, action = item['data']
             sorted_text += f"Idx {idx}: {action.upper()} {u}-{v}\n"
             
        self.txt_right.insert(tk.END, sorted_text if sorted_text else "Empty Stack")
