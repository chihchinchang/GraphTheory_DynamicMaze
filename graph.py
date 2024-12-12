from collections import defaultdict, deque

class Graph:
    # Graph class for creation, editing, and analysis.

    def __init__(self, directed=False):
        # Initialize the graph (directed or undirected).
        self.graph = defaultdict(list)
        self.weights = {}  # Store edge weights
        self.directed = directed

        # Variables used for Tarjan's algorithm
        self.index = 0  # To track of the discovery time of each node
        self.stack = []  # Stack to keep nodes being explored
        self.on_stack = set()  # Set to track nodes currently in the stack
        self.sccs = []  # List to store SCC
        self.indices = {}  # Stores the discovery time (index) of each node
        self.low_link = {}  # Stores the low-link values of nodes


#-----------------------------Other functions on graphs to define:

    def add_node(self, node):
        #Add a node to the graph.
        if node not in self.graph:
            self.graph[node] = []
            print(f"Node '{node}' added.")
        else:
            print(f"Node '{node}' already exists.")


    def add_edge(self, node1, node2, weight=1):
        if node2 not in self.graph[node1]:  # Prevent duplicate edges
            self.graph[node1].append(node2)
            self.weights[(node1, node2)] = weight
            if not self.directed:
                self.graph[node2].append(node1)
                self.weights[(node2, node1)] = weight
            print(f"Edge added: {node1} --- {node2} (weight={weight})")


    def remove_edge(self, node1, node2):
        if node2 in self.graph[node1]:  # Only proceed if the edge exists
            self.graph[node1].remove(node2)
            del self.weights[(node1, node2)]
            if not self.directed:
                self.graph[node2].remove(node1)
                del self.weights[(node2, node1)]
            print(f"Edge removed: {node1} --- {node2}")


    def save_graph(self, filename):
        # Save the graph to a file.
        with open(filename, 'w') as file:
            for node, neighbors in self.graph.items():
                for neighbor in neighbors:
                    weight = self.weights.get((node, neighbor), 1)
                    file.write(f"{node} {neighbor} {weight}\n")
        print(f"Graph saved to {filename}")


    def load_graph(self, filename):
        # Load a graph from a file.
        with open(filename, 'r') as file:
            for line in file:
                node1, node2, weight = line.strip().split()
                self.add_edge(node1, node2, int(weight))
        print(f"Graph loaded from {filename}")


    def display_graph(self):
        # Display the graph.
        print("Graph Structure:")
        for node, neighbors in self.graph.items():
            print(f"{node}: {neighbors}")


#-----------------------------Basic graph metric:

    def node_degree(self, node):
        #Return the degree of a given node.
        if node in self.graph:
            return len(self.graph[node])
        else:
            return 0  # Node does not exist


    def graph_density(self):
        #Calculate the density of the graph."""
        num_edges = sum(len(neighbors) for neighbors in self.graph.values()) // 2  # For undirected graph
        num_nodes = len(self.graph)
        if num_nodes > 1:
            max_edges = num_nodes * (num_nodes - 1) / 2
            return num_edges / max_edges
        else:
            return 0  # No edges if there's only one node


#-----------------------------Path finding algo:

    def find_shortest_path(self, start, end):
        # Find the shortest path between two nodes (Dijkstra's algorithm).
        distances = {node: float('inf') for node in self.graph}
        distances[start] = 0
        previous_nodes = {node: None for node in self.graph}
        unvisited = set(self.graph)

        while unvisited:
            current = min(unvisited, key=lambda node: distances[node])
            unvisited.remove(current)

            if current == end:
                break

            for neighbor in self.graph[current]:
                weight = self.weights[(current, neighbor)]
                alternative_route = distances[current] + weight
                if alternative_route < distances[neighbor]:
                    distances[neighbor] = alternative_route
                    previous_nodes[neighbor] = current

        # Reconstruct path
        path, current = [], end
        while current:
            path.insert(0, current)
            current = previous_nodes[current]
        return path, distances[end]


    def all_paths(self, start, end, path=None):
        # Find all paths from 'start' point to 'end' point.
        if path is None:
            path = [start]
        if start == end:
            return [path]
        paths = []
        for neighbor in self.graph[start]:
            if neighbor not in path:
                new_paths = self.all_paths(neighbor, end, path + [neighbor])
                paths.extend(new_paths)
        return paths


# -----------------------------Graph traversal algo:

    def bfs(self, start, end):
        visited = []  # To track visited nodes
        queue = deque([start])  # Queue to explore nodes in BFS
        path = []

        while queue:
            node = queue.popleft()  # Take the first node from the queue
            if node not in visited:
                visited.append(node)
                path.append(node)

                if node == end:  # If we reached the end node, return the path
                    return path

                # Add unvisited neighbors to the queue
                for neighbor in self.graph[node]:
                    if neighbor not in visited:
                        queue.append(neighbor)

        return []  # Return empty if no path found


    def dfs(self, start, end, visited=None):
        if visited is None:
            visited = set()

        visited.add(start)

        if start == end:
            return [start]

        for neighbor in self.graph[start]:
            if neighbor not in visited:
                path = self.dfs(neighbor, end, visited)
                if path:
                    return [start] + path

        return []


    # -----------------------------Proper graph coloring:

    def graph_coloring(self):
        # Assign colors to nodes such that no two adjacent nodes share the same color.
        color = {}
        for node in self.graph:
            available_colors = {0, 1, 2, 3}  # For simplicity, just 4 colors
            for neighbor in self.graph[node]:
                if neighbor in color:
                    available_colors.discard(color[neighbor])
            color[node] = min(available_colors)  # Assign the smallest available color
        return color


# -----------------------------Computation of set of connected components of an undirected graph:

    def connected_components(self):
        # Find connected components using DFS.
        visited = set()
        components = []

        # Perform DFS from a node and collect all reachable nodes
        def dfs_cc(node, visited):
            # DFS to collect all nodes in the current connected component.
            visited.add(node)
            component = [node]
            for neighbor in self.graph[node]:
                if neighbor not in visited:
                    component += dfs_cc(neighbor, visited)  # Recursive call for unvisited neighbors
            return component

        # Iterate through all nodes in the graph
        for node in self.graph:
            if node not in visited:
                component = dfs_cc(node, visited)
                components.append(component)  # Add the component to the list

        return components


    # -----------------------------Computation of set of SCC of a directed graph:

    def tarjan_scc(self):
        # Find strongly connected components using Tarjan's algorithm.
        for node in self.graph:
            if node not in self.indices:
                self._strongconnect(node)
        return self.sccs

    def _strongconnect(self, node):
        # Helper function for DFS in Tarjan's Algorithm.
        # Set the discovery time and low-link value
        self.indices[node] = self.low_link[node] = self.index
        self.index += 1
        self.stack.append(node)
        self.on_stack.add(node)

        # Explore each neighbor
        for neighbor in self.graph[node]:
            if neighbor not in self.indices:  # If the neighbor hasn't been visited
                self._strongconnect(neighbor)
                # After the recursive call, we update the low-link value
                self.low_link[node] = min(self.low_link[node], self.low_link[neighbor])
            elif neighbor in self.on_stack:  # If the neighbor is in the current stack
                # Means the neighbor is part of the current SCC
                self.low_link[node] = min(self.low_link[node], self.indices[neighbor])

        # If node is a root (start point of an SCC)
        if self.low_link[node] == self.indices[node]:
            scc = []
            while True:
                w = self.stack.pop()
                self.on_stack.remove(w)
                scc.append(w)
                if w == node:
                    break
            self.sccs.append(scc)
