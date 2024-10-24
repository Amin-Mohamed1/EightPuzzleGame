# TARGET_POSITIONS = {
#     '1': (0, 1),
#     '2': (0, 2),
#     '3': (1, 0),
#     '4': (1, 1),
#     '5': (1, 2),
#     '6': (2, 0),
#     '7': (2, 1),
#     '8': (2, 2)
# }
#
#
# def int_to_string(state: int) -> str:
#     """Convert integer state to string representation."""
#     return str(state).zfill(9)
#
#
# def manhattan_heuristic(state: int) -> float:
#     """Calculate the Manhattan distance heuristic for the 8-puzzle from an integer representation."""
#     state_str = int_to_string(state)
#     total_distance = 0
#     for i in range(9):
#         tile = state_str[i]
#         if tile != '0':
#             current_pos = (i // 3, i % 3)
#             target_pos = TARGET_POSITIONS[tile]
#             total_distance += abs(current_pos[0] - target_pos[0]) + abs(current_pos[1] - target_pos[1])
#     return total_distance
#
#
# def euclidean_heuristic(state: int) -> float:
#     """Calculate the Euclidean distance heuristic for the 8-puzzle from an integer representation."""
#     state_str = int_to_string(state)
#     total_distance = 0.0
#     for i in range(9):
#         tile = state_str[i]
#         if tile != '0':
#             current_pos = (i // 3, i % 3)
#             target_pos = TARGET_POSITIONS[tile]
#             distance = ((current_pos[0] - target_pos[0]) ** 2 + (current_pos[1] - target_pos[1]) ** 2) ** 0.5
#             total_distance += distance
#     return total_distance
#
#
# def misplaced_tiles_heuristic(state: int) -> float:
#     """Count the number of misplaced tiles for the 8-puzzle from an integer representation."""
#     state_str = int_to_string(state)
#     misplaced_count = 0
#     for i in range(9):
#         tile = state_str[i]
#         if tile != '0' and tile != str(i):
#             misplaced_count += 1
#     return misplaced_count
#
#
# if __name__ == "__main__":
#     state = 541623078
#     print("Manhattan Heuristic:", manhattan_heuristic(state))
#     print("Euclidean Heuristic:", euclidean_heuristic(state))
#     print("Misplaced Tiles Heuristic:", misplaced_tiles_heuristic(state))
