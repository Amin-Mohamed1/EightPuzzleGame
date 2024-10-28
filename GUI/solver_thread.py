from PyQt5.QtCore import QThread, pyqtSignal
from Logic.solver_factory import solve_puzzle


class SolverThread(QThread):
    finished = pyqtSignal(dict)

    def __init__(self, method_name: str, game_initial_state: int):
        super(SolverThread, self).__init__()
        self.method_name = method_name
        self.game_initial_state = game_initial_state

    def run(self):
        solve = solve_puzzle(self.method_name, self.game_initial_state)
        self.finished.emit(solve)
