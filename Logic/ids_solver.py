from typing import List, Tuple, Dict
import time
from EightPuzzleGame.Logic.puzzle_solver import PuzzleSolver
from EightPuzzleGame.Logic.utils import get_neighbors, is_solvable


class IDSPuzzleSolver(PuzzleSolver):
    def __init__(self, initial_state: List[List[int]]):
        """Initialize the IDS Puzzle Solver with the given initial state."""
        super().__init__(initial_state)

    def solve(self) -> None:
        """Solve the puzzle using Iterative Deepening Search (IDS) algorithm."""
        if not is_solvable(self.initial_state):
            self.reset_solver()
            return

        timer_started = time.perf_counter()
        self.visited_set = set()
        self.explored_set = set()
        depth_limit = 0

        while True:
            result = self.depth_limited_search(depth_limit)
            if result:
                break
            depth_limit += 1

        self.run_time = time.perf_counter() - timer_started

    def depth_limited_search(self, depth_limit: int):
        """Perform depth-limited search up to the given depth limit."""
        stack_frontier = [(self.initial_state, 0)]
        child_parent_map = {}
        self.visited_set = set()
        self.explored_set = set()
        self.visited_set.add(tuple(map(tuple, self.initial_state)))

        # DFS loop
        while stack_frontier:
            state, depth = stack_frontier.pop()
            if state == self.goal_state:
                self.solution_path = self.get_path(child_parent_map, state)
                self.cost = depth
                return self.solution_path, depth

            if depth <= depth_limit:
                state_tuple = tuple(map(tuple, state))
                self.num_nodes += 1
                self.explored_set.add(state_tuple)
                self.max_search_depth = max(self.max_search_depth, depth)
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
        for neighbor in get_neighbors(state):
            neighbor_tuple = tuple(map(tuple, neighbor))

            if neighbor_tuple not in self.visited_set:
                stack.append((neighbor, current_depth + 1))
                child_parent_map[neighbor_tuple] = state
                self.visited_set.add(neighbor_tuple)

    def get_path(self, child_parent_map: Dict, goal_state: List[List[int]]) -> List[List[List[int]]]:
        """Reconstruct the solution path from the goal state back to the initial state."""
        path = []
        current_state = tuple(map(tuple, goal_state))
        while current_state in child_parent_map:
            path.append(current_state)
            current_state = tuple(map(tuple, child_parent_map[current_state]))

        path.append(tuple(map(tuple, self.initial_state)))
        path.reverse()
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

    def get_cost(self) -> int:
        """Return the cost of steps taken to solve the puzzle."""
        return self.cost
