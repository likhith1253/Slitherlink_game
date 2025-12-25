import tkinter as tk
from tkinter import ttk, messagebox
import time
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from ui.styles import *
from ui.components import HoverButton, CardFrame
from daa.sorting import merge_sort, heap_sort

class BenchmarkPage(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master, bg=BG_COLOR)
        self.title("Algorithm Benchmark")
        self.geometry("800x600")
        
        tk.Label(self, text="Sorting Algorithm Benchmark", font=FONT_TITLE, bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=10)
        
        controls = tk.Frame(self, bg=BG_COLOR)
        controls.pack(pady=10)
        
        tk.Label(controls, text="Data Size (N):", bg=BG_COLOR, fg=TEXT_DIM).pack(side=tk.LEFT, padx=5)
        self.n_var = tk.StringVar(value="1000")
        entry = tk.Entry(controls, textvariable=self.n_var, width=10)
        entry.pack(side=tk.LEFT, padx=5)
        
        HoverButton(controls, text="Run Benchmark", command=self.run_benchmark, fg=APPLE_BLUE).pack(side=tk.LEFT, padx=20)
        
        self.result_frame = tk.Frame(self, bg=BG_COLOR)
        self.result_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        self.fig.patch.set_facecolor(BG_COLOR)
        self.ax.set_facecolor(CARD_BG)
        # Style ticks and labels if possible
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.result_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    def bubble_sort(self, arr):
        n = len(arr)
        for i in range(n):
            for j in range(0, n-i-1):
                if arr[j] > arr[j+1]:
                    arr[j], arr[j+1] = arr[j+1], arr[j]
        return arr
        
    def run_benchmark(self):
        try:
            n = int(self.n_var.get())
            if n > 5000:
                if not messagebox.askyesno("Warning", "N > 5000 might freeze the UI with Bubble Sort. Continue?"):
                    return
        except ValueError:
            messagebox.showerror("Error", "Invalid N")
            return
            
        # Generate Data
        data = [random.random() for _ in range(n)]
        
        times = {}
        
        # 1. Bubble Sort
        arr = data[:]
        start = time.time()
        self.bubble_sort(arr)
        times['Bubble Sort'] = (time.time() - start) * 1000 # ms
        
        # 2. Merge Sort
        arr = data[:]
        start = time.time()
        merge_sort(arr)
        times['Merge Sort'] = (time.time() - start) * 1000
        
        # 3. Heap Sort
        arr = data[:]
        start = time.time()
        heap_sort(arr)
        times['Heap Sort'] = (time.time() - start) * 1000
        
        # 4. Python Sort (Timsort)
        arr = data[:]
        start = time.time()
        sorted(arr)
        times['Python Sort'] = (time.time() - start) * 1000
        
        # Plot
        self.ax.clear()
        self.ax.bar(times.keys(), times.values(), color=[APPLE_RED, APPLE_PURPLE, APPLE_ORANGE, APPLE_GREEN])
        self.ax.set_title(f"Execution Time for N={n} (ms)", color=TEXT_COLOR)
        self.ax.tick_params(axis='x', colors=TEXT_COLOR)
        self.ax.tick_params(axis='y', colors=TEXT_COLOR)
        self.ax.spines['bottom'].set_color(TEXT_COLOR)
        self.ax.spines['top'].set_color(TEXT_COLOR) 
        self.ax.spines['left'].set_color(TEXT_COLOR)
        self.ax.spines['right'].set_color(TEXT_COLOR)
        
        for i, v in enumerate(times.values()):
            self.ax.text(i, v + 0.5, f"{v:.1f}", color=TEXT_COLOR, ha='center')
            
        self.canvas.draw()
