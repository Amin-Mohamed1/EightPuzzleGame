from typing import List

TARGET_POSITIONS = {
    1: (0, 1),
    2: (0, 2),
    3: (1, 0),
    4: (1, 1),
    5: (1, 2),
    6: (2, 0),
    7: (2, 1),
    8: (2, 2)
}


def manhattan_heuristic(state: List[List[int]]) -> float:
    """Calculate the Manhattan distance heuristic for the 8-puzzle """
    total_distance = 0
    for i in range(3):
        for j in range(3):
            value = state[i][j]
            if value != 0:
                target_row, target_col = TARGET_POSITIONS[value]
                distance = abs(i - target_row) + abs(j - target_col)
                total_distance += distance
    return total_distance


def euclidean_heuristic(state: List[List[int]]) -> float:
    """Calculate the Euclidean distance heuristic for the 8-puzzle """
    total_distance = 0.0
    for i in range(3):
        for j in range(3):
            value = state[i][j]
            if value != 0:
                target_row, target_col = TARGET_POSITIONS[value]
                distance = ((i - target_row) ** 2 + (j - target_col) ** 2) ** 0.5
                total_distance += distance
    return total_distance


def misplaced_tiles_heuristic(state: List[List[int]]) -> float:
    """Count the number of misplaced tiles for the 8-puzzle """
    misplaced_count = 0
    for i in range(3):
        for j in range(3):
            value = state[i][j]
            if value != 0 and (i, j) != TARGET_POSITIONS[value]:
                misplaced_count += 1
    return misplaced_count
