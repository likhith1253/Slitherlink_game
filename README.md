# Loopy DAA - Slitherlink AI Duel

**Course**: Design and Analysis of Algorithms (DAA)  
**Project**: Phase 1 - Slitherlink Game with AI  

## Overview
This is a Python-based implementation of the puzzle game **Slitherlink** (also known as Loopy). It features a polished "Apple Professional" dark UI, a smart Hint system, and an AI opponent powered by Greedy algorithms and Sorting.

## Features
- **Game Modes**: Easy (4x4), Medium (5x5), Hard (7x7).
- **AI Opponent**: A Greedy CPU that uses Sorting algorithms to pick the best moves.
- **Smart Hints**: Guarantees a winnable path using internal graph solving logic.
- **Undo/Redo**: Full history support.
- **Statistics**: Tracks wins, losses, and games played.
- **Professional UI**: Radiant Dark theme with neon accents and smooth animations.

## DAA Syllabus Integration
This project explicitly demonstrates the following Unit 1 & 2 topics:
1.  **Graph Representation**: The board is modeled as a graph (Adjacency List) in `logic/graph.py`.
2.  **Graph Algorithms**:
    *   **BFS/DFS**: Used for board generation and connectivity checks (`daa/graph_algos.py`).
    *   **Cycle Detection**: Used to validate loops.
3.  **Sorting**: Bubble, Insertion, and Selection Sort are implemented in `daa/sorting.py` and used by the CPU to rank moves.
4.  **Asymptotic Analysis**: Complexity notes are provided in `daa/analysis_notes.py`.

## How to Run
1.  Python 3.9+ with Tkinter (included with the standard Windows/macOS installers; `sudo apt install python3-tk` on Debian/Ubuntu).
2.  Start the game:
    ```bash
    python main.py
    ```
3.  Optional charts (`benchmark_viz.py`, `compare_algos.py`, `correctness_proof_viz.py`) need `pip install matplotlib numpy networkx`.

## Tests
```bash
pip install pytest
python -m pytest tests
```
Five tests cover job sequencing with deadlines and headless game simulations (human vs CPU move/undo/hint, expert-mode energy, CPU loop prevention). The Tkinter interface itself is not covered by automated tests.

## Project Structure
*   `main.py`: Entry point.
*   `ui/`: User Interface components (Tkinter).
*   `logic/`: Core game logic (GameState, Validators, CPU players).
*   `daa/`: Algorithms implementation (Sorting, Graphs, Greedy algorithms).
*   `data/`: Stores game statistics (`statistics.json`, includes a match history).
*   `tests/`: Automated tests.

## Limitations
*   No benchmark numbers are committed: run `benchmark_viz.py` / `compare_algos.py` to measure the algorithms on your machine.
*   Save files (`savegame.bin`) are Python pickles; only load saves you created yourself.
*   The "Smart Hints" and the CPU opponents are heuristics (greedy / job sequencing / knapsack variants), not a complete Slitherlink solver guarantee.

## License
MIT, see [LICENSE](LICENSE).

## Controls
*   **Left Click**: Toggle edge (Line / Empty).
*   **Undo/Redo**: Use on-screen buttons.
*   **Hint**: Request a move suggestion.

---
*Generated for DAA Course Submission*
