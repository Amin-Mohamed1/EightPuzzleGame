from typing import List, Tuple, Dict


def reset_solver(self) -> None:
    """Reset solver attributes if the puzzle is determined to be unsolvable."""
    self.num_nodes = 0
    self.solution_path = []
    self.max_search_depth = 0
    self.run_time = 0
    self.cost = 0


def expand_state(self, state: List[List[int]], stack: List[Tuple[List[List[int]], int]],
                 current_depth: int, child_parent_map: Dict) -> None:
    """Expand the current state by finding its valid neighbors and add them to the stack."""
    for neighbor in self.get_neighbors(state):
        neighbor_tuple = tuple(map(tuple, neighbor))

        # Only add neighbor states that have not been visited or explored
        if neighbor_tuple not in self.visited_set and neighbor_tuple not in self.explored_set:
            stack.append((neighbor, current_depth + 1))
            child_parent_map[neighbor_tuple] = state
            self.visited_set.add(neighbor_tuple)


def get_neighbors(self, state: List[List[int]]) -> List[List[List[int]]]:
    """Generate valid neighbor states by moving the empty tile (0)."""
    neighbors = []
    zero_pos = self.find_empty_tile(state)  # Locate the position of the empty tile (0)
    directions = [(-1, 0), (1, 0), (0, 1), (0, -1)]  # Define movement directions (up, down, right, left)

    # Try moving the empty tile in each direction and generate new states
    for direction in directions:
        new_zero_pos = (zero_pos[0] + direction[0], zero_pos[1] + direction[1])
        if self.is_within_bounds(new_zero_pos):
            new_state = self.swap(state, zero_pos, new_zero_pos)
            neighbors.append(new_state)

    return neighbors


def find_empty_tile(self, state: List[List[int]]) -> Tuple[int, int]:
    """Find the position of the empty tile (represented by 0) in the puzzle."""
    for i in range(len(state)):
        for j in range(len(state[i])):
            if state[i][j] == 0:
                return i, j
    return -1, -1  # Default return value (should not happen if valid input is provided)


def is_within_bounds(self, position: Tuple[int, int]) -> bool:
    """Check if the given position is within the 3x3 puzzle boundaries."""
    return (0 <= position[0] < 3 and
            0 <= position[1] < 3)


def swap(self, state: List[List[int]], parent: Tuple[int, int], child: Tuple[int, int]) -> List[List[int]]:
    """Swap the positions of two tiles and return the new state."""
    new_state = [row[:] for row in state]  # Create a copy of the current state
    new_state[parent[0]][parent[1]], new_state[child[0]][child[1]] = (
        new_state[child[0]][child[1]], new_state[parent[0]][parent[1]])
    return new_state


def get_path(self, child_parent_map: Dict, goal_state: List[List[int]]) -> List[List[List[int]]]:
    """Reconstruct the solution path from the goal state back to the initial state."""
    path = []
    current_state = tuple(map(tuple, goal_state))

    # Trace back from the goal state to the initial state using the child-parent map
    while current_state in child_parent_map:
        path.append(current_state)
        current_state = tuple(map(tuple, child_parent_map[current_state]))

    # Add the initial state and reverse the path to get the correct order
    path.append(tuple(map(tuple, self.initial_state)))
    path.reverse()

    # Convert tuples back to lists for consistency
    return [list(map(list, state)) for state in path]
