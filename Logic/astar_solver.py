import time
import heapq
from math import ceil
from typing import Callable, Dict
from Logic.puzzle_solver import PuzzleSolver
from Logic.utils import *

class AStarPuzzleSolver(PuzzleSolver):
    def __init__(self, initial_state: int, heuristic: Callable[[int], float]):
        # Initialize the A* Puzzle Solver with the given initial state
        super().__init__(initial_state)
        self.start_time = 0  # Start time of the search
        self.heuristic = heuristic
        self.current_cost = 0
        self.map_of_costs = {}
        self.g_cost = {}

    def solve(self):
        """Solve the puzzle using the A* algorithm."""
        if not is_solvable(self.initial_state):
            self.reset_solver()
            return
        
        timer_started = time.perf_counter()
        self.current_cost = self.heuristic(self.initial_state) + self.cost
        heap = [(self.current_cost, self.initial_state)]
        self.frontier_set.add(self.initial_state)
        self.map_of_costs[self.initial_state] = self.current_cost
        child_parent_map: Dict[int, int] = {}
        self.g_cost[self.initial_state] = self.cost

        while len(heap) != 0:
            state_cost, state = heapq.heappop(heap)
            self.frontier_set.remove(state)
            self.explored_set.add(state)
            self.max_search_depth = max(self.max_search_depth, self.g_cost[state])

            if state == self.goal_state:
                self.solution_path = self.get_path(child_parent_map, state)
                self.cost = len(self.solution_path)-1
                self.num_nodes = len(self.explored_set)
                break

            self.expand_state(state, heap, self.g_cost[state], child_parent_map)

        self.run_time = time.perf_counter() - timer_started

    def reset_solver(self) -> None:
        """Reset solver attributes if the puzzle is determined to be unsolvable."""
        self.num_nodes = 0
        self.solution_path = []
        self.max_search_depth = 0
        self.run_time = 0
        self.cost = 0

    def expand_state(self, state: int, heap: List[tuple[float, int]],
                     current_depth: int,child_parent_map: Dict[int, int]) -> None:
        """Expand the current state by finding its valid neighbors and add them to the heap."""
        for neighbor in get_neighbors(state):
            self.g_cost[neighbor] = current_depth + 1
            new_cost = current_depth + 1 + self.heuristic(neighbor)
            # Check if the neighbor is already in explored_set or frontier
            if neighbor not in self.explored_set and neighbor not in self.frontier_set:
                self.frontier_set.add(neighbor)
                heapq.heappush(heap, (new_cost, neighbor))
                child_parent_map[neighbor] = state
                self.map_of_costs[neighbor] = new_cost
            elif neighbor in self.frontier_set:
                temp = self.map_of_costs[neighbor]
                if new_cost < temp:
                    heap = [(cost, state) for cost, state in heap if state != neighbor]
                    self.map_of_costs[neighbor] = new_cost
                    heapq.heappush(heap, (new_cost, neighbor))
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

    def get_steps(self) -> list[int]:
        """Return the sequence of steps taken to solve the puzzle."""
        return self.solution_path

    def get_cost(self) -> int:
        """Return the cost of steps taken to solve the puzzle."""
        return int(self.cost)

