import random
from graph import Graph

class MazeGame:
    # Dynamic maze (labyrinth) game logic.

    def __init__(self):
        self.graph = Graph(directed=False)
        self.start = None
        self.end = None
        self.powers = {'view_graph': 3, 'block_dynamics': 1, 'teleport': 1}  # Player powers
        self.show_graph_turns = 0  # Counter for "view graph for 3 turns"


    def setup_game(self, nodes, edges, start, end):
        # Set up the maze with nodes, edges, start, and end.
        for node in nodes:
            self.graph.add_node(node)
        for edge in edges:
            self.graph.add_edge(*edge)
        self.start = start
        self.end = end


    def apply_dynamics(self, block_dynamics=False):
        # Ensure at least one edge is added and one edge is removed per turn, while keeping the graph connected.
        if block_dynamics:
            print("Graph dynamics blocked this turn!")
            return

        nodes = list(self.graph.graph.keys())

        # Ensure adding a new edge
        if len(nodes) > 1:
            added = False
            for _ in range(10):  # Try up to 10 times to find a valid pair
                node1, node2 = random.sample(nodes, 2)
                if node2 not in self.graph.graph[node1]:  # Only add if no edge exists
                    self.graph.add_edge(node1, node2, random.randint(1, 10))
                    added = True
                    break
            if not added:
                print("No valid edge to add this turn.")

        # Ensure removing an edge while keeping the graph connected
        if len(nodes) > 1:
            removed = False
            for _ in range(10):  # Try up to 10 times to find a valid edge
                node1, node2 = random.sample(nodes, 2)
                if node2 in self.graph.graph[node1]:  # Only remove if edge exists
                    self.graph.remove_edge(node1, node2)

                    # Check if the graph is still connected
                    components = self.graph.connected_components()
                    if len(components) == 1:  # Graph is still connected
                        removed = True
                        break
                    else:  # Graph would be disconnected, re-add the edge
                        self.graph.add_edge(node1, node2, random.randint(1, 10))

            if not removed:
                print("No valid edge to remove this turn.")


    def use_power(self):
        # Allow the player to use a power.
        print("Available powers:")
        print(f"1. View graph structure for the next 3 turns ({self.powers['view_graph']} left)")
        print(f"2. Block graph dynamics for one turn ({self.powers['block_dynamics']} left)")
        print(f"3. Teleport to an unconnected node ({self.powers['teleport']} left)")
        choice = input("Choose a power (1/2/3 or press Enter to skip): ")

        if choice == '1' and self.powers['view_graph'] > 0:
            self.show_graph_turns = 3
            self.powers['view_graph'] -= 1
            print("You can now view the graph structure for the next 3 turns!")
            return 'view_graph'
        elif choice == '2' and self.powers['block_dynamics'] > 0:
            self.powers['block_dynamics'] -= 1
            print("You have blocked graph dynamics for the next turn!")
            return 'block_dynamics'
        elif choice == '3' and self.powers['teleport'] > 0:
            self.powers['teleport'] -= 1
            return 'teleport'
        elif choice == '':
            print("You chose to skip using a power.")
        else:
            print("Invalid choice or no powers left for this option!")
        return None


    def teleport(self, current_position):
        # Teleport the player to an unconnected node.
        # Get the unconnected nodes excluding the current and end positions
        unconnected_nodes = [node for node in self.graph.graph if
                             node != current_position and node != self.end and node not in self.graph.graph[current_position]]

        if unconnected_nodes:
            print(f"Available nodes to teleport to: {unconnected_nodes}")
            target = input(f"Choose a node to teleport to {unconnected_nodes}: ")
            if target in unconnected_nodes:
                print(f"Teleported to {target}")
                return target  # Return the new position
            else:
                print("Invalid teleport target!")
        else:
            print("No unconnected nodes available to teleport to!")

        return current_position  # Return the current position if teleport fails


    def play_game(self):
        # Play the maze game.
        current_position = self.start
        print(f"Start: {self.start}, Goal: {self.end}")

        while current_position != self.end:

            print(f"Current position: {current_position}")

            # Allow the player to use a power
            power_action = self.use_power()

            # Handle teleportation
            if power_action == 'teleport':  # Check if the player chose teleportation
                current_position = self.teleport(current_position)  # Pass the current position to teleport
                print(f"After teleporting, current position is: {current_position}")  # Debugging print

                if current_position == self.end:  # Check if teleportation brings the player to the goal
                    print("You reached the goal!")
                    break  # Exit the game loop if the player reaches the goal via teleportation

            # Apply graph dynamics unless blocked by power
            self.apply_dynamics(block_dynamics=(power_action == 'block_dynamics'))

            # Show the updated graph structure after dynamics (if viewing power is still active)
            if self.show_graph_turns > 0 and self.powers['view_graph'] > 0:
                self.graph.display_graph()
                self.show_graph_turns -= 1

            # Check if player reached the goal after the move
            if current_position == self.end:
                print("You reached the goal!")
                break  # Exit the loop if the player has reached the goal

            # Player chooses a move
            move = input(f"Choose your next node from {self.graph.graph[current_position]}: ")
            if move in self.graph.graph[current_position]:  # Valid move to an adjacent node
                current_position = move  # Update current position
                print(f"Moved to {current_position}")
            else:
                print("Invalid move!")

        print("Game finished!")  # Message after reaching the goal
