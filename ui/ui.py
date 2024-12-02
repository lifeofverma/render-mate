import sys
from getpass import getuser
from PySide2.QtWidgets import QApplication, QMainWindow, QMenuBar, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel
from PySide2.QtGui import QPixmap
from PySide2.QtCore import Qt 

class RenderMate(QMainWindow):
    def __init__(self):
        super().__init__()


        self.setWindowTitle("RenderMate V1.0.0")
        self.setStyleSheet("background-color: #0f0f0f;")
        self.RV_playerMenu = QMenuBar()        
        self.RV_playerMenu.addMenu("RV Player Path")
        self.RV_playerMenu.setStyleSheet("""QMenuBar{color: white;} QMenuBar::item{background-color: #1d1d1d;} QMenuBar::item:selected{background-color:#1d1d1d;} QMenuBar::item:hover{color:#0f0f0f;}""")
        self.setMenuBar(self.RV_playerMenu)

        self.central_widget = QWidget()
        self.central_widget.setStyleSheet("background-color: #0f0f0f;")
        self.setCentralWidget(self.central_widget)



        # header widget starts from here
        self.header = QWidget()
        self.header.setFixedSize(1500,100)
        self.header.setStyleSheet("background-color: #1d1d1d;")


        self.nuke_icon_label = QLabel()
        self.user_icon_label = QLabel()
        self.user_name = QLabel(getuser())
        self.tool_name = QLabel("RenderMate")
        nuke_icon = QPixmap("icons/nuke_red_icon.png")
        user_icon = QPixmap("icons/user_icon.png")
        scaled_nuke_icon = nuke_icon.scaled(64, 64 , Qt.KeepAspectRatio,  Qt.SmoothTransformation )
        scaled_user_icon = user_icon.scaled(64,64 , Qt.KeepAspectRatio , Qt.SmoothTransformation)
        self.nuke_icon_label.setPixmap(scaled_nuke_icon)
        self.user_icon_label.setPixmap(scaled_user_icon)

        self.header_layout = QHBoxLayout()
        self.header_layout.addWidget(self.nuke_icon_label)
        self.header_layout.addWidget(self.user_icon_label)
        self.header_layout.addWidget(self.tool_name)
        self.header_layout.addWidget(self.user_name)
        self.header.setLayout(self.header_layout)



        # side bar starts from here 

        self.side_bar = QWidget()
        self.side_bar.setStyleSheet("background-color: #323232;")

        self.add_button = QPushButton("Add")
        self.start_all = QPushButton("Start")
        self.pause_all = QPushButton("Pause")
        self.remove_all = QPushButton("Remove")
        self.remove_selected = QPushButton("Remove Selected")

        self.buttons_layout = QVBoxLayout()
        self.buttons_layout.addWidget(self.add_button)
        self.buttons_layout.addWidget(self.start_all)
        self.buttons_layout.addWidget(self.pause_all)
        self.buttons_layout.addWidget(self.remove_all)
        self.buttons_layout.addWidget(self.remove_selected)

        self.side_bar.setLayout(self.buttons_layout)



        self.test_table = QWidget()
        self.test_table.setStyleSheet("background-color: black;")
        self.side_bar.setFixedSize(500,500)
        self.test_table.setFixedSize(500,500)

        
        self.midwidgetlayout = QHBoxLayout()
        self.midwidgetlayout.addWidget(self.side_bar)
        self.midwidgetlayout.addWidget(self.test_table)


        # self.vlayout = QVBoxLayout()
        # self.vlayout.addWidget(self.header)
        # self.vlayout.addLayout(self.midwidgetlayout)






        main_layout = QVBoxLayout()
        main_layout.addWidget(self.header)
        main_layout.addLayout(self.midwidgetlayout)
        self.central_widget.setLayout(main_layout) 






if __name__ == "__main__":
    app = QApplication()
    ui = RenderMate()
    ui.show()
    sys.exit(app.exec_())
    