import sys
import TowerSolver
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QLineEdit, QGridLayout, QWidget, QCheckBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSlot, QThread


class MainWindow(QMainWindow):
    def __init__(self):

        super(MainWindow, self).__init__()
        self.solver = TowerSolver.TowerSolver()
        self.centralwidget = QWidget()
        self.setCentralWidget(self.centralwidget)
        self.labels = []
        self.setGeometry(200, 200, 400, 600)

        # create thread for solving process
        self.thread = QThread()
        self.solver.output.connect(self.update_board)
        self.solver.moveToThread(self.thread)
        self.thread.started.connect(self.solver.initialize)
        self.thread.finished.connect(self.thread.quit)
        self.inputs = []

        self.initLayOut()

    def initLayOut(self):
        # create grid layout and add buttons, labels and text inputs
        self.layout = QGridLayout(self.centralwidget)

        self.quitbutton = QtWidgets.QPushButton("Quit", self)
        self.quitbutton.clicked.connect(self.on_quit_click)
        self.layout.addWidget(self.quitbutton, 10, 2)

        self.solvebutton = QtWidgets.QPushButton("Solve", self)
        self.solvebutton.clicked.connect(self.on_solve_click)
        self.layout.addWidget(self.solvebutton, 10, 0)

        self.resetbutton = QtWidgets.QPushButton("Reset", self)
        self.resetbutton.clicked.connect(self.on_reset_click)
        self.layout.addWidget(self.resetbutton, 10, 1)

        self.visualizebtn = QCheckBox("Visualization")
        self.visualizebtn.stateChanged.connect(lambda:self.solver.visualize(self.visualizebtn))
        self.layout.addWidget(self.visualizebtn, 10, 3)

        for row in range(1, 6):
            self.input = QLineEdit(self)
            self.input2 = QLineEdit(self)
            self.input.textChanged[str].connect(self.onChanged)
            self.input2.textChanged[str].connect(self.onChanged)
            self.inputs.append(self.input)
            self.inputs.append(self.input2)
            self.layout.addWidget(self.input, row, 0)
            self.layout.addWidget(self.input2, row, 6)


            for col in range(1, 6):
                self.input = QLineEdit(self)
                self.input2 = QLineEdit(self)
                self.input.textChanged[str].connect(self.onChanged)
                self.input2.textChanged[str].connect(self.onChanged)
                self.inputs.append(self.input)
                self.inputs.append(self.input2)
                self.layout.addWidget(self.input, 0, col)
                self.layout.addWidget(self.input2, 6, col)

                self.label = QtWidgets.QLabel("0")
                self.labels.append(self.label)
                self.layout.addWidget(self.label, row, col)

    @pyqtSlot()
    def on_solve_click(self):
        # initialize solver thread and connect thread output to update_board to see visualization of backtracking
        self.thread.start()

    def on_quit_click(self):
        self.close()

    # reset values to 0
    def on_reset_click(self):
        self.solver.reset_board()
        board = self.solver.get_board()
        self.update_board(board)
        for input in self.inputs:
            input.clear()


    def update_board(self, solved_board):
        for i in range(25):
            self.labels[i].setText(str(solved_board[i//5 + 1][i % 5 + 1]))

    # change board value according to text input
    def onChanged(self, text):
        try:
            idx = self.layout.indexOf(self.sender())
            pos = self.layout.getItemPosition(idx)
            self.solver.change_board_value((pos[0], pos[1]), int(text))
        except ValueError:
            pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mywindow = MainWindow()
    mywindow.show()
    sys.exit(app.exec_())

MainWindow()
