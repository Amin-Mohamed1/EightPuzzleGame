import time

from EightPuzzleGame.Logic.puzzle_solver import PuzzleSolver
from typing import List


class BFSPuzzleSolver(PuzzleSolver):
    def __init__(self, initial_state: List[List[int]]):
        # Initialize the BFS Puzzle Solver with the given initial state
        super().__init__(initial_state)
        self.queue = []  # Initialize an empty queue
        self.parent_map = {}  # To store the parent of each state
        self.start_time = 0  # Start time of the search

    def solve(self) -> None:
        if self.__is_solved(self.initial_state):
            self.solution_path = [self.initial_state]
            return
        # Solve the puzzle using Breadth First Search
        if not self.__bfs():
            self.reset_solver()

    def get_number_of_nodes(self) -> int:
        return self.num_nodes

    def get_depth(self) -> int:
        return self.max_search_depth

    def get_runtime(self) -> float:
        return self.run_time

    def get_steps(self) -> List[List[List[int]]]:
        return self.solution_path

    def __is_solved(self, state: list[list[int]]) -> bool:
        return state == self.goal_state

    def __get_empty_tile_position(self, state: list[list[int]]) -> tuple[int, int]:
        for i in range(3):
            for j in range(3):
                if state[i][j] == 0:
                    return i, j
        return -1, -1  # Default return value (should not happen if valid input is provided)

    def __swap_tiles(self, state: list[list[int]], x1: int, y1: int, x2: int, y2: int) -> list[list[int]]:
        new_state = [row[:] for row in state]
        new_state[x1][y1], new_state[x2][y2] = new_state[x2][y2], new_state[x1][y1]
        return new_state

    def __convert_to_tuple_of_tuples(self, state: list[list[int]]):
        return tuple([tuple(row) for row in state])

    def __generate_solution_path(self, current_state: list[list[int]]):
        state = self.__convert_to_tuple_of_tuples(current_state)
        while state:
            self.solution_path.insert(0, [list(row) for row in state])
            state = self.parent_map[state]

    def __generate_neighbor_states(self, queue_size: int) -> bool:
        for _ in range(queue_size):
            current_state = self.queue.pop(0)  # Dequeue the first element from the queue
            x1, y1 = self.__get_empty_tile_position(current_state)
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            for direction in directions:
                x2, y2 = x1 + direction[0], y1 + direction[1]
                if 0 <= x2 < 3 and 0 <= y2 < 3:
                    new_state = self.__swap_tiles(current_state, x1, y1, x2, y2)
                    if self.__convert_to_tuple_of_tuples(new_state) not in self.visited_set:
                        self.num_nodes += 1
                        self.visited_set.add(self.__convert_to_tuple_of_tuples(new_state))
                        self.parent_map[self.__convert_to_tuple_of_tuples(new_state)] = self.__convert_to_tuple_of_tuples(current_state)
                        self.queue.append(new_state)
                        if self.__is_solved(new_state):
                            self.run_time = time.perf_counter() - self.start_time
                            self.__generate_solution_path(new_state)
                            return True
        return False

    def __bfs(self) -> bool:
        self.parent_map = {self.__convert_to_tuple_of_tuples(self.initial_state): None}  # To store the parent of
        # each state
        self.queue = [self.initial_state]  # Initialize an empty queue
        self.start_time = time.perf_counter()  # Start the timer
        self.visited_set.add(self.__convert_to_tuple_of_tuples(self.initial_state))
        while self.queue:
            queue_size = len(self.queue)
            self.max_search_depth += 1
            self.cost += 1
            if self.__generate_neighbor_states(queue_size):
                return True
        return False

    def reset_solver(self) -> None:
        """Reset solver attributes if the puzzle is determined to be unsolvable."""
        self.num_nodes = 0
        self.solution_path = []
        self.max_search_depth = 0
        self.run_time = 0
        self.cost = 0

    def get_cost(self) -> int:
        return self.cost

