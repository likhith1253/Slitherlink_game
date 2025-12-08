"""
Board Canvas
============
Handles the drawing of the game grid, edges, and interaction.
Clean, minimalist Apple style.
"""

import tkinter as tk
from ui.styles import *

class BoardCanvas(tk.Canvas):
    def __init__(self, master, game_state, on_move_callback):
        super().__init__(master, bg=BG_COLOR, highlightthickness=0)
        self.game_state = game_state
        self.on_move_callback = on_move_callback
        
        self.cell_size = CELL_SIZE
        self.margin = 40
        
        self.bind("<Button-1>", self.on_click)
        self.bind("<Motion>", self.on_hover)
        
        self.hovered_edge = None
        self.hint_edge = None
        
    def draw(self):
        self.delete("all")
        
        rows = self.game_state.rows
        cols = self.game_state.cols
        
        # Center the grid
        width = self.winfo_width()
        height = self.winfo_height()
        
        if width < 10: width = 600
        if height < 10: height = 600
            
        grid_w = cols * self.cell_size
        grid_h = rows * self.cell_size
        
        self.start_x = (width - grid_w) // 2
        self.start_y = (height - grid_h) // 2
        
        # Draw Background Grid (Very subtle dots)
        for r in range(rows + 1):
            for c in range(cols + 1):
                x = self.start_x + c * self.cell_size
                y = self.start_y + r * self.cell_size
                # Tiny guide dots
                self.create_oval(x-1, y-1, x+1, y+1, fill="#3A3A3C", outline="")

        # Draw Clues
        for r in range(rows):
            for c in range(cols):
                if (r, c) in self.game_state.clues:
                    val = self.game_state.clues[(r, c)]
                    x = self.start_x + c * self.cell_size + self.cell_size // 2
                    y = self.start_y + r * self.cell_size + self.cell_size // 2
                    
                    color = TEXT_DIM # Default grey
                    if self._is_clue_satisfied((r, c), val):
                        color = APPLE_BLUE # Blue when done (Apple style)
                    elif self._is_clue_violated((r, c), val):
                        color = APPLE_RED
                        
                    self.create_text(x, y, text=str(val), font=FONT_CLUE, fill=color)
        
        # Draw Active Edges
        for edge in self.game_state.graph.edges:
            self._draw_edge(edge, TEXT_COLOR, width=3) # White lines
            
        # Draw Hovered Edge
        if self.hovered_edge:
            edge = tuple(sorted(self.hovered_edge))
            if edge not in self.game_state.graph.edges:
                self._draw_edge(self.hovered_edge, "#3A3A3C", width=3) # Dark grey hover

        # Draw Hint Edge
        if self.hint_edge:
            self._draw_edge(self.hint_edge, APPLE_YELLOW, width=3)

        # Draw Dots (Vertices)
        for r in range(rows + 1):
            for c in range(cols + 1):
                x = self.start_x + c * self.cell_size
                y = self.start_y + r * self.cell_size
                self.create_oval(x - DOT_RADIUS, y - DOT_RADIUS, x + DOT_RADIUS, y + DOT_RADIUS, fill=TEXT_COLOR, outline="")

    def _draw_edge(self, edge, color, width):
        (r1, c1), (r2, c2) = edge
        x1 = self.start_x + c1 * self.cell_size
        y1 = self.start_y + r1 * self.cell_size
        x2 = self.start_x + c2 * self.cell_size
        y2 = self.start_y + r2 * self.cell_size
        
        self.create_line(x1, y1, x2, y2, width=width, fill=color, capstyle=tk.ROUND)

    def _is_clue_satisfied(self, cell, val):
        from logic.validators import count_edges_around_cell
        return count_edges_around_cell(self.game_state.graph, cell) == val

    def _is_clue_violated(self, cell, val):
        from logic.validators import count_edges_around_cell
        return count_edges_around_cell(self.game_state.graph, cell) > val

    def on_hover(self, event):
        edge = self._get_closest_edge(event.x, event.y)
        if edge != self.hovered_edge:
            self.hovered_edge = edge
            self.draw()

    def on_click(self, event):
        if self.game_state.game_over: return
        edge = self._get_closest_edge(event.x, event.y)
        if edge:
            u, v = edge
            self.on_move_callback(u, v)
            self.hint_edge = None
            self.draw()

    def _get_closest_edge(self, x, y):
        threshold = 15
        rows = self.game_state.rows
        cols = self.game_state.cols
        
        best_edge = None
        min_dist = float('inf')
        
        # Horizontal
        for r in range(rows + 1):
            for c in range(cols):
                x1 = self.start_x + c * self.cell_size
                y1 = self.start_y + r * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1
                
                if abs(y - y1) < threshold and x1 <= x <= x2:
                    dist = abs(y - y1)
                    if dist < min_dist:
                        min_dist = dist
                        best_edge = ((r, c), (r, c+1))
                        
        # Vertical
        for r in range(rows):
            for c in range(cols + 1):
                x1 = self.start_x + c * self.cell_size
                y1 = self.start_y + r * self.cell_size
                x2 = x1
                y2 = y1 + self.cell_size
                
                if abs(x - x1) < threshold and y1 <= y <= y2:
                    dist = abs(x - x1)
                    if dist < min_dist:
                        min_dist = dist
                        best_edge = ((r, c), (r+1, c))
                        
        return best_edge

    def show_hint(self, edge):
        self.hint_edge = edge
        self.draw()
