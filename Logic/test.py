from EightPuzzleGame.Logic import bfs_solver
from EightPuzzleGame.Logic.solver_factory import solve_puzzle


def test_bfs():
    initial_state = [[1, 2, 5], [3, 4, 0], [6, 7, 8]]
    bfs = bfs_solver.BFSPuzzleSolver(initial_state)
    bfs.solve()
    assert bfs.get_depth() == 3
    assert bfs.cost == 3
    assert bfs.solution_path == [[[1, 2, 5], [3, 4, 0], [6, 7, 8]], [[1, 2, 0], [3, 4, 5], [6, 7, 8]],
                                 [[1, 0, 2], [3, 4, 5], [6, 7, 8]], [[0, 1, 2], [3, 4, 5], [6, 7, 8]]]


def test_unsolvable_puzzle():
    initial_state = [[1, 2, 3], [4, 5, 6], [8, 7, 0]]
    bfs = bfs_solver.BFSPuzzleSolver(initial_state)
    bfs.solve()
    assert bfs.get_depth() == 0
    assert bfs.cost == 0
    assert bfs.solution_path == []


def test_factory_with_bfs():
    initial_state = [[1, 2, 5], [3, 4, 0], [6, 7, 8]]
    result = solve_puzzle("BFS", initial_state)
    assert result['depth'] == 3
    assert result['cost'] == 3
    assert result['solution_path'] == [[[1, 2, 5], [3, 4, 0], [6, 7, 8]], [[1, 2, 0], [3, 4, 5], [6, 7, 8]],
                                       [[1, 0, 2], [3, 4, 5], [6, 7, 8]], [[0, 1, 2], [3, 4, 5], [6, 7, 8]]]
