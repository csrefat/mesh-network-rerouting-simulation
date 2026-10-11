import networkx as nx
import matplotlib.pyplot as plt
import time
import pandas as pd

def create_10_node_mesh():
    """10 node """
    G = nx.Graph()
    
    # 10 Nodes (0 to 9)
    G.add_nodes_from(range(10))
    
    # Weighted Edges (u, v, latency/weight)
    edges = [
        (0, 1, 2), (0, 2, 3), (0, 3, 4),
        (1, 4, 2), (2, 4, 3), (2, 5, 2), (3, 6, 3),
        (4, 7, 2), (5, 7, 3), (5, 8, 4), (6, 8, 2),
        (7, 9, 2), (8, 9, 3), (4, 5, 1), (7, 8, 2)
    ]
    
    for u, v, w in edges:
        G.add_edge(u, v, weight=w)
        
    return G

def plot_network(G, path, title, filename):
    """shortest path """
    pos = {
        0: (0, 1), 
        1: (1, 2), 2: (1, 1), 3: (1, 0),
        4: (2, 2), 5: (2, 1), 6: (2, 0),
        7: (3, 2), 8: (3, 0),
        9: (4, 1)
    }
    
    plt.figure(figsize=(9, 5))
    
    # All nodes and edges
    nx.draw_networkx_nodes(G, pos, node_color='skyblue', node_size=700)
    nx.draw_networkx_labels(G, pos, font_size=12, font_weight='bold')
    nx.draw_networkx_edges(G, pos, edge_color='gray', style='dashed', width=1.5)
    
    # Highlight Shortest Path
    if path:
        path_edges = list(zip(path[:-1], path[1:]))
        nx.draw_networkx_nodes(G, pos, nodelist=path, node_color='springgreen', node_size=800)
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=3)
        
    # Edge Weights (Latency)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    
    plt.title(title, fontsize=14, fontweight='bold')
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.show()

def run_mesh_simulation(source_node=0, sink_node=9, failed_node=4):
    print("="*50)
    print("      MESH NETWORK RE-ROUTING SIMULATION      ")
    print("="*50)
    
    # 1. Initialize Network
    G = create_10_node_mesh()
    
    # 2. Compute Initial Shortest Path
    t_start = time.perf_counter()
    initial_path = nx.dijkstra_path(G, source_node, sink_node, weight='weight')
    initial_cost = nx.dijkstra_path_length(G, source_node, sink_node, weight='weight')
    t_initial_ms = (time.perf_counter() - t_start) * 1000
    
    print(f"[+] Initial Path ({source_node} -> {sink_node}): {initial_path}")
    print(f"[+] Path Cost / Latency: {initial_cost} ms")
    print(f"[+] Path Discovery Time: {t_initial_ms:.4f} ms\n")
    
    # Plot Normal State
    plot_network(G, initial_path, "Normal Network State (Shortest Path: Red)", "normal_mesh.png")
    
    # 3. Simulate Node Failure
    print(f"[!] Simulating Node Failure on Node {failed_node}...")
    G.remove_node(failed_node)
    
    # 4. Re-routing / Convergence
    t_start = time.perf_counter()
    if nx.has_path(G, source_node, sink_node):
        new_path = nx.dijkstra_path(G, source_node, sink_node, weight='weight')
        new_cost = nx.dijkstra_path_length(G, source_node, sink_node, weight='weight')
        t_reroute_ms = (time.perf_counter() - t_start) * 1000
        
        print(f"[✓] Re-routing Successful!")
        print(f"[+] New Path: {new_path}")
        print(f"[+] New Path Cost: {new_cost} ms")
        print(f"[+] Convergence / Re-routing Time: {t_reroute_ms:.4f} ms")
        
        # Plot Failed State
        plot_network(G, new_path, f"After Node {failed_node} Failure (Re-routed Path: Red)", "rerouted_mesh.png")
        
        # 5. Output Summary Table
        df = pd.DataFrame([{
            "Metric": "Initial State",
            "Path": str(initial_path),
            "Hop Count": len(initial_path) - 1,
            "Path Cost (ms)": initial_cost,
            "Computation Delay (ms)": round(t_initial_ms, 4)
        }, {
            "Metric": f"After Node {failed_node} Failure",
            "Path": str(new_path),
            "Hop Count": len(new_path) - 1,
            "Path Cost (ms)": new_cost,
            "Computation Delay (ms)": round(t_reroute_ms, 4)
        }])
        
        print("\n" + "="*50)
        print("SIMULATION RESULTS SUMMARY:")
        print("="*50)
        print(df.to_string(index=False))
        df.to_csv("simulation_results.csv", index=False)
        print("\n[+] Results saved to 'simulation_results.csv'")
    else:
        print("[X] Network Partitioned! No path available.")

if __name__ == "__main__":
    run_mesh_simulation(source_node=0, sink_node=9, failed_node=4)
