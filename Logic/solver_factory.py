from typing import List
from EightPuzzleGame.Logic.astar_euclidean import AStarEuclideanPuzzleSolver
from EightPuzzleGame.Logic.astar_manhattan import AStarManhattanPuzzleSolver
from EightPuzzleGame.Logic.bfs_solver import BFSPuzzleSolver
from EightPuzzleGame.Logic.dfs_solver import DFSPuzzleSolver
from EightPuzzleGame.Logic.ids_solver import IDSPuzzleSolver
from EightPuzzleGame.Logic.puzzle_solver import PuzzleSolver


class SolverFactory:
    @staticmethod
    def create_solver(method_name: str, initial_state: List[List[int]]) -> PuzzleSolver:
        solvers = {
            "DFS": DFSPuzzleSolver,
            "BFS": BFSPuzzleSolver,
            "IDS": IDSPuzzleSolver,
            "AStarManhattan": AStarManhattanPuzzleSolver,
            "AStarEuclidean": AStarEuclideanPuzzleSolver
        }

        if method_name not in solvers:
            raise ValueError(f"Unsupported method name: {method_name}")

        return solvers[method_name](initial_state)


def solve_puzzle(method_name: str, initial_state: List[List[int]]) -> dict:
    solver = SolverFactory.create_solver(method_name, initial_state)
    solver.solve()
    return {
        "solution_path": solver.get_steps(),
        "runtime": solver.get_runtime(),
        "depth": solver.get_depth(),
        "num_nodes": solver.get_number_of_nodes(),
        "cost": solver.cost,
    }


# if __name__ == "__main__":
#     initial_state = [[1, 2, 0],
#                      [3, 4, 5],
#                      [6, 7, 8]]
#
#     result = solve_puzzle("IDS", initial_state)
#     solution_path = result['solution_path']
#     runtime = result['runtime']
#     depth = result['depth']
#     num_nodes = result['num_nodes']
#     cost = result['cost']
#
#     print(solution_path)
#     print(runtime)
#     print(depth)
#     print(num_nodes)
#     print(cost)
