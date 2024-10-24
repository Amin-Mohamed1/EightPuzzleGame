from abc import ABC, abstractmethod
from typing import List


class PuzzleSolver(ABC):
    def __init__(self, initial_state: int):
        self.initial_state = initial_state
        self.goal_state = 12345678
        self.num_nodes = 0
        self.max_search_depth = 0
        self.run_time = 0
        self.solution_path = []
        self.explored_set = set()
        self.frontier_set = set()
        self.cost = 0

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
    def get_steps(self) -> List[int]:
        pass
