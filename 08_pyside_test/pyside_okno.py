import sys
from PySide6 import QtWidgets, QtCore
#česky
x = 0

app = QtWidgets.QApplication(sys.argv)
window = QtWidgets.QMainWindow()
window.setWindowTitle("Moje okno")
window.resize(500, 500)

central_widget = QtWidgets.QWidget()
window.setCentralWidget(central_widget)

main_layout = QtWidgets.QVBoxLayout(central_widget)
label = QtWidgets.QLabel("To je moje okno")
label.setAlignment(QtCore.Qt.AlignCenter)
label.setStyleSheet("font-size: 100px; color: green; font-weight: bold;")
main_layout.addWidget(label)

show_x = QtWidgets.QLabel(f"Hodnota x: {x}")
show_x.setAlignment(QtCore.Qt.AlignCenter)
show_x.setStyleSheet("font-size: 20px;")
main_layout.addWidget(show_x)


button = QtWidgets.QPushButton("Klikni mě")
button.setStyleSheet("font-size: 30px;")
main_layout.addWidget(button)
def on_button_clicked():
    global x
    x += 1
    label.setText("Tlačítko bylo kliknuto!")
    show_x.setText(f"Hodnota x: {x}")


button.clicked.connect(on_button_clicked)

window.show()
sys.exit(app.exec())