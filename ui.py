# Import modules
import sys
from getpass import getuser
import os
from pathlib import Path 
import subprocess

# Importing third party modules
from PySide2.QtWidgets import QApplication, QMainWindow, QProgressBar, QMenuBar, QWidget, QPushButton, QVBoxLayout,  QHBoxLayout, QLabel, QTableWidget, QFileDialog, QTableWidgetItem, QHeaderView
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
        # self.header.setStyleSheet("background-color: #1d1d1d;")
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






        #############################################################################################################################################

        # Sidebar widget setup
        self.side_bar = QWidget()
        # self.side_bar.setStyleSheet("background-color: #323232;")
        
        # Initialize buttons for sidebar
        self.add_button = QPushButton("add")
        self.start_all = QPushButton("Start all")
        self.stop_all = QPushButton("stop all")
        self.remove_all = QPushButton("Remove all")
        self.remove_selected = QPushButton("Remove Selected")

        #adding functions to buttons
        self.add_button.clicked.connect(self.add_files_to_table)
        self.remove_all.clicked.connect(self.clear_table)
        self.remove_selected.clicked.connect(self.remove_selected_rows)

        # Layout for sidebar buttons
        self.buttons_layout = QVBoxLayout()
        self.buttons_layout.addWidget(self.add_button)
        self.buttons_layout.addWidget(self.start_all)
        self.buttons_layout.addWidget(self.stop_all)
        self.buttons_layout.addWidget(self.remove_all)
        self.buttons_layout.addWidget(self.remove_selected)
        
        # set Layout for sidebar buttons
        self.side_bar.setLayout(self.buttons_layout)





        #############################################################################################################################################


        # Property widget (table) setup
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(7)
        self.table_widget.setHorizontalHeaderLabels(["File Path", "File Name" , "Writes" , "Progress" , "Status" , "Operations" , "Launchers"]) 
        
        # Set header behavior for property widget
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_widget.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        
        # Table and sidebar layout setup
        self.hbox_layout = QHBoxLayout()
        self.hbox_layout.addWidget(self.side_bar)
        self.hbox_layout.addWidget(self.table_widget)

        # Main layout setup
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.header)
        main_layout.addLayout(self.hbox_layout)
        self.central_widget.setLayout(main_layout) 




    #############################################################################################################################################
    
    
    def create_operation_row_widget(self):
            """
            Creates a QWidget containing multiple buttons for operations in the table rows.
            Returns:
                operation_row_widget (QWidget): A widget containing operation buttons.
            """
            self.operation_row_widget = QWidget()

            self.start_button = QPushButton("Start")
            self.start_button.setMinimumHeight(40)

            self.stop_button = QPushButton("Stop")
            self.stop_button.setMinimumHeight(40)

            # Create horizontal layout for buttons
            self.button_layout = QHBoxLayout()
            self.button_layout.addWidget(self.start_button)
            self.button_layout.addWidget(self.stop_button)

            # Set layout to the widget
            self.operation_row_widget.setLayout(self.button_layout)

            return self.operation_row_widget





    def create_launcher_row_widget(self):
            """
            Creates a QWidget containing multiple buttons for operations in the table rows.
            Returns:
                operation_row_widget (QWidget): A widget containing operation buttons.
            """
            self.launcher_row_widget = QWidget()

            # Initialize buttons
            self.rv_button = QPushButton("RV")
            self.rv_button.setMinimumHeight(40)

            self.nuke_button = QPushButton("Nuke")
            self.nuke_button.clicked.connect(self.open_nuke_file)
            self.nuke_button.setMinimumHeight(40)

            self.open_render_dir_button = QPushButton("Open Render dir")
            self.open_render_dir_button.setMinimumHeight(40)

            # Create horizontal layout for buttons
            self.button_layout = QHBoxLayout()
            self.button_layout.addWidget(self.rv_button)
            self.button_layout.addWidget(self.nuke_button)
            self.button_layout.addWidget(self.open_render_dir_button)

            # Set layout to the widget
            self.launcher_row_widget.setLayout(self.button_layout)

            return self.launcher_row_widget


























    def add_files_to_table(self):
        """
        Opens a file dialog to select Nuke files, 
        extracts file paths and names, 
        and populates them in the table widget.
        """
        # Open file dialog to select Nuke files
        selected_files = list(QFileDialog.getOpenFileNames(
            None, 
            "Select Nuke Files", 
            r"D:\GamutX\Render_Mate\Nuke_files", 
            "Nuke Files (*.nk)"
        )[0])

        # Separate file paths and names
        file_paths = []
        file_names = []

        for file in selected_files:
            file_paths.append(os.path.dirname(file))
            file_names.append(os.path.basename(file))

        # Set the number of rows in the table
        self.table_widget.setRowCount(len(file_paths))

        # Populate the table widget with file paths, names, and operation widgets
        for row in range(len(file_paths)):
            file_path_item = QTableWidgetItem(file_paths[row])
            file_name_item = QTableWidgetItem(file_names[row])

            # Align text to the center
            file_path_item.setTextAlignment(Qt.AlignCenter)
            file_name_item.setTextAlignment(Qt.AlignCenter)

            # Set items and widgets in the respective columns
            self.table_widget.setItem(row, 0, file_path_item)
            self.table_widget.setItem(row, 1, file_name_item)
            self.table_widget.setCellWidget(row, 5, self.create_operation_row_widget())
            self.table_widget.setCellWidget(row, 6, self.create_launcher_row_widget())
            progress_bar = QProgressBar()
            progress_bar.setValue(50)  # Set an initial value, you can modify it as needed
            self.table_widget.setCellWidget(row, 3, progress_bar)



    ######################################################################################
    
    
    def clear_table(self):
        """
        Removes all rows from the table widget.
        """
        self.table_widget.setRowCount(0)


    ######################################################################################
    def remove_selected_rows(self):
        """
        Removes only the selected rows from the table widget.
        """
        # Get selected rows
        selected_rows = self.table_widget.selectionModel().selectedRows()

        # Remove rows in descending order to maintain row integrity
        for row in sorted(selected_rows, reverse=True):
            self.table_widget.removeRow(row.row())


    def open_nuke_file(self):
        nuke_button_row = self.table_widget.indexAt(self.sender().parent().pos()).row()
        file_path = self.table_widget.item(nuke_button_row , 0)
        file_name = self.table_widget.item(nuke_button_row, 1)
        nuke_file = Path(Path(file_path.text()) / file_name.text()).as_posix()

        nuke_software_path = r"C:\Program Files\Nuke13.2v5\Nuke13.2.exe"
        nukeX_args = "--nukex"
        subprocess.Popen([f"{nuke_software_path}", nukeX_args , nuke_file ])





if __name__ == "__main__":
    app = QApplication()
    ui = RenderMate()
    ui.show()
    sys.exit(app.exec_())