from typing import List, Tuple, Dict
import time
from EightPuzzleGame.Logic.puzzle_solver import PuzzleSolver
from EightPuzzleGame.Logic.utils import get_neighbors, is_solvable


class DFSPuzzleSolver(PuzzleSolver):
    def __init__(self, initial_state: int):
        """Initialize the DFS Puzzle Solver with the given initial state."""
        super().__init__(initial_state)

    def solve(self) -> None:
        """Solve the puzzle using the Depth-First Search (DFS) algorithm."""
        if not is_solvable(self.initial_state):
            self.reset_solver()
            return

        timer_started = time.perf_counter()
        stack_frontier: List[Tuple[int, int]] = [(self.initial_state, 0)]
        self.frontier_set.add(self.initial_state)
        child_parent_map: Dict[int, int] = {}
        self.explored_set = set()

        # DFS loop
        while stack_frontier:
            state, depth = stack_frontier.pop()
            self.frontier_set.remove(state)
            self.explored_set.add(state)
            self.num_nodes += 1
            self.max_search_depth = max(self.max_search_depth, depth)

            if state == self.goal_state:
                self.solution_path = self.get_path(child_parent_map, state)
                self.cost = depth
                break

            self.expand_state(state, stack_frontier, depth, child_parent_map)

        self.run_time = time.perf_counter() - timer_started

    def reset_solver(self) -> None:
        """Reset solver attributes if the puzzle is determined to be unsolvable."""
        self.num_nodes = 0
        self.solution_path = []
        self.max_search_depth = 0
        self.run_time = 0
        self.cost = 0

    def expand_state(self, state: int, stack: List[Tuple[int, int]],
                     current_depth: int, child_parent_map: Dict[int, int]) -> None:
        """Expand the current state by finding its valid neighbors and add them to the stack."""
        for neighbor in get_neighbors(state):
            # Check if the neighbor is already in explored_set or stack_frontier
            if neighbor not in self.explored_set and not any(neighbor == s[0] for s in stack):
                # if neighbor not in self.explored_set and neighbor not in self.frontier_set:
                stack.append((neighbor, current_depth + 1))
                self.frontier_set.add(neighbor)
                child_parent_map[neighbor] = state

    def get_path(self, child_parent_map: Dict[int, int], goal_state: int) -> List[int]:
        """Reconstruct the solution path from the goal state back to the initial state."""
        path = []
        current_state = goal_state

        while current_state in child_parent_map:
            path.append(current_state)
            current_state = child_parent_map[current_state]

        path.append(self.initial_state)
        path.reverse()

        return path

    def get_number_of_nodes(self) -> int:
        """Return the total number of nodes explored during the search."""
        return self.num_nodes

    def get_depth(self) -> int:
        """Return the maximum search depth reached during the exploration."""
        return self.max_search_depth

    def get_runtime(self) -> float:
        """Return the total runtime of the solution process."""
        return self.run_time

    def get_steps(self) -> List[int]:
        """Return the sequence of steps taken to solve the puzzle."""
        return self.solution_path

    def get_cost(self) -> int:
        """Return the cost (depth) of the solution path."""
        return self.cost
