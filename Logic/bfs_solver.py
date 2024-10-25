import time

from EightPuzzleGame.Logic.puzzle_solver import PuzzleSolver
from typing import List
from EightPuzzleGame.Logic.utils import is_solvable


class BFSPuzzleSolver(PuzzleSolver):
    def __init__(self, initial_state: int):
        # Initialize the BFS Puzzle Solver with the given initial state
        super().__init__(initial_state)
        self.queue = []  # Initialize an empty queue
        self.parent_map = {}  # To store the parent of each state
        self.start_time = 0  # Start time of the search

    def solve(self) -> None:
        if not is_solvable(self.initial_state):
            self.reset_solver()
            return

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

    def get_steps(self) -> List[int]:
        return self.solution_path

    def get_cost(self) -> int:
        return self.cost

    def __is_solved(self, state: int) -> bool:
        return state == self.goal_state

    def __get_empty_tile_position(self, state: int) -> int:
        flat_state = [int(digit) for digit in str(state).zfill(9)]
        for i in range(9):
            if flat_state[i] == 0:
                return i
        return -1

    def __get_neighbors(self, state: int) -> list[int]:
        empty_tile_position = self.__get_empty_tile_position(state)
        directions = [1, -1, 3, -3]
        neighbors = []
        for direction in directions:
            new_position = empty_tile_position + direction
            if 0 <= new_position < 9:
                neighbors.append(self.__swap_tiles(state, empty_tile_position, new_position))
        return neighbors

    def __swap_tiles(self, state: int, source: int, destination: int) -> int:
        flat_state = [int(digit) for digit in str(state).zfill(9)]
        flat_state[source], flat_state[destination] = flat_state[destination], flat_state[source]
        return int("".join([str(digit) for digit in flat_state]))

    def __generate_solution_path(self, current_state: int):
        while current_state:
            self.solution_path.insert(0, current_state)
            current_state = self.parent_map[current_state]

    def __generate_neighbor_states(self, queue_size: int) -> bool:
        for _ in range(queue_size):
            current_state = self.queue.pop(0)  # Dequeue the first element from the queue
            self.num_nodes += 1
            neighbor_states = self.__get_neighbors(current_state)
            for neighbor_states in neighbor_states:
                if neighbor_states not in self.explored_set:
                    self.explored_set.add(neighbor_states)
                    self.parent_map[neighbor_states] = current_state
                    if self.__is_solved(neighbor_states):
                        self.run_time = time.perf_counter() - self.start_time
                        self.__generate_solution_path(neighbor_states)
                        self.num_nodes += 1  # Include the goal state in the explored nodes
                        return True
                    self.queue.append(neighbor_states)
        return False

    def __bfs(self) -> bool:
        self.parent_map = {self.initial_state: None}  # To store the parent of each state
        self.queue = [self.initial_state]  # Initialize an empty queue
        self.start_time = time.perf_counter()  # Start the timer
        self.explored_set.add(self.initial_state)
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

    # def __is_solvable(self, state: int) -> bool:
    #     digits = [int(digit) for digit in str(state).zfill(9)]
    #     state_2d = [digits[i:i + 3] for i in range(0, 9, 3)]
    #     inversions_count = 0
    #     # right and down check
    #     for i in range(3):
    #         for j in range(2):
    #             for k in range(j + 1, 3):
    #                 if state_2d[i][j] > state_2d[i][k]:
    #                     inversions_count += 1
    #                 if state_2d[j][i] > state_2d[k][i]:
    #                     inversions_count += 1
    #     return inversions_count % 2 == 0
