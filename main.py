import sys
import random
import logging
import pyautogui
from PyQt5.QtWidgets import (QApplication, QPushButton, QVBoxLayout, 
                            QWidget, QSystemTrayIcon, QMenu)
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIcon

class MouseMover(QWidget):
    def __init__(self):
        super().__init__()
        
        # Configuration
        pyautogui.FAILSAFE = False  # Disable failsafe
        self.move_interval = 30000   # 30 seconds
        self.movement_range = (5, 15) # Min/Max pixels to move
        
        # Setup logging
        logging.basicConfig(
            filename='mouse_mover.log',
            level=logging.INFO,
            format='%(asctime)s - %(message)s'
        )
        
        self.init_ui()
        self.init_movements()
        self.init_timer()
        self.init_tray_icon()

    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle('Mouse Mover Pro')
        self.setFixedSize(250, 100)
        
        self.button = QPushButton('Start', self)
        self.button.clicked.connect(self.toggle_movement)
        
        layout = QVBoxLayout()
        layout.addWidget(self.button)
        self.setLayout(layout)
        
    def init_movements(self):
        """Initialize random movement patterns"""
        min_move, max_move = self.movement_range
        self.movements = [
            (random.randint(min_move, max_move), 0),          # Right
            (0, random.randint(min_move, max_move)),         # Down
            (-random.randint(min_move, max_move), 0),        # Left
            (0, -random.randint(min_move, max_move))         # Up
        ]
        self.index = 0
        logging.info("Movement pattern initialized")

    def init_timer(self):
        """Initialize the movement timer"""
        self.timer = QTimer(self)
        self.timer.setInterval(self.move_interval)
        self.timer.timeout.connect(self.move_mouse)

    def init_tray_icon(self):
        """Initialize system tray icon"""
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("icon.png"))  # Add your icon file
        
        menu = QMenu()
        show_action = menu.addAction("Show")
        show_action.triggered.connect(self.show)
        exit_action = menu.addAction("Exit")
        exit_action.triggered.connect(self.close)
        
        self.tray_icon.setContextMenu(menu)
        self.tray_icon.show()
        self.tray_icon.activated.connect(self.tray_icon_clicked)

    def tray_icon_clicked(self, reason):
        """Handle tray icon clicks"""
        if reason == QSystemTrayIcon.DoubleClick:
            self.showNormal()

    def toggle_movement(self):
        """Toggle mouse movement on/off"""
        if self.timer.isActive():
            self.timer.stop()
            self.button.setText('Start')
            logging.info("Movement stopped")
        else:
            self.init_movements()  # Generate new random pattern
            self.timer.start()
            self.button.setText('Stop')
            logging.info("Movement started")

    def move_mouse(self):
        """Perform the mouse movement"""
        try:
            move = self.movements[self.index]
            current_x, current_y = pyautogui.position()
            new_x = current_x + move[0]
            new_y = current_y + move[1]
            
            pyautogui.moveTo(new_x, new_y, duration=0.25)
            logging.info(f"Moved mouse to ({new_x}, {new_y})")
            
            # Cycle to next movement
            self.index = (self.index + 1) % len(self.movements)
            
        except Exception as e:
            logging.error(f"Error moving mouse: {str(e)}")
            self.timer.stop()
            self.button.setText('Start')

    def closeEvent(self, event):
        """Clean up when closing the application"""
        self.timer.stop()
        self.tray_icon.hide()
        logging.info("Application closed")
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # Set application style (optional)
    app.setStyle('Fusion')
    
    # Create and show main window
    mover = MouseMover()
    mover.show()
    
    sys.exit(app.exec_())