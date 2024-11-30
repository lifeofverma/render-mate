import sys
from PySide2.QtWidgets import QApplication, QMainWindow, QMenuBar, QWidget, QPushButton, QVBoxLayout, QHBoxLayout

class RenderMate(QMainWindow):
    def __init__(self):
        super().__init__()





        self.setWindowTitle("RenderMate V1.0.0")
        self.RV_playerMenu = QMenuBar()        
        self.RV_playerMenu.addMenu("RV Player Path")
        self.setMenuBar(self.RV_playerMenu)


        self.central_widget = QWidget()
        self.central_widget.setStyleSheet("background-color: darkgray;")
        self.setCentralWidget(self.central_widget)

        self.header = QWidget()
        self.header.setFixedHeight(500)
        self.header.setStyleSheet("background-color: lightgray;")
        self.testbtn = QPushButton("test")

        self.header_layout = QHBoxLayout()
        self.header_layout.addWidget(self.testbtn)
        self.header.setLayout(self.header_layout)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.header)
        self.central_widget.setLayout(main_layout) 






if __name__ == "__main__":
    app = QApplication()
    ui = RenderMate()
    ui.show()
    sys.exit(app.exec_())
    