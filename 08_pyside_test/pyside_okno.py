import sys
from PySide6 import QtWidgets, QtCore
#česky
class ColorSwatch(QtWidgets.QPushButton):
    def __init__(self, color_hex, parent=None):
        super().__init__(parent)
        self.color_hex = color_hex
        self.setFixedSize(50, 50)
        self.setCursor(QtCore.Qt.PointingHandCursor)
        self.setStyleSheet(f"background-color: {self.color_hex}; border: 1px solid #ddd; border-radius: 10px;")
    def print_my_color(self):
        print(f"Moje barva je {self.color_hex}")
    
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Moje okno")
        self.resize(500, 500)

        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QtWidgets.QVBoxLayout(central_widget)
        label = QtWidgets.QLabel("To je moje okno")
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setStyleSheet("font-size: 100px; color: green; font-weight: bold;")
        main_layout.addWidget(label)
        red_swatch = ColorSwatch("#FF0000")
        main_layout.addWidget(red_swatch,alignment=QtCore.Qt.AlignCenter)
        red_swatch.clicked.connect(red_swatch.print_my_color)
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())