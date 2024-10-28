import time
from typing import Tuple, Dict, List
from Logic.puzzle_solver import PuzzleSolver
from Logic.utils import *


class IDSPuzzleSolver(PuzzleSolver):

    def __init__(self, game_initial_state: int):
        """Initialize the DFS Puzzle Solver with the given initial state."""
        super().__init__(game_initial_state)

    def solve(self) -> None:
        if not is_solvable(self.initial_state):
            self.reset_solver()
            return

        timer_started = time.perf_counter()
        depth_limit = 0
        self.num_nodes = 0
        self.max_search_depth = 0
        self.run_time = 0

        while True:
            self.frontier_set = set()
            self.explored_set = set()
            stack_frontier: List[Tuple[int, int]] = [(self.initial_state, 0)]
            self.frontier_set.add((self.initial_state, 0))
            child_parent_map: Dict[Tuple[int, int], Tuple[int, int]] = {(self.initial_state, 0): (-1, -1)}

            self.solution_path = self.depth_limited_search(depth_limit, stack_frontier, child_parent_map)
            if self.solution_path:
                self.run_time = time.perf_counter() - timer_started
                self.cost = len(self.solution_path) - 1
                self.max_search_depth = depth_limit
                return
            else:
                depth_limit += 1

    def depth_limited_search(self, depth_limit: int, stack_frontier: List[Tuple[int, int]],
                             child_parent_map: Dict[Tuple[int, int], Tuple[int, int]]) -> list[int]:
        while stack_frontier:
            state, depth = stack_frontier.pop()
            self.frontier_set.remove((state, depth))
            self.explored_set.add((state, depth))
            self.num_nodes += 1

            if state == self.goal_state:
                self.get_path(state, child_parent_map, depth)
                return self.solution_path

            if depth < depth_limit:
                self.expand_state(state, stack_frontier, depth, child_parent_map, depth_limit)
        return []

    def get_path(self, current_state: int, child_parent_map: Dict[Tuple[int, int], Tuple[int, int]], depth: int):
        state = (current_state, depth)
        while state != (-1, -1):
            self.solution_path.insert(0, state[0])
            state = child_parent_map[state]

    def expand_state(self, state: int, stack: List[Tuple[int, int]],
                     current_depth: int, child_parent_map: Dict[Tuple[int, int], Tuple[int, int]],
                     limit: int) -> None:
        """Expand the current state by finding its valid neighbors and add them to the stack."""
        for neighbor in get_neighbors(state):
            neighbor_with_depth = (neighbor, current_depth + 1)
            if (neighbor_with_depth not in self.explored_set) and (neighbor_with_depth not in self.frontier_set):
                # if neighbor_with_depth[1] < limit:
                stack.append((neighbor, current_depth + 1))
                self.frontier_set.add(neighbor_with_depth)
                child_parent_map[neighbor_with_depth] = (state, current_depth)

    def reset_solver(self) -> None:
        """Reset solver attributes if the puzzle is determined to be unsolvable."""
        self.num_nodes = 0
        self.solution_path = []
        self.max_search_depth = 0
        self.run_time = 0
        self.cost = 0

    def get_number_of_nodes(self) -> int:
        return self.num_nodes

    def get_cost(self) -> int:
        return self.cost

    def get_depth(self) -> int:
        return len(self.solution_path) - 1

    def get_runtime(self) -> float:
        return self.run_time

    def get_steps(self) -> List[int]:
        return self.solution_path
