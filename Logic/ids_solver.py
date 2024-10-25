from typing import List, Tuple, Dict
import time
from EightPuzzleGame.Logic.utils import *
from EightPuzzleGame.Logic.puzzle_solver import PuzzleSolver


class IDSPuzzleSolver(PuzzleSolver):

    def __init__(self, initial_state: int):
        """Initialize the DFS Puzzle Solver with the given initial state."""
        super().__init__(initial_state)

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
            self.frontier_set.add(self.initial_state)
            child_parent_map: Dict[int, int] = {}

            self.solution_path = self.depth_limited_search(depth_limit, stack_frontier, child_parent_map)
            if len(self.solution_path) != 0:
                # print(depth_limit)
                self.run_time = time.perf_counter() - timer_started
                self.cost = len(self.solution_path) - 1
                self.max_search_depth = len(self.solution_path) - 1
                return
            else:
                depth_limit += 1

    def depth_limited_search(self, depth_limit: int, stack_frontier: List[Tuple[int, int]],
                             child_parent_map: Dict[int, int]) -> list[int]:
        while stack_frontier:
            state, depth = stack_frontier.pop()
            self.frontier_set.remove(state)
            self.explored_set.add(state)
            self.num_nodes += 1

            if state == self.goal_state:
                self.solution_path = self.get_path(child_parent_map, state)
                return self.solution_path

            if depth < depth_limit:
                self.expand_state(state, stack_frontier, depth, child_parent_map)

        return self.solution_path

    def get_path(self, child_parent_map: Dict[int, int], goal_state: int) -> List[int]:
        """Reconstruct the solution path from the goal state back to the initial state."""
        path = []
        current_state = 12345678

        while current_state in child_parent_map:
            path.append(current_state)
            current_state = child_parent_map[current_state]

        path.append(self.initial_state)
        path.reverse()

        return path

    def expand_state(self, state: int, stack: List[Tuple[int, int]],
                     current_depth: int, child_parent_map: Dict[int, int]) -> None:
        """Expand the current state by finding its valid neighbors and add them to the stack."""
        for neighbor in get_neighbors(state):
            # Check if the neighbor is already in explored_set or stack_frontier
            # if neighbor not in self.explored_set and not any(neighbor == s[0] for s in stack):
            if neighbor not in self.explored_set and neighbor not in self.frontier_set:
                stack.append((neighbor, current_depth + 1))
                self.frontier_set.add(neighbor)
                child_parent_map[neighbor] = state

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

#
# def main():
#     initial_state = 725310648
#     goal_state = 12345678
#
#     solver = IDSPuzzleSolver(initial_state)
#     solver.solve()
#     if solver.solution_path:
#         print("Solution path:")
#         for state in solver.solution_path:
#             state_str = str(state).zfill(9)
#             print(f"{state_str[0]} {state_str[1]} {state_str[2]}")
#             print(f"{state_str[3]} {state_str[4]} {state_str[5]}")
#             print(f"{state_str[6]} {state_str[7]} {state_str[8]}")
#             print()
#
#         print(f"Total cost (number of moves): {len(solver.solution_path) - 1}")
#         print(f"Maximum depth reached: {len(solver.solution_path) - 1}")
#         print(f"Number of nodes expanded: {solver.get_number_of_nodes()}")
#         print(f"Run time: {solver.get_runtime()} seconds")
#     else:
#         print("No solution found.")
#
#
# if __name__ == "__main__":
#     main()
