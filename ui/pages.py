"""
UI Pages
========
Content pages for the main window.
Includes Game Over handling.
"""

import tkinter as tk
from tkinter import messagebox
from ui.styles import *
from ui.components import HoverButton, CardFrame
from ui.board_canvas import BoardCanvas
from logic.game_state import GameState

class HomePage(tk.Frame):
    def __init__(self, master, on_start_game):
        super().__init__(master, bg=BG_COLOR)
        self.on_start_game = on_start_game
        
        # Hero Section
        tk.Label(self, text="Loopy.", font=FONT_TITLE, bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=(80, 10))
        tk.Label(self, text="The Slitherlink Duel.", font=FONT_HEADER, bg=BG_COLOR, fg=TEXT_DIM).pack(pady=(0, 60))
        
        # Difficulty Selection
        card = CardFrame(self, padx=40, pady=40)
        card.pack(pady=20)
        
        tk.Label(card, text="Select Difficulty", font=FONT_BODY, bg=CARD_BG, fg=TEXT_DIM).pack(pady=(0, 20))
        
        HoverButton(card, text="Easy (4x4)", command=lambda: on_start_game(4, 4, "Easy"), width=24, fg=APPLE_GREEN).pack(pady=5)
        HoverButton(card, text="Medium (5x5)", command=lambda: on_start_game(5, 5, "Medium"), width=24, fg=APPLE_BLUE).pack(pady=5)
        HoverButton(card, text="Hard (7x7)", command=lambda: on_start_game(7, 7, "Hard"), width=24, fg=APPLE_RED).pack(pady=5)

class GamePage(tk.Frame):
    def __init__(self, master, game_state, on_back):
        super().__init__(master, bg=BG_COLOR)
        self.game_state = game_state
        self.on_back = on_back
        
        # Top Bar (Info)
        self.info_bar = tk.Frame(self, bg=BG_COLOR)
        self.info_bar.pack(fill=tk.X, pady=20, padx=40)
        
        self.lbl_turn = tk.Label(self.info_bar, text="", font=FONT_HEADER, bg=BG_COLOR, fg=ACCENT_COLOR)
        self.lbl_turn.pack(side=tk.LEFT)
        
        self.lbl_status = tk.Label(self.info_bar, text="", font=FONT_BODY, bg=BG_COLOR, fg=TEXT_DIM)
        self.lbl_status.pack(side=tk.RIGHT)
        
        # Board Area
        self.board_frame = CardFrame(self, padx=20, pady=20)
        self.board_frame.pack(expand=True, fill=tk.BOTH, padx=40, pady=(0, 20))
        
        self.canvas = BoardCanvas(self.board_frame, game_state, self.on_move)
        self.canvas.pack(expand=True, fill=tk.BOTH)
        
        # Controls
        controls = tk.Frame(self, bg=BG_COLOR)
        controls.pack(fill=tk.X, pady=20, padx=40)
        
        HoverButton(controls, text="Undo", command=self.undo, fg=WARNING_COLOR).pack(side=tk.LEFT, padx=5)
        HoverButton(controls, text="Redo", command=self.redo, fg=WARNING_COLOR).pack(side=tk.LEFT, padx=5)
        HoverButton(controls, text="Hint", command=self.hint, fg=SUCCESS_COLOR).pack(side=tk.LEFT, padx=5)
        HoverButton(controls, text="End Game", command=on_back, fg=ERROR_COLOR).pack(side=tk.RIGHT, padx=5)
        
        self.update_ui()

    def on_move(self, u, v):
        if self.game_state.make_move(u, v):
            self.update_ui()
            self.check_game_over()
            if not self.game_state.game_over and self.game_state.turn == "Player 2 (CPU)":
                self.after(500, self.cpu_move)

    def cpu_move(self):
        move = self.game_state.cpu.make_move()
        if move:
            u, v = move
            self.game_state.make_move(u, v, is_cpu=True)
            self.update_ui()
            self.check_game_over()

    def check_game_over(self):
        if self.game_state.game_over:
            winner = self.game_state.winner
            if winner == "Stalemate":
                msg = "Game Over!\nStalemate: No valid moves left."
            else:
                msg = f"Game Over!\nWinner: {winner}"
            messagebox.showinfo("Game Over", msg)
            # Optionally navigate back or show a "Play Again" button
            # For now, just show info.

    def undo(self):
        if self.game_state.undo():
            self.update_ui()

    def redo(self):
        if self.game_state.redo():
            self.update_ui()

    def hint(self):
        move, reason = self.game_state.get_hint()
        if move:
            self.canvas.show_hint(move)
            self.game_state.message = f"Hint: {reason}"
            self.update_ui()
        else:
            self.game_state.message = "No hints available."
            self.update_ui()

    def update_ui(self):
        self.canvas.draw()
        self.lbl_turn.config(text=f"Turn: {self.game_state.turn}")
        self.lbl_status.config(text=self.game_state.message)

class StatsPage(tk.Frame):
    def __init__(self, master, on_back):
        super().__init__(master, bg=BG_COLOR)
        
        tk.Label(self, text="Statistics", font=FONT_TITLE, bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=40)
        
        card = CardFrame(self, padx=40, pady=40)
        card.pack(pady=20)
        
        # Load stats
        from logic.statistics import StatisticsManager
        stats = StatisticsManager().stats
        
        tk.Label(card, text=f"Games Played: {stats.get('games_played', 0)}", font=FONT_BODY, bg=CARD_BG, fg=TEXT_COLOR).pack(anchor="w", pady=5)
        tk.Label(card, text=f"Wins vs CPU: {stats.get('wins_vs_cpu', 0)}", font=FONT_BODY, bg=CARD_BG, fg=APPLE_GREEN).pack(anchor="w", pady=5)
        tk.Label(card, text=f"Losses: {stats.get('losses', 0)}", font=FONT_BODY, bg=CARD_BG, fg=APPLE_RED).pack(anchor="w", pady=5)
        
        HoverButton(self, text="Back", command=on_back).pack(pady=20)
