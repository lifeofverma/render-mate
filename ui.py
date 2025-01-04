# Import modules
import sys
from getpass import getuser
import os
from pathlib import Path 
import subprocess
import json

# Importing third party modules
from PySide2.QtWidgets import QApplication, QInputDialog, QMessageBox, QComboBox, QSpacerItem,QSizePolicy, QMainWindow, QProgressBar, QMenuBar, QWidget, QPushButton, QVBoxLayout,  QHBoxLayout, QLabel, QTableWidget, QFileDialog, QTableWidgetItem, QHeaderView
from PySide2.QtGui import QPixmap, QIcon
from PySide2.QtCore import Qt , QSize

# Importing custom modules
from constants.constants import NUKE_ICON, USER_ICON, ADD_ICON, REMOVE_ICON, REMOVE_SELECTED_ICON, PLAY_ICON, STOP_ICON, OPERATION_PLAY_ICON, OPERATION_STOP_ICON, OPEN_DIR_ICON, RV_ICON
from modules.PathManager import PathManager
from modules.NukeFileReader import GetNukeFileProperties


class RenderMate(QMainWindow):
    def __init__(self):
        super().__init__()


        self.setWindowTitle("RenderMate V1.0.0")
        self.setMinimumSize(1600, 800)
        self.menu_bar = QMenuBar()        
        self.setMenuBar(self.menu_bar)
        self.set_path = self.menu_bar.addMenu("Set Path")
        self.set_nuke_path_action = self.set_path.addAction("Set Nuke Path")
        self.set_rv_player_path_action = self.set_path.addAction("Set RV Player Path")

        self.set_nuke_path_action.triggered.connect(self.nuke_path_action)
        self.set_rv_player_path_action.triggered.connect(self.rv_player_path_action)


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
        self.side_bar_widget = QWidget()
        self.side_bar_widget.setFixedWidth(105)
        # self.side_bar.setStyleSheet("background-color: #323232;")
        
        # Create buttons
        self.add_button = QPushButton()
        self.add_button.setFlat(True)
        self.remove_selected = QPushButton()
        self.remove_all = QPushButton()
        self.start_all = QPushButton()
        self.stop_all = QPushButton()



        self.add_button.clicked.connect(self.add_files_to_table)
        self.remove_all.clicked.connect(self.clear_table)
        self.remove_selected.clicked.connect(self.remove_selected_rows)
        self.start_all.clicked.connect(self.render_all)

        # set buttons icons
        self.add_button.setIcon(QIcon(ADD_ICON))
        self.start_all.setIcon(QIcon(PLAY_ICON))
        self.stop_all.setIcon(QIcon(STOP_ICON))
        self.remove_all.setIcon(QIcon(REMOVE_ICON))
        self.remove_selected.setIcon(QIcon(REMOVE_SELECTED_ICON))



        self.add_button.setIconSize(QSize(40, 40)) 
        self.remove_selected.setIconSize(QSize(40, 40)) 
        self.remove_all.setIconSize(QSize(60, 40)) 
        self.start_all.setIconSize(QSize(40, 40)) 
        # self.stop_all.setStyleSheet("QPushButton { border: none; }") 
        self.stop_all.setIconSize(QSize(40, 40)) 
        


        # Create labels for buttons
        self.add_label = QLabel("Add")
        self.add_label.setFixedHeight(40)
        self.remove_all_label = QLabel("Remove all")
        self.remove_selected_label = QLabel("Remove Selected")
        self.start_all_label = QLabel("Start all")
        self.stop_all_label = QLabel("Stop all")
        
        self.add_label.setFixedHeight(20)
        self.remove_selected_label.setFixedHeight(30)
        self.remove_all_label.setFixedHeight(10)
        self.start_all_label.setFixedHeight(20)
        self.stop_all_label.setFixedHeight(20)

        
        self.add_label.setAlignment(Qt.AlignCenter)
        self.remove_selected_label.setAlignment(Qt.AlignCenter)
        self.remove_all_label.setAlignment(Qt.AlignCenter)
        self.start_all_label.setAlignment(Qt.AlignCenter)
        self.stop_all_label.setAlignment(Qt.AlignCenter)




        # Create individual layouts for each button and label pair
        self.add_layout = QVBoxLayout()
        self.add_layout.setSpacing(0)
        self.add_layout.addWidget(self.add_button)
        self.add_layout.addWidget(self.add_label)

        self.remove_all_layout = QVBoxLayout()
        self.remove_all_layout.setSpacing(0)
        self.remove_all_layout.addWidget(self.remove_all)
        self.remove_all_layout.addWidget(self.remove_all_label)

        self.remove_selected_layout = QVBoxLayout()
        self.remove_selected_layout.setSpacing(0)
        self.remove_selected_layout.addWidget(self.remove_selected)
        self.remove_selected_layout.addWidget(self.remove_selected_label)

        self.start_all_layout = QVBoxLayout()
        self.start_all_layout.setSpacing(0)
        self.start_all_layout.addWidget(self.start_all)
        self.start_all_layout.addWidget(self.start_all_label)
        

        self.stop_all_layout = QVBoxLayout()
        self.stop_all_layout.setSpacing(0)
        self.stop_all_layout.addWidget(self.stop_all)
        self.stop_all_layout.addWidget(self.stop_all_label)

        # Create the main layout and add each button layout
        self.side_bar_main_layout = QVBoxLayout()
        self.side_bar_main_layout.addLayout(self.add_layout)
        self.side_bar_main_layout.addLayout(self.remove_all_layout)
        self.side_bar_main_layout.addLayout(self.remove_selected_layout)
        self.side_bar_main_layout.addLayout(self.start_all_layout)
        self.side_bar_main_layout.addLayout(self.stop_all_layout)
        
        # Create a spacer item with a fixed height
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        # Add the spacer before the sidebar widget in the layout
        self.side_bar_main_layout.addItem(spacer)
        # set Layout for sidebar buttons
        self.side_bar_widget.setLayout(self.side_bar_main_layout)


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
        self.hbox_layout.addWidget(self.side_bar_widget)
        self.hbox_layout.addWidget(self.table_widget)

        # Main layout setup
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.header)
        main_layout.addLayout(self.hbox_layout)
        self.central_widget.setLayout(main_layout) 




        self.status_label_list = ["In Progress" , "completed" , "Stopped" , "Error"]

    def render_status_label_widget(self):
        self.status_label = QLabel("On Que")
        self.status_label.setAlignment(Qt.AlignCenter)
        return self.status_label


    def progress_bar_creator(self):
        self.progress_bar = QProgressBar()
        return self.progress_bar


    #############################################################################################################################################
    def create_operation_row_widget(self):
            """
            Creates a QWidget containing multiple buttons for operations in the table rows.
            
            Returns:
                operation_row_widget (QWidget): A widget containing operation buttons.
            """
            self.operation_row_widget = QWidget()

            self.start_button = QPushButton("")
            self.start_button.setIcon(QIcon(OPERATION_PLAY_ICON))
            self.start_button.setIconSize(QSize(40, 40)) 
            self.start_button.setMinimumHeight(40)
            self.start_button.clicked.connect(self.render_selected)  

            self.stop_button = QPushButton("")
            self.stop_button.setIcon(QIcon(OPERATION_STOP_ICON))
            self.stop_button.setIconSize(QSize(40, 40)) 
            self.stop_button.setMinimumHeight(40)
            self.stop_button.clicked.connect(self.stop_render_button) 
            
            # Create horizontal layout for buttons
            self.button_layout = QHBoxLayout()
            self.button_layout.addWidget(self.start_button)
            self.button_layout.addWidget(self.stop_button)

            # Set layout to the widget
            self.operation_row_widget.setLayout(self.button_layout)

            return self.operation_row_widget

    ######################################################################################
    def create_launcher_row_widget(self):
            """
            Creates a QWidget containing multiple buttons for launcher in the table rows.
            
            Returns:
                create_launcher_row_widget (QWidget): A widget containing operation buttons.
            """
            self.launcher_row_widget = QWidget()

            # Initialize buttons
            self.rv_button = QPushButton("")
            self.rv_button.setIcon(QIcon(RV_ICON))
            self.rv_button.setIconSize(QSize(40, 40)) 
            self.rv_button.setFlat(True)
            self.rv_button.setMinimumHeight(40)

            self.nuke_button = QPushButton("")
            self.nuke_button.setIcon(QIcon(NUKE_ICON))
            self.nuke_button.setFlat(True)
            self.nuke_button.setIconSize(QSize(40, 40)) 
            self.nuke_button.clicked.connect(self.open_nuke_file)
            self.nuke_button.setMinimumHeight(40)

            self.open_render_dir = QPushButton("")
            self.open_render_dir.setFlat(True)
            self.open_render_dir.setIcon(QIcon(OPEN_DIR_ICON))
            self.open_render_dir.setIconSize(QSize(40, 40)) 
            self.open_render_dir.setMinimumHeight(40)
            self.open_render_dir.clicked.connect(self.open_render_dir_button)

            # Create horizontal layout for buttons
            self.button_layout = QHBoxLayout()
            self.button_layout.addWidget(self.rv_button)
            self.button_layout.addWidget(self.nuke_button)
            self.button_layout.addWidget(self.open_render_dir)

            # Set layout to the widget
            self.launcher_row_widget.setLayout(self.button_layout)

            return self.launcher_row_widget









    # Define a function to prompt the user for the Nuke executable path and update it
    def nuke_path_action(self):
        """
        Prompt the user to enter the Nuke executable path
        and update it in the path configuration.
        """

        nuke_path, user_confirmed = QInputDialog.getText(self, "Set Nuke Path", "Enter the Nuke executable path:")

        # Check if the user clicked OK Update the Nuke path in the JSON file
        if user_confirmed and nuke_path.strip():  
            path_manager = PathManager()
            path_manager.set_nuke_path(nuke_path)








    # Define a function to prompt the user for the RV Player executable path and update it
    def rv_player_path_action(self):
        """
        Prompt the user to enter the RV player executable path
        and update it in the path configuration.
        """
        rv_player_path, user_confirmed = QInputDialog.getText(self, "Set RV Player Path", "Enter the RV player executable path:")

         # Check if the user clicked OK Update the RV Player path in the JSON file
        if user_confirmed: 
            path_manager = PathManager()
            path_manager.set_rv_player_path(rv_player_path)






    ######################################################################################
    def add_files_to_table(self):
        """
        Opens a file dialog to select Nuke files, 
        extracts file paths and names, 
        and populates them in the table widget.
        """

        # Open file dialog to select Nuke files
        self.selected_files = list(QFileDialog.getOpenFileNames(
            None, 
            "Select Nuke Files", 
            r"D:\GamutX\Render_Mate\Nuke_files", 
            "Nuke Files (*.nk)"
        )[0])

        # Separate file paths and names
        file_paths = []
        file_names = []

        for file in self.selected_files:
            file_paths.append(os.path.dirname(file))
            file_names.append(os.path.basename(file))

        # Set the number of rows in the table to match the number of selected files
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
            self.table_widget.setCellWidget(row, 3, self.progress_bar_creator())
            self.table_widget.setCellWidget(row, 4, self.render_status_label_widget())


        # Set write nodes name in the respective columns
        for row, nuke_file in enumerate(self.selected_files):
            # Create a widget to display write nodes or a message and Fetch the list of write nodes from the Nuke file
            write_nodes_widget = QComboBox()
            nuke_file_reader = GetNukeFileProperties(nuke_file)
            write_node_names = nuke_file_reader.get_write_nodes_name()

            # Populate the combo box with the write nodes OR Set a QLabel with "No write nodes found" message
            if write_node_names:
                write_nodes_widget.addItems(write_node_names)
                self.table_widget.setCellWidget(row, 2, write_nodes_widget)
            
            else:
                no_nodes_label = QLabel("No write nodes found")
                no_nodes_label.setAlignment(Qt.AlignCenter)
                self.table_widget.setCellWidget(row, 2, no_nodes_label)






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






    ######################################################################################
    def open_nuke_file(self):
        """
        Opens the selected Nuke file using the Nuke software.

        This function determines which row in the table the 'Open in Nuke' button
        was clicked, retrieves the file path and name, and launches Nuke with 
        the selected script.
        """

        # Get the row of the clicked button within the table
        selected_row  = self.table_widget.indexAt(self.sender().parent().pos()).row()

        # Retrieve the file path and file name from the respective table columns
        file_path = self.table_widget.item(selected_row  , 0)
        file_name = self.table_widget.item(selected_row , 1)

        # Combine file path and file name to get the full path of the Nuke file
        nuke_file_path  = Path(Path(file_path.text()) / file_name.text()).as_posix()

        # Define the path to the Nuke executable and the required arguments
        path_manager = PathManager()
        nuke_executable_path  = path_manager.get_nuke_path()
        nukeX_arguments  = "--nukex"

        subprocess.Popen([f"{nuke_executable_path}", nukeX_arguments , nuke_file_path  ] , creationflags= subprocess.CREATE_NEW_CONSOLE)







    ######################################################################################
    def render_selected(self, selected_row=None):
        """
        Trigger the rendering of the selected Nuke file with a chosen write node.

        This method identifies the row in the table where the render operation was triggered, 
        retrieves the corresponding file path and name, and renders the script using the 
        selected write node from the combo box. If no write nodes are available, it shows 
        a warning popup.

        """

        if selected_row is None:
        # Identify the table row where the button was clicked
            selected_row  = self.table_widget.indexAt(self.sender().parent().pos()).row()

        # Retrieve file path and name from the selected row in the table
        file_path = self.table_widget.item(selected_row  , 0)
        file_name = self.table_widget.item(selected_row , 1)
        render_status = self.table_widget.cellWidget(selected_row  , 4)
        render_status.setText(self.status_label_list[0])  

       # Construct the full path to the Nuke script and Path to the Nuke executable
        nuke_file_path  = Path(Path(file_path.text()) / file_name.text()).as_posix()

        # Initialize PathManager, retrieve Nuke file properties, and get Nuke executable path
        path_manager = PathManager()
        nuke_file_properties = GetNukeFileProperties(nuke_file_path)
        nuke_executable_path  = path_manager.get_nuke_path()
        

        # Retrieve the write node combo box from the selected row (column index 2)
        write_nodes = self.table_widget.cellWidget(selected_row , 2)
        
        # Check if the combo box exists and is valid, Get the selected write node, Prepare the rendering command
        if write_nodes and isinstance(write_nodes , QComboBox):
            selected_write_node = write_nodes.currentText()
            frame_range = nuke_file_properties.get_frame_range(selected_write_node)

            # Check if the frame range contains "None" (indicating it's not set), then show a warning message
            if "None" in frame_range:
                QMessageBox.warning(None, "Limit Range Not Set", "The limit range is not specified in the write node.")

            # Construct the Nuke render command with the selected write node and frame range, then execute it
            else:
                start_frame = int(frame_range.split('-')[0])
                end_frame = int(frame_range.split('-')[1])
                progress_bar = self.table_widget.cellWidget(selected_row  , 3)
                progress_bar.setRange(start_frame , end_frame)
                command = [nuke_executable_path, '-t' , '-X', selected_write_node, '-F', f"{frame_range}", nuke_file_path ]

                with subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) as process:                                        
                    for line in process.stdout:
                        if line.startswith('Frame '):
                            progress_bar.setValue(int(line.split()[1]))

                    for error in process.stderr:
                        if error:
                            render_status.setText(self.status_label_list[3])

                    process.wait()
     
                    if process.returncode == 0:
                        render_status.setText(self.status_label_list[1]) 

        # Display a warning if no write nodes are found in the script
        else:
            QMessageBox.warning(None, "No Write Nodes Found", "The selected script doesn't have any write nodes.")













    def open_render_dir_button(self):
        # Identify the table row where the button was clicked
        selected_row  = self.table_widget.indexAt(self.sender().parent().pos()).row()
        # Retrieve file path and name from the selected row in the table
        file_path = self.table_widget.item(selected_row  , 0)
        file_name = self.table_widget.item(selected_row , 1)

       # Construct the full path to the Nuke script and Path to the Nuke executable
        nuke_file_path  = Path(Path(file_path.text()) / file_name.text()).as_posix()
        nuke_file_reader = GetNukeFileProperties(nuke_file_path)
        
        write_nodes = self.table_widget.cellWidget(selected_row , 2)
        
        # Check if the combo box exists and is valid, Get the selected write node, Prepare the rendering command
        if write_nodes and isinstance(write_nodes , QComboBox):
            selected_write_node = write_nodes.currentText()
            dir_path = nuke_file_reader.get_file_path(selected_write_node)
            if dir_path:
                if os.path.exists(os.path.dirname(dir_path)):
                    os.startfile(os.path.dirname(dir_path))
                else:
                    QMessageBox.warning(None, "Invalid path", "Path is Invalid!")
            else:
                QMessageBox.warning(None, "No paths Found", "The selected write Node doesn't have any directory path.")





    def render_all(self):
        """
        Trigger the rendering of all Nuke files in the table, one by one.

        This method loops through each row in the table and calls the render_selected method
        to render the Nuke scripts with the selected write nodes.
        """
        total_rows = self.table_widget.rowCount()  # Get the total number of rows in the table
        for row in range(total_rows):
            # Call render_selected to render the script for the current row
            self.render_selected(selected_row=row)









    def stop_render_button(self):
            # Identify the table row where the button was clicked
            selected_row  = self.table_widget.indexAt(self.sender().parent().pos()).row()
            render_status = self.table_widget.cellWidget(selected_row  , 4)
            if render_status.text() == self.status_label_list[0]:
                print("rg")




if __name__ == "__main__":
    app = QApplication()
    ui = RenderMate()
    ui.show()
    sys.exit(app.exec_())