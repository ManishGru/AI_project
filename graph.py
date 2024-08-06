import random
import math
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk

def generate_random_graph(n_nodes, edge_probability):
    G = nx.Graph()
    for i in range(n_nodes):
        for j in range(i+1, n_nodes):
            if random.random() < edge_probability:
                G.add_edge(i, j)
    return G

def initial_solution(G, n_colors):
    return {node: random.randint(0, n_colors-1) for node in G.nodes()}

def cost(G, coloring):
    return sum(1 for u, v in G.edges() if coloring[u] == coloring[v])

def neighbor(coloring, n_colors):
    new_coloring = coloring.copy()
    node = random.choice(list(new_coloring.keys()))
    new_coloring[node] = random.randint(0, n_colors-1)
    return new_coloring

def simulated_annealing(G, n_colors, initial_temp, cooling_rate, n_iterations):
    current_solution = initial_solution(G, n_colors)
    current_cost = cost(G, current_solution)
    best_solution = current_solution.copy()
    best_cost = current_cost
    temperature = initial_temp
    cost_history = [current_cost]
    
    for _ in range(n_iterations):
        new_solution = neighbor(current_solution, n_colors)
        new_cost = cost(G, new_solution)
        if new_cost < current_cost or random.random() < math.exp((current_cost - new_cost) / temperature):
            current_solution = new_solution
            current_cost = new_cost
            if current_cost < best_cost:
                best_solution = current_solution.copy()
                best_cost = current_cost
        cost_history.append(current_cost)
        temperature *= cooling_rate
    
    return best_solution, best_cost, cost_history

def find_optimal_coloring(G, initial_temp, cooling_rate, n_iterations):
    n_colors = 1
    while True:
        best_solution, best_cost, cost_history = simulated_annealing(G, n_colors, initial_temp, cooling_rate, n_iterations)
        if best_cost == 0:
            return best_solution, n_colors, cost_history
        n_colors += 1

def plot_results(G, coloring, cost_history):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Plot final graph coloring
    pos = nx.spring_layout(G)
    colors = ['red', 'blue', 'green', 'yellow', 'purple', 'orange', 'pink', 'brown', 'cyan', 'magenta']
    node_colors = [colors[coloring[node] % len(colors)] for node in G.nodes()]
    nx.draw(G, pos, node_color=node_colors, with_labels=True, node_size=500, font_size=10, font_weight='bold', ax=ax1)
    ax1.set_title(f"Final Graph Coloring (Colors used: {len(set(coloring.values()))})")

    # Plot cost over iterations
    ax2.plot(cost_history)
    ax2.set_title("Cost over Iterations")
    ax2.set_xlabel("Iteration")
    ax2.set_ylabel("Cost")

    fig.tight_layout()
    return fig

class GraphColoringApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Graph Coloring with Optimal Color Selection")
        self.geometry("1000x800")

        self.create_widgets()

    def create_widgets(self):
        input_frame = ttk.Frame(self, padding="10")
        input_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(input_frame, text="Number of nodes:").grid(column=0, row=0, sticky=tk.W)
        self.n_nodes = ttk.Entry(input_frame)
        self.n_nodes.grid(column=1, row=0)
        self.n_nodes.insert(0, "20")

        ttk.Label(input_frame, text="Edge probability (0-1):").grid(column=0, row=1, sticky=tk.W)
        self.edge_probability = ttk.Entry(input_frame)
        self.edge_probability.grid(column=1, row=1)
        self.edge_probability.insert(0, "0.3")

        ttk.Label(input_frame, text="Initial temperature:").grid(column=0, row=2, sticky=tk.W)
        self.initial_temp = ttk.Entry(input_frame)
        self.initial_temp.grid(column=1, row=2)
        self.initial_temp.insert(0, "10")

        ttk.Label(input_frame, text="Cooling rate (0-1):").grid(column=0, row=3, sticky=tk.W)
        self.cooling_rate = ttk.Entry(input_frame)
        self.cooling_rate.grid(column=1, row=3)
        self.cooling_rate.insert(0, "0.995")

        ttk.Label(input_frame, text="Number of iterations:").grid(column=0, row=4, sticky=tk.W)
        self.n_iterations = ttk.Entry(input_frame)
        self.n_iterations.grid(column=1, row=4)
        self.n_iterations.insert(0, "1000")

        ttk.Button(input_frame, text="Run Algorithm", command=self.run_algorithm).grid(column=0, row=5, columnspan=2)

        self.result_text = tk.Text(input_frame, height=5, width=50)
        self.result_text.grid(column=0, row=6, columnspan=2)

        self.canvas_frame = ttk.Frame(self)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)

    def run_algorithm(self):
        try:
            n_nodes = int(self.n_nodes.get())
            edge_probability = float(self.edge_probability.get())
            initial_temp = float(self.initial_temp.get())
            cooling_rate = float(self.cooling_rate.get())
            n_iterations = int(self.n_iterations.get())

            G = generate_random_graph(n_nodes, edge_probability)
            best_solution, n_colors, cost_history = find_optimal_coloring(G, initial_temp, cooling_rate, n_iterations)

            result = f"Optimal solution found using {n_colors} colors\n"
            result += "Coloring:\n"
            for node, color in best_solution.items():
                result += f"Node {node}: Color {color}\n"

            self.result_text.delete('1.0', tk.END)
            self.result_text.insert(tk.END, result)

            fig = plot_results(G, best_solution, cost_history)
            
            for widget in self.canvas_frame.winfo_children():
                widget.destroy()

            canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        except ValueError as e:
            self.result_text.delete('1.0', tk.END)
            self.result_text.insert(tk.END, f"Error: {str(e)}\nPlease check your inputs.")

if __name__ == "__main__":
    app = GraphColoringApp()
    app.mainloop()
