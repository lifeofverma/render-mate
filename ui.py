# Import modules
import sys
from getpass import getuser
import os
# Importing third party modules
from PySide2.QtWidgets import QApplication, QMainWindow, QMenuBar, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QFileDialog, QTableWidgetItem, QHeaderView
from PySide2.QtGui import QPixmap, QIcon
from PySide2.QtCore import Qt 

# Importing custom modules
from constants.constants import NUKE_ICON, USER_ICON, ADD_ICON, PAUSE_ICON, REMOVE_ICON, REMOVE_SELECTED_ICON, PLAY_ICON




from pprint import pprint



class RenderMate(QMainWindow):
    def __init__(self):
        super().__init__()


        self.setWindowTitle("RenderMate V1.0.0")
        # self.setFixedSize(800, 200)
        self.RV_playerMenu = QMenuBar()        
        self.RV_playerMenu.addMenu("RV Player Path")
        self.setMenuBar(self.RV_playerMenu)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)



        # header widget starts from here
        self.header = QWidget()
        self.header.setStyleSheet("background-color: #1d1d1d;")
        # self.header.setFixedSize(1000,100)
        self.nuke_icon_label = QLabel()
        self.user_icon_label = QLabel()
        self.user_name = QLabel(getuser())
        self.tool_name = QLabel("RenderMate")
        self.nuke_icon_label.setPixmap(QPixmap(NUKE_ICON).scaled(64, 64 , Qt.KeepAspectRatio,  Qt.SmoothTransformation ))
        self.user_icon_label.setPixmap(QPixmap(USER_ICON).scaled(64,64 , Qt.KeepAspectRatio , Qt.SmoothTransformation))

        self.header_layout = QHBoxLayout()
        self.header_layout.addWidget(self.nuke_icon_label)
        self.header_layout.addWidget(self.user_icon_label)
        self.header_layout.addWidget(self.tool_name)
        self.header_layout.addWidget(self.user_name)
        self.header.setLayout(self.header_layout)



        # side bar starts from here 

        self.side_bar = QWidget()
        self.side_bar.setStyleSheet("background-color: #323232;")
        self.add_button = QPushButton("add")
        self.add_button.clicked.connect(self.add_files)
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



        self.property_widget = QTableWidget()
        self.property_widget.setColumnCount(6)
        self.property_widget.setHorizontalHeaderLabels(["File Path", "File Name" , "Writes" , "Progress" , "Status" , "Operations"]) 
        self.property_widget.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.property_widget.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.property_widget.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.property_widget.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch) 
        self.property_widget.horizontalHeader().setSectionResizeMode(4, QHeaderView.Stretch) 
        self.property_widget.horizontalHeader().setSectionResizeMode(5, QHeaderView.Stretch)
        self.property_widget.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        
        self.hbox_layout = QHBoxLayout()
        self.hbox_layout.addWidget(self.side_bar)
        self.hbox_layout.addWidget(self.property_widget)


        self.operation_widget = QWidget()
        self.rvbtn = QPushButton("RV")
        self.rvbtn.setMinimumHeight(40)
        self.nuke_btn = QPushButton("nuke")
        self.start_btn = QPushButton("start")
        self.stop_btn = QPushButton("stop")
        self.open_dir_btn = QPushButton("open dir")
        self.pause_btn = QPushButton("pause")

        self.op_widget_layout = QHBoxLayout()
        self.op_widget_layout.addWidget(self.rvbtn)
        self.op_widget_layout.addWidget(self.nuke_btn)
        self.op_widget_layout.addWidget(self.start_btn)
        self.op_widget_layout.addWidget(self.stop_btn)
        self.op_widget_layout.addWidget(self.open_dir_btn)
        self.op_widget_layout.addWidget(self.pause_btn)

        self.operation_widget.setLayout(self.op_widget_layout)        
        




        main_layout = QVBoxLayout()
        main_layout.addWidget(self.header)
        main_layout.addLayout(self.hbox_layout)
        self.central_widget.setLayout(main_layout) 

    def add_files(self):
        files =  list(QFileDialog.getOpenFileNames(None , "Select a nuke file", r"D:\GamutX\Render_Mate\Nuke_files" , "Nuke Files(*.nk)")[0])
        files_path = []
        files_name = []

        for file in files:
            files_path.append(os.path.dirname(file))
            files_name.append(os.path.basename(file))

        self.property_widget.setRowCount(len(files_path))

        for i in range(len(files_path)):
            self.property_widget.setItem(i, 0 , QTableWidgetItem(files_path[i]))
            self.property_widget.setItem(i, 1 , QTableWidgetItem(files_name[i]))
            self.property_widget.setCellWidget(i, 5 , self.operation_widget )





if __name__ == "__main__":
    app = QApplication()
    ui = RenderMate()
    ui.show()
    sys.exit(app.exec_())