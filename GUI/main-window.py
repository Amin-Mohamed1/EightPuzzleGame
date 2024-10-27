import random
import sys
from functools import partial
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi
from Logic.solver_factory import solve_puzzle


class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("8-Game-Window.ui", self)
        self.current_state = []
        self.states_memo = []
        self.state_pointer = 0
        self.add_buttons()
        self.randomize()

        self.manhattan_radio.setChecked(True)

        self.random_button.clicked.connect(self.randomize)
        self.submit_button.clicked.connect(self.read_input)
        self.next_button.clicked.connect(self.move_state_forward)
        self.prev_button.clicked.connect(self.move_state_backward)
        self.back_button.clicked.connect(partial(self.swap_pages, True))

        self.dfs_button.clicked.connect(partial(self.solve, "DFSPuzzleSolver"))
        self.bfs_button.clicked.connect(partial(self.solve, "BFSPuzzleSolver"))
        self.ids_button.clicked.connect(partial(self.solve, "IDSPuzzleSolver"))
        self.a_star_button.clicked.connect(self.handle_radio)

    def add_buttons(self):
        self.current_state = [[self.board_button1, self.board_button2, self.board_button3],
                              [self.board_button4, self.board_button5, self.board_button6],
                              [self.board_button7, self.board_button8, self.board_button9]]

    def randomize(self):
        self.swap_pages(True)
        numbers = list(range(9))
        random.shuffle(numbers)
        for i in range(3):
            for j in range(3):
                self.current_state[i][j].setText(str(numbers.pop()))
        self.coloring_board()

    def read_input(self):
        self.swap_pages(True)
        user_input = self.input_field.text().replace(" ", "").split(',')
        for i in range(3):
            for j in range(3):
                self.current_state[i][j].setText(user_input.pop(0))
        self.coloring_board()

    def get_buttons_data(self):
        data = 0
        for i in range(3):
            for j in range(3):
                data = data * 10 + int(self.current_state[i][j].text())
        return data

    def add_data_to_buttons(self, data: int):
        str_data = str(data).zfill(9)
        pointer = 0
        for i in range(3):
            for j in range(3):
                self.current_state[i][j].setText(str_data[pointer])
                pointer += 1

    def swap_pages(self, algorithms: bool):
        if algorithms:
            self.states_memo = []
            self.state_pointer = 0
            self.stack_widget.setCurrentIndex(0)
        else:
            self.stack_widget.setCurrentIndex(1)

    def move_state_forward(self):
        if self.state_pointer < len(self.states_memo) - 1:
            self.state_pointer += 1
            self.add_data_to_buttons(self.states_memo[self.state_pointer])
            self.coloring_board()

    def move_state_backward(self):
        if self.state_pointer > 0:
            self.state_pointer -= 1
            self.add_data_to_buttons(self.states_memo[self.state_pointer])
            self.coloring_board()

    def solve(self, method: str):
        solver = solve_puzzle(method, self.get_buttons_data())
        self.states_memo = solver['solution_path']
        if self.states_memo:
            self.cost_label.setText(f"Cost = {solver['cost']}")
            self.depth_label.setText(f"Max Depth = {solver['depth']}")
            self.time_label.setText(f"Time Taken = {solver['runtime']:.7f}" + " seconds")
            self.nodes_expansion_label.setText(f"Nodes Expansion = {solver['num_nodes']}")
        else:
            self.cost_label.setText("Cost = Infinity")
            self.depth_label.setText("Max Depth = Infinity")
            self.time_label.setText("Time Taken = Infinity")
            self.nodes_expansion_label.setText("Nodes Expansion = Infinity")

        self.swap_pages(False)

    def change_button_color(self, i: int, j: int, color: str):
        self.current_state[i][j].setStyleSheet(f"background-color: {color};")

    def coloring_board(self):
        for i in range(3):
            for j in range(3):
                if self.current_state[i][j].text() == "0":
                    self.change_button_color(i, j, "rgb(74, 238, 148)")
                else:
                    self.change_button_color(i, j, "#558DC0")

    def get_selected_radio(self):
        if self.manhattan_radio.isChecked():
            return "AStarManhattan"
        elif self.euclidean_radio.isChecked():
            return "AStarEuclidean"
        else:
            return "AStarMisplacedTiles"

    def handle_radio(self):
        self.solve(self.get_selected_radio())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
