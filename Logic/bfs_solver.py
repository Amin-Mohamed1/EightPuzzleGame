from Logic.puzzle_solver import PuzzleSolver
from typing import List


class BFSPuzzleSolver(PuzzleSolver):
    def __init__(self, initial_state: List[List[int]]):
        # Initialize the BFS Puzzle Solver with the given initial state
        super().__init__(initial_state)

    def solve(self) -> None:
        return

    def get_number_of_nodes(self) -> int:
        return 0

    def get_depth(self) -> int:
        return 0

    def get_runtime(self) -> float:
        return 0

    def get_steps(self) -> List[List[List[int]]]:
        return []
