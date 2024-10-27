from Logic.astar_solver import AStarPuzzleSolver
from Logic.heuristics import manhattan_heuristic, euclidean_heuristic, misplaced_tiles_heuristic
from Logic.bfs_solver import BFSPuzzleSolver
from Logic.dfs_solver import DFSPuzzleSolver
from Logic.ids_solver import IDSPuzzleSolver


def solve_puzzle(method_name: str, game_initial_state: int) -> dict:
    if method_name == "AStarManhattan":
        solver = AStarPuzzleSolver(game_initial_state, manhattan_heuristic)
    elif method_name == "AStarEuclidean":
        solver = AStarPuzzleSolver(game_initial_state, euclidean_heuristic)
    elif method_name == "AStarMisplacedTiles":
        solver = AStarPuzzleSolver(game_initial_state, misplaced_tiles_heuristic)
    elif method_name == "BFSPuzzleSolver":
        solver = BFSPuzzleSolver(game_initial_state)
    elif method_name == "DFSPuzzleSolver":
        solver = DFSPuzzleSolver(game_initial_state)
    elif method_name == "IDSPuzzleSolver":
        solver = IDSPuzzleSolver(game_initial_state)
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


# if __name__ == "__main__":
#     initial_state = 806547231
#     result = solve_puzzle("AStarMisplacedTiles", initial_state)
#     print("Solution Path:", result['solution_path'])
#     print("Runtime:", result['runtime'])
#     print("Depth:", result['depth'])
#     print("Number of Nodes:", result['num_nodes'])
#     print("Cost:", result['cost'])
