from typing import List, Tuple


def find_empty_tile(state: List[List[int]]) -> Tuple[int, int]:
    """Find the position of the empty tile (represented by 0) in the puzzle."""
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j
    return -1, -1


def is_within_bounds(position: Tuple[int, int]) -> bool:
    """Check if the given position is within the 3x3 puzzle boundaries."""
    return 0 <= position[0] < 3 and 0 <= position[1] < 3


def swap(state: List[List[int]], parent: Tuple[int, int], child: Tuple[int, int]) -> List[List[int]]:
    """Swap the positions of two tiles and return the new state."""
    new_state = [row[:] for row in state]
    new_state[parent[0]][parent[1]], new_state[child[0]][child[1]] = (
        new_state[child[0]][child[1]], new_state[parent[0]][parent[1]])
    return new_state


def get_neighbors(state: List[List[int]]) -> List[List[List[int]]]:
    """Generate valid neighbor states by moving the empty tile (0)."""
    neighbors = []
    zero_pos = find_empty_tile(state)
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]

    for direction in directions:
        new_zero_pos = (zero_pos[0] + direction[0], zero_pos[1] + direction[1])
        if is_within_bounds(new_zero_pos):
            new_state = swap(state, zero_pos, new_zero_pos)
            neighbors.append(new_state)

    return neighbors


def count_inversions(state: List[List[int]]) -> int:
    """Count the number of inversions in the puzzle state."""
    flat_state = [tile for row in state for tile in row if tile != 0]
    inversions = sum(1 for i in range(len(flat_state))
                     for j in range(i + 1, len(flat_state))
                     if flat_state[i] > flat_state[j])
    return inversions


def is_solvable(state: List[List[int]]) -> bool:
    """Check if the 8-puzzle is solvable based on the number of inversions.
    The puzzle is solvable if the number of inversions is even.
    """
    return count_inversions(state) % 2 == 0
