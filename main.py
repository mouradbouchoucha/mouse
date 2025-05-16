import sys
import time
import pyautogui
from PyQt5.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtCore import QTimer

class MouseMover(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.movements = [
            (5, 0),   # Right
            (0, 5),   # Down
            (-5, 0),  # Left
            (0, -5)   # Up
        ]
        self.index = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.move_mouse)

    def initUI(self):
        self.button = QPushButton('Start', self)
        self.button.clicked.connect(self.toggle_movement)

        layout = QVBoxLayout()
        layout.addWidget(self.button)
        self.setLayout(layout)

        self.setWindowTitle('Mouse Mover')
        self.show()

    def toggle_movement(self):
        if self.timer.isActive():
            self.timer.stop()
            self.button.setText('Start')
        else:
            self.timer.start(5000)  # Move every 5 seconds
            self.button.setText('Stop')

    def move_mouse(self):
        move = self.movements[self.index]
        current_x, current_y = pyautogui.position()
        pyautogui.moveTo(current_x + move[0], current_y + move[1])
        self.index = (self.index + 1) % len(self.movements)  # Cycle through movements

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MouseMover()
    sys.exit(app.exec_())