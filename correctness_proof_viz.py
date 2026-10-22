import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

def generate_proof_visualization():
    # Create a figure with 2 subplots
    fig = plt.figure(figsize=(14, 6))
    
    # --- Left Subplot: The Logic Tree (Proof by Contradiction) ---
    ax1 = fig.add_subplot(121)
    
    G = nx.DiGraph()
    
    # Define Nodes
    root = "Unsatisfied Constraint\n(e.g., Cell 3)"
    left_move = "Greedy Move\n(Satisfy Constraint)"
    right_move = "Non-Greedy Move\n(Ignore Constraint)"
    valid_state = "Valid State"
    violation = "Violation\n(Constraint Broken)"
    solvable = "Solvable"
    crash = "CRASH\n(Contradiction)"
    
    # Add Edges
    G.add_edge(root, left_move)
    G.add_edge(root, right_move)
    G.add_edge(left_move, valid_state)
    G.add_edge(right_move, violation)
    G.add_edge(valid_state, solvable)
    G.add_edge(violation, crash)
    
    # Layout
    pos = {
        root: (0, 10),
        left_move: (-2, 6),
        right_move: (2, 6),
        valid_state: (-2, 3),
        violation: (2, 3),
        solvable: (-2, 0),
        crash: (2, 0)
    }
    
    # Draw Nodes
    nx.draw_networkx_nodes(G, pos, ax=ax1, node_size=3000, node_color='lightgray', edgecolors='black')
    
    # Draw Labels
    nx.draw_networkx_labels(G, pos, ax=ax1, font_size=9, font_weight='bold')
    
    # Draw Edges (Green for Safe, Red for Unsafe)
    safe_edges = [(root, left_move), (left_move, valid_state), (valid_state, solvable)]
    unsafe_edges = [(root, right_move), (right_move, violation), (violation, crash)]
    
    nx.draw_networkx_edges(G, pos, ax=ax1, edgelist=safe_edges, edge_color='green', width=2, arrows=True, arrowstyle='-|>', arrowsize=20)
    nx.draw_networkx_edges(G, pos, ax=ax1, edgelist=unsafe_edges, edge_color='red', width=2, arrows=True, arrowstyle='-|>', arrowsize=20)
    
    ax1.set_title("Logic Tree: Proof by Contradiction", fontsize=14, fontweight='bold')
    ax1.axis('off')
    
    # --- Right Subplot: Sorting Efficiency ---
    ax2 = fig.add_subplot(122)
    
    # Data
    steps = np.arange(1, 6)
    random_possibilities = [100, 80, 60, 40, 20]
    sorted_possibilities = [100, 20, 5, 1, 0]  # Drastic reduction
    
    width = 0.35
    
    ax2.bar(steps - width/2, random_possibilities, width, label='Random Execution', color='gray', alpha=0.7)
    ax2.bar(steps + width/2, sorted_possibilities, width, label='Sorted Execution (Greedy)', color='green', alpha=0.8)
    
    ax2.set_xlabel('Step Number', fontsize=12)
    ax2.set_ylabel('Remaining Possibilities (Search Space)', fontsize=12)
    ax2.set_title('Sorting Efficiency: Search Space Reduction', fontsize=14, fontweight='bold')
    ax2.set_xticks(steps)
    ax2.legend()
    
    # Annotations to highlight efficiency
    ax2.annotate('Tight Constraints First\n(Massive Pruning)', xy=(2 + width/2, 20), xytext=(3, 50),
                 arrowprops=dict(facecolor='black', shrink=0.05), fontsize=10)
    
    plt.tight_layout()
    plt.savefig('correctness_proof.png', dpi=300)
    print("Graph generated and saved as 'correctness_proof.png'")

if __name__ == "__main__":
    generate_proof_visualization()
