from abc import ABC, abstractmethod
from typing import List


class PuzzleSolver(ABC):
    def __init__(self, initial_state: List[List[int]]):
        self.initial_state = initial_state
        self.goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
        self.num_nodes = 0  # Total number of nodes expanded
        self.max_search_depth = 0  # Maximum depth reached during the search
        self.run_time = 0  # Total runtime
        self.solution_path = []  # Path from initial state to goal state

    @abstractmethod
    def solve(self) -> None:
        pass

    @abstractmethod
    def get_number_of_nodes(self) -> int:
        pass

    @abstractmethod
    def get_depth(self) -> int:
        pass

    @abstractmethod
    def get_runtime(self) -> float:
        pass

    @abstractmethod
    def get_steps(self) -> List[List[List[int]]]:
        pass
