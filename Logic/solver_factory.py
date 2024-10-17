from typing import List
from Logic.astar_euclidean import AStarEuclideanPuzzleSolver
from Logic.astar_manhattan import AStarManhattanPuzzleSolver
from Logic.bfs_solver import BFSPuzzleSolver
from Logic.dfs_solver import DFSPuzzleSolver
from Logic.ids_solver import IDSPuzzleSolver
from Logic.puzzle_solver import PuzzleSolver


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


if __name__ == "__main__":
    initial_state = [[1, 6, 5],
                     [7, 0, 2],
                     [4, 8, 3]]

    result = solve_puzzle("DFS", initial_state)
    solution_path = result['solution_path']
    runtime = result['runtime']
    depth = result['depth']
    num_nodes = result['num_nodes']
    cost = result['cost']

    print(solution_path)
    print(runtime)
    print(depth)
    print(num_nodes)
    print(cost)
