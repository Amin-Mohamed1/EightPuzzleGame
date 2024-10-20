from typing import List
from Logic.astar_solver import AStarPuzzleSolver
from Logic.bfs_solver import BFSPuzzleSolver
from Logic.dfs_solver import DFSPuzzleSolver
from Logic.ids_solver import IDSPuzzleSolver
from Logic.heuristics import manhattan_heuristic, euclidean_heuristic, misplaced_tiles_heuristic


def solve_puzzle(method_name: str, initial_state: List[List[int]]) -> dict:
    if method_name == "AStarManhattan":
        solver = AStarPuzzleSolver(initial_state, manhattan_heuristic)
    elif method_name == "AStarEuclidean":
        solver = AStarPuzzleSolver(initial_state, euclidean_heuristic)
    elif method_name == "AStarMisplacedTiles":
        solver = AStarPuzzleSolver(initial_state, misplaced_tiles_heuristic)
    elif method_name == "BFSPuzzleSolver":
        solver = BFSPuzzleSolver(initial_state)
    elif method_name == "DFSPuzzleSolver":
        solver = DFSPuzzleSolver(initial_state)
    elif method_name == "IDSPuzzleSolver":
        solver = IDSPuzzleSolver(initial_state)
    else:
        raise ValueError(f"Unsupported method name: {method_name}")

    solver.solve()
    return {
        "solution_path": solver.get_steps(),
        "runtime": solver.get_runtime(),
        "depth": solver.get_depth(),
        "num_nodes": solver.get_number_of_nodes(),
        "cost": solver.get_cost(),
    }


if __name__ == "__main__":
    initial_state = [[0, 2, 1],
                     [4, 3, 5],
                     [6, 7, 8]]

    result = solve_puzzle("IDSPuzzleSolver", initial_state)
    print("Solution Path:", result['solution_path'])
    print("Runtime:", result['runtime'])
    print("Depth:", result['depth'])
    print("Number of Nodes:", result['num_nodes'])
    print("Cost:", result['cost'])
    print()
