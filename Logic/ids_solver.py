import time
from typing import List, Tuple, Dict
from EightPuzzleGame.Logic.puzzle_solver import PuzzleSolver


class IDSPuzzleSolver(PuzzleSolver):
    def __init__(self, initial_state: List[List[int]]):
        """Initialize the IDS Puzzle Solver with the given initial state."""
        super().__init__(initial_state)

    def count_inversions(self) -> int:
        """ Count the number of inversions in the puzzle state. """
        # Flatten the puzzle state, excluding the empty tile (0)
        flat_state = [tile for row in self.initial_state for tile in row if tile != 0]
        # Count the number of inversions
        inversions = sum(1 for i in range(len(flat_state))
                         for j in range(i + 1, len(flat_state))
                         if flat_state[i] > flat_state[j])
        return inversions

    def is_solvable(self) -> bool:
        """Check if the 8-puzzle is solvable based on the number of inversions.
        The puzzle is solvable if the number of inversions is even.
        """
        return self.count_inversions() % 2 == 0

    def solve(self) -> None:
        """Solve the puzzle using Iterative Deepening Search (IDS) algorithm."""
        # Check if the puzzle is solvable
        if not self.is_solvable():
            self.reset_solver()
            return

        # Start the timer to measure the runtime of the solver
        timer_started = time.perf_counter()
        # Initialize visited and explored sets
        self.visited_set = set()
        self.explored_set = set()

        depth_limit = 0  # Start with a depth limit of 0

        # Perform iterative deepening until a solution is found
        while True:
            result = self.depth_limited_search(depth_limit)
            if result:  # If a solution is found, exit the loop
                break
            depth_limit += 1  # Increase the depth limit for the next iteration

        # Calculate the total runtime of the solver
        self.run_time = time.perf_counter() - timer_started

    def depth_limited_search(self, depth_limit: int):
        """Perform depth-limited search up to the given depth limit."""
        # Initialize stack frontier with the initial state and depth 0
        stack_frontier = [(self.initial_state, 0)]
        # Map to store the relationship between child and parent states
        child_parent_map = {}
        # Clear visited and explored sets for the current depth level
        self.visited_set = set()
        self.explored_set = set()
        # Mark the initial state as visited
        self.visited_set.add(tuple(map(tuple, self.initial_state)))

        # DFS-like loop with depth limit
        while stack_frontier:
            state, depth = stack_frontier.pop()

            # Check if the current state is the goal state
            if state == self.goal_state:
                # Construct the solution path
                self.solution_path = self.get_path(child_parent_map, state)
                self.cost = depth
                return self.solution_path, depth

            # Only expand nodes that are within the current depth limit
            if depth <= depth_limit:
                state_tuple = tuple(map(tuple, state))
                # Increment the node count and add the state to the explored set
                self.num_nodes += 1
                self.explored_set.add(state_tuple)
                # Update the maximum depth reached
                self.max_search_depth = max(self.max_search_depth, depth)
                # Expand the current state and explore its neighbors
                self.expand_state(state, stack_frontier, depth, child_parent_map)

    def reset_solver(self) -> None:
        """Reset solver attributes if the puzzle is determined to be unsolvable."""
        self.num_nodes = 0
        self.solution_path = []
        self.max_search_depth = 0
        self.run_time = 0
        self.cost = 0

    def expand_state(self, state: List[List[int]], stack: List[Tuple[List[List[int]], int]],
                     current_depth: int, child_parent_map: Dict) -> None:
        """Expand the current state by finding its valid neighbors and add them to the stack."""
        for neighbor in self.get_neighbors(state):
            neighbor_tuple = tuple(map(tuple, neighbor))

            # Only add neighbor states that have not been visited or explored
            if neighbor_tuple not in self.visited_set and neighbor_tuple not in self.explored_set:
                stack.append((neighbor, current_depth + 1))  # Increase depth
                child_parent_map[neighbor_tuple] = state  # Record the parent-child relationship
                self.visited_set.add(neighbor_tuple)  # Mark the neighbor as visited

    def get_neighbors(self, state: List[List[int]]) -> List[List[List[int]]]:
        """Generate valid neighbor states by moving the empty tile (0)."""
        neighbors = []
        zero_pos = self.find_empty_tile(state)  # Locate the position of the empty tile (0)
        directions = [(-1, 0), (1, 0), (0, 1), (0, -1)]  # Define movement directions (up, down, right, left)

        # Try moving the empty tile in each direction and generate new states
        for direction in directions:
            new_zero_pos = (zero_pos[0] + direction[0], zero_pos[1] + direction[1])
            if self.is_within_bounds(new_zero_pos):
                new_state = self.swap(state, zero_pos, new_zero_pos)
                neighbors.append(new_state)

        return neighbors

    def find_empty_tile(self, state: List[List[int]]) -> Tuple[int, int]:
        """Find the position of the empty tile (represented by 0) in the puzzle."""
        for i in range(len(state)):
            for j in range(len(state[i])):
                if state[i][j] == 0:
                    return i, j
        return -1, -1  # Default return value (should not happen if valid input is provided)

    def is_within_bounds(self, position: Tuple[int, int]) -> bool:
        """Check if the given position is within the 3x3 puzzle boundaries."""
        return (0 <= position[0] < 3 and
                0 <= position[1] < 3)

    def swap(self, state: List[List[int]], parent: Tuple[int, int], child: Tuple[int, int]) -> List[List[int]]:
        """Swap the positions of two tiles and return the new state."""
        new_state = [row[:] for row in state]  # Create a copy of the current state
        # Swap the positions of the parent (empty tile) and child (tile to move)
        new_state[parent[0]][parent[1]], new_state[child[0]][child[1]] = (
            new_state[child[0]][child[1]], new_state[parent[0]][parent[1]])
        return new_state

    def get_path(self, child_parent_map: Dict, goal_state: List[List[int]]) -> List[List[List[int]]]:
        """Reconstruct the solution path from the goal state back to the initial state."""
        path = []
        current_state = tuple(map(tuple, goal_state))

        # Trace back from the goal state to the initial state using the child-parent map
        while current_state in child_parent_map:
            path.append(current_state)
            current_state = tuple(map(tuple, child_parent_map[current_state]))

        # Add the initial state and reverse the path to get the correct order
        path.append(tuple(map(tuple, self.initial_state)))
        path.reverse()

        # Convert tuples back to lists for consistency
        return [list(map(list, state)) for state in path]

    def get_number_of_nodes(self) -> int:
        """Return the total number of nodes explored during the search."""
        return self.num_nodes

    def get_depth(self) -> int:
        """Return the maximum search depth reached during the exploration."""
        return self.max_search_depth

    def get_runtime(self) -> float:
        """Return the total runtime of the solution process."""
        return self.run_time

    def get_steps(self) -> List[List[List[int]]]:
        """Return the sequence of steps taken to solve the puzzle."""
        return self.solution_path

    def get_visited(self) -> set:
        """Return the set of all states that have been visited."""
        return self.visited_set

    def get_explored(self) -> set:
        """Return the set of all states that have been explored."""
        return self.explored_set
