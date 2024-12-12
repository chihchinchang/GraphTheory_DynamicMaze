from maze_game import MazeGame
from graph import Graph  # Import the Graph class

def main():
    # --- Graph Testing Section ---
    print("Graph Test Results:")

    # Initialize an undirected graph for testing
    graph = Graph(directed=False)

    # Add nodes and edges
    graph.add_node('A')
    graph.add_node('B')
    graph.add_node('C')
    graph.add_node('D')
    graph.add_node('E')
    graph.add_node('F')
    graph.add_node('G')
    graph.add_node('H')
    graph.add_node('I')

    graph.add_edge('A', 'B', 5)
    graph.add_edge('A', 'C', 2)
    graph.add_edge('B', 'D', 1)
    graph.add_edge('B', 'E', 3)
    graph.add_edge('C', 'F', 4)
    graph.add_edge('D', 'F', 6)
    graph.add_edge('E', 'G', 7)
    graph.add_edge('F', 'H', 2)
    graph.add_edge('G', 'I', 4)
    graph.add_edge('H', 'I', 3)

    # Remove edges
    #graph.remove_edge('A', 'B')
    #graph.remove_edge('A', 'C')
    #graph.remove_edge('B', 'D')
    #graph.remove_edge('B', 'E')
    #graph.remove_edge('C', 'F')
    #graph.remove_edge('D', 'F')
    #graph.remove_edge('E', 'G')
    #graph.remove_edge('F', 'H')
    #graph.remove_edge('G', 'I')
    #graph.remove_edge('H', 'I')


    # --- Test Save ---
    print("\n--- Graph Saving ---")
    graph.display_graph()
    graph.save_graph('my_graph.txt')


    # --- Test Load ---
    print("\n--- Graph loading ---")
    loaded_graph = Graph(directed=False)
    loaded_graph.load_graph('my_graph.txt')
    print("\n--- Graph after loading from file ---")
    loaded_graph.display_graph()

    # Find the saved file in Finder
    import os
    print(os.getcwd())
    print("In finder, press Command + Shift + G, paste the path.")

    # --- Display the graph structure ---
    print("\n--- Graph Structure ---")
    graph.display_graph()


    # --- Test Basic Graph Metrics ---
    print("\n--- Basic Graph Metrics ---")
    print(f"Degree of A: {graph.node_degree('A')}")
    print(f"Graph Density: {graph.graph_density()}")


    # --- Test Pathfinding Algorithms ---
    print("\n--- Pathfinding Algorithms ---")
    print(f"Shortest Path from A to I: {graph.find_shortest_path('A', 'I')}")
    print(f"All Paths from A to I: {graph.all_paths('A', 'I')}")


    # --- Test Graph Traversal Algorithms (with stopping at the end node) ---
    print("\n--- Graph Traversal Algorithms ---")
    print(f"BFS starting from A to I: {graph.bfs('A', 'I')}")
    print(f"DFS starting from A to I: {graph.dfs('A', 'I')}")


    # --- Test Graph Coloring ---
    print("\n--- Graph Coloring ---")
    print(f"Graph Coloring: {graph.graph_coloring()}")


    # --- Test Connected Components (Undirected Graph) ---
    print("\n--- Connected Components ---")
    print(f"Connected Components: {graph.connected_components()}")


    # --- Test Strongly Connected Components (Directed Graph) ---
    # First, set the graph to be directed for testing SCC
    print("\n--- Strongly Connected Components ---")

    # Create a directed graph for testing SCC
    directed_graph = Graph(directed=True)  # Directed graph

    # Add nodes to the directed graph
    directed_graph.add_node('A')
    directed_graph.add_node('B')
    directed_graph.add_node('C')
    directed_graph.add_node('D')

    # Add edges to the directed graph (this graph has two SCCs)
    directed_graph.add_edge('A', 'B', 5)
    directed_graph.add_edge('B', 'C', 2)
    directed_graph.add_edge('C', 'A', 3)  # SCC 1: A -> B -> C -> A
    directed_graph.add_edge('B', 'D', 1)  # D is a separate SCC
    directed_graph.add_edge('D', 'D', 4)  # SCC 2: D is self-connected

    # Test SCC (Strongly Connected Components) using Tarjan's algorithm
    print(f"Strongly Connected Components: {directed_graph.tarjan_scc()}")


    # --- Maze Game Section ---
    print("\n--- Starting Maze Game ---")

    # Initialize the maze game
    game = MazeGame()

    # Set up the game with a maze
    nodes = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
    edges = [
        ('A', 'B', 5), ('A', 'C', 2),
        ('B', 'D', 1), ('B', 'E', 3),
        ('C', 'F', 4), ('D', 'F', 6),
        ('E', 'G', 7), ('F', 'H', 2),
        ('G', 'I', 4), ('H', 'I', 3)
    ]
    start = 'A'
    end = 'I'

    graph.display_graph()

    game.setup_game(nodes, edges, start, end)

    # Play the game
    game.play_game()

if __name__ == "__main__":
    main()
