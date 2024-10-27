from typing import List


def find_empty_tile(state: int) -> int:
    """Find the position of the empty tile (represented by 0) in the puzzle."""
    state_str = str(state).zfill(9)
    return state_str.index('0')


def swap(state: int, empty_pos: int, new_pos: int) -> int:
    """Swap the empty tile (0) with another tile at new_pos and return the new state as an integer."""
    state_str = list(str(state).zfill(9))
    state_str[empty_pos], state_str[new_pos] = state_str[new_pos], state_str[empty_pos]
    return int(''.join(state_str))


def get_neighbors(state: int) -> List[int]:
    """Generate valid neighbor states by moving the empty tile (0)."""
    neighbors_list = []
    zero_pos = find_empty_tile(state)
    row, col = divmod(zero_pos, 3)
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    for direction in directions:
        new_row, new_col = row + direction[0], col + direction[1]
        if 0 <= new_row < 3 and 0 <= new_col < 3:
            new_zero_pos = new_row * 3 + new_col
            new_state = swap(state, zero_pos, new_zero_pos)
            neighbors_list.append(new_state)

    return neighbors_list


def count_inversions(state: int) -> int:
    """Count the number of inversions in the puzzle state (integer representation)."""
    flat_state = [int(tile) for tile in str(state) if tile != '0']
    inversion_nums = sum(1 for i in range(len(flat_state))
                         for j in range(i + 1, len(flat_state))
                         if flat_state[i] > flat_state[j])
    return inversion_nums


def is_solvable(state: int) -> bool:
    """Check if the 8-puzzle is solvable based on the number of inversions.
    The puzzle is solvable if the number of inversions is even.
    """
    return count_inversions(state) % 2 == 0


# if __name__ == "__main__":
    # initial_state = 123405678
    # empty_tile_position = find_empty_tile(initial_state)
    # print(f"Empty tile position: {empty_tile_position}")
    #
    # neighbors = get_neighbors(initial_state)
    # print(f"Neighbors of {initial_state}: {neighbors}")
    #
    # inversions = count_inversions(initial_state)
    # print(f"Number of inversions in {initial_state}: {inversions}")
    #
    # solvable = is_solvable(initial_state)
    # print(f"Is the puzzle solvable? {'Yes' if solvable else 'No'}")



# OTHER DIRECTIONS
    # directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    # directions = [(1, 0), (-1, 0), (0, -1), (0, 1)]
    # directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    # directions = [(1, 0), (0, 1), (0, -1), (-1, 0)]
    # directions = [(1, 0), (0, -1), (-1, 0), (0, 1)]
    # directions = [(1, 0), (0, -1), (0, 1), (-1, 0)]
    # directions = [(-1, 0), (1, 0), (0, 1), (0, -1)]
    # directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    # directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    # directions = [(-1, 0), (0, 1), (0, -1), (1, 0)]
    # directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]
    # directions = [(-1, 0), (0, -1), (0, 1), (1, 0)]
    # directions = [(0, 1), (1, 0), (-1, 0), (0, -1)]
    # directions = [(0, 1), (-1, 0), (1, 0), (0, -1)]
    # directions = [(0, 1), (-1, 0), (0, -1), (1, 0)]
    # directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    # directions = [(0, 1), (0, -1), (-1, 0), (1, 0)]
    # directions = [(0, -1), (1, 0), (-1, 0), (0, 1)]
    # directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    # directions = [(0, -1), (-1, 0), (1, 0), (0, 1)]
    # directions = [(0, -1), (-1, 0), (0, 1), (1, 0)]
    # directions = [(0, -1), (0, 1), (1, 0), (-1, 0)]
    # directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
