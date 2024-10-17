import time
from typing import List, Tuple, Dict
from Logic.puzzle_solver import PuzzleSolver


class DFSPuzzleSolver(PuzzleSolver):
    def __init__(self, initial_state: List[List[int]]):
        """Initialize the DFS Puzzle Solver with the given initial state."""
        super().__init__(initial_state)

    def count_inversions(self) -> int:
        """Count inversions in the puzzle state."""
        flat_state = [tile for row in self.initial_state for tile in row if tile != 0]
        inversions = sum(1 for i in range(len(flat_state))
                         for j in range(i + 1, len(flat_state))
                         if flat_state[i] > flat_state[j])
        return inversions

    def is_solvable(self) -> bool:
        """Check if the 8-puzzle is solvable."""
        return self.count_inversions() % 2 == 0

    def solve(self) -> None:
        """Solve the puzzle using Depth-First Search (DFS) algorithm."""
        if not self.is_solvable():
            self.reset_solver()
            return

        timer_started = time.perf_counter()
        stack_frontier = [(self.initial_state, 0)]
        child_parent_map = {}
        self.visited_set = set()
        self.explored_set = set()
        self.visited_set.add(tuple(map(tuple, self.initial_state)))

        while stack_frontier:
            state, depth = stack_frontier.pop()

            if state == self.goal_state:
                self.solution_path = self.get_path(child_parent_map, state)
                self.cost = depth
                break

            state_tuple = tuple(map(tuple, state))
            self.num_nodes += 1
            self.explored_set.add(state_tuple)
            self.max_search_depth = max(self.max_search_depth, depth)
            self.expand_state(state, stack_frontier, depth, child_parent_map)

        self.run_time = time.perf_counter() - timer_started

    def reset_solver(self) -> None:
        """Reset solver attributes when the puzzle is not solvable."""
        self.num_nodes = 0
        self.solution_path = []
        self.max_search_depth = 0
        self.run_time = 0
        self.cost = 0

    def expand_state(self, state: List[List[int]], stack: List[Tuple[List[List[int]], int]],
                     current_depth: int, child_parent_map: Dict) -> None:
        """Expand the current state and add its neighbors to the stack."""
        for neighbor in self.get_neighbors(state):
            neighbor_tuple = tuple(map(tuple, neighbor))

            if neighbor_tuple not in self.visited_set and neighbor_tuple not in self.explored_set:
                stack.append((neighbor, current_depth + 1))
                child_parent_map[neighbor_tuple] = state
                self.visited_set.add(neighbor_tuple)

    def get_neighbors(self, state: List[List[int]]) -> List[List[List[int]]]:
        """Get valid neighbor states by moving the empty tile."""
        # print("Current State")
        # print(state)
        neighbors = []
        zero_pos = self.find_empty_tile(state)
        directions = [(-1, 0), (1, 0), (0, 1), (0, -1)]
        for direction in directions:
            new_zero_pos = (zero_pos[0] + direction[0], zero_pos[1] + direction[1])
            if self.is_within_bounds(new_zero_pos):
                new_state = self.swap(state, zero_pos, new_zero_pos)
                # print(new_state)
                neighbors.append(new_state)
        return neighbors

    def find_empty_tile(self, state: List[List[int]]) -> Tuple[int, int]:
        """Find the position of the empty tile (represented by 0)."""
        for i in range(len(state)):
            for j in range(len(state[i])):
                if state[i][j] == 0:
                    return i, j
        return -1, -1

    def is_within_bounds(self, position: Tuple[int, int]) -> bool:
        """Check if the position is within the bounds of the puzzle."""
        return (0 <= position[0] < 3 and
                0 <= position[1] < 3)

    def swap(self, state: List[List[int]], parent: Tuple[int, int], child: Tuple[int, int]) -> List[List[int]]:
        """Swap two tiles in the state and return the new state."""
        new_state = [row[:] for row in state]
        new_state[parent[0]][parent[1]], new_state[child[0]][child[1]] = (
            new_state[child[0]][child[1]], new_state[parent[0]][parent[1]])
        return new_state

    def get_path(self, child_parent_map: Dict, goal_state: List[List[int]]) -> List[List[List[int]]]:
        """Construct the solution path from the goal state to the initial state."""
        path = []
        current_state = tuple(map(tuple, goal_state))

        while current_state in child_parent_map:
            path.append(current_state)
            current_state = tuple(map(tuple, child_parent_map[current_state]))

        path.append(tuple(map(tuple, self.initial_state)))
        path.reverse()

        return [list(map(list, state)) for state in path]

    # Getters for attributes
    def get_number_of_nodes(self) -> int:
        """Return the number of nodes explored during the search."""
        return self.num_nodes

    def get_depth(self) -> int:
        """Return the maximum depth reached during the search."""
        return self.max_search_depth

    def get_runtime(self) -> float:
        """Return the runtime of the solution process."""
        return self.run_time

    def get_steps(self) -> List[List[List[int]]]:
        """Return the steps taken to reach the solution."""
        return self.solution_path

    def get_visited(self) -> set:
        """Return the set of visited states."""
        return self.visited_set

    def get_explored(self) -> set:
        """Return the set of explored states."""
        return self.explored_set
