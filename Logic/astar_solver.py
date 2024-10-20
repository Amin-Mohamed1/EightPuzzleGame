from typing import List, Callable, Tuple, Dict
from EightPuzzleGame.Logic.puzzle_solver import PuzzleSolver


class AStarPuzzleSolver(PuzzleSolver):
    def __init__(self, initial_state: List[List[int]], heuristic: Callable[[List[List[int]]], float]):
        super().__init__(initial_state)
        self.heuristic = heuristic

    def solve(self):
        pass

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

