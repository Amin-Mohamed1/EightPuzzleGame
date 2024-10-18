import time
from utils import *
from Logic.puzzle_solver import PuzzleSolver


class DFSPuzzleSolver(PuzzleSolver):
    def __init__(self, initial_state: List[List[int]]):
        """Initialize the DFS Puzzle Solver with the given initial state."""
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
        """Solve the puzzle using the Depth-First Search (DFS) algorithm."""
        # Check if the puzzle is solvable
        if not self.is_solvable():
            reset_solver(self)
            return

        # Start the timer to measure the runtime of the solver
        timer_started = time.perf_counter()
        # Initialize stack frontier with the initial state and depth 0
        stack_frontier = [(self.initial_state, 0)]
        # Map to store the relationship between child and parent states
        child_parent_map = {}
        # Visited and explored states sets
        self.visited_set = set()
        self.explored_set = set()
        self.visited_set.add(tuple(map(tuple, self.initial_state)))

        # DFS loop
        while stack_frontier:
            state, depth = stack_frontier.pop()

            # Check if the current state is the goal state
            if state == self.goal_state:
                # Get the solution path
                self.solution_path = get_path(self, child_parent_map, state)
                self.cost = depth
                break

            state_tuple = tuple(map(tuple, state))
            # Increment the node count and add the state to the explored set
            self.num_nodes += 1
            self.explored_set.add(state_tuple)
            # Update the maximum depth reached
            self.max_search_depth = max(self.max_search_depth, depth)
            # Expand the current state and explore its neighbors
            expand_state(self, state, stack_frontier, depth, child_parent_map)

        # Calculate the total runtime of the solver
        self.run_time = time.perf_counter() - timer_started

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
