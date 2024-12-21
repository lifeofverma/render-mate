# **Project Name**
RenderMate

## **Project Description**
AutoNukeRender is a tool designed to streamline the rendering process for multiple Nuke scripts without the need to open each file manually. It allows users to manage and execute renders for multiple Nuke scripts in a single, efficient workflow. 

This tool is especially helpful for freelancers and small teams, offering a local render-farm-style experience, empowering their rendering processes, and boosting productivity.

---

## **Goals**
The primary goal of AutoNukeRender is to simplify and automate the rendering process for Nuke artists. It is designed to:
- Save time by eliminating the need to manually open and render multiple Nuke scripts.
- Provide a local render farm experience for users.
- Empower freelancers and small teams globally to manage and execute renders efficiently.

---

## **Features**
AutoNukeRender provides a user-friendly interface with the following key features:

### **Main Functionalities**
1. **Add File**
   - Opens a popup window to browse and select `.nk` files for rendering.
   - Selected files are added to a list displayed in the main UI.

2. **Remove File**
   - Allows the user to select and remove specific files from the list, excluding them from the rendering process.

3. **Remove All**
   - Clears all files from the list.

4. **Render All**
   - Starts rendering all files listed in the UI simultaneously.

5. **Pause All**
   - Pauses the rendering process for all files currently being processed.

---

### **UI Information**
The tool provides comprehensive details about each file in the list:
- **File Path:** Displays the full file path of the `.nk` script.
- **File Name:** Shows the name of the `.nk` script.
- **Open Directory:** Opens the folder containing the Nuke file.

### **Write Nodes Selection**
- Allows users to choose specific Write Nodes to render when a script contains multiple nodes.

### **Render Progress and Status**
- **Progress:** Displays the progress of the render for each file as a percentage.
- **Status:** Indicates the current render state:
  - `Complete`: Render finished successfully.
  - `On Queue`: The render is waiting in the queue to start.
  - `In Progress`: Render is ongoing.
  - `Error`: Render encountered an issue.
  - `Paused`: Render is paused.
  - `Stopped`: Render was terminated.

---

### **Operations**
AutoNukeRender includes several actions for each file:
- **RV Player Button:** Opens the rendered data directly in RV Player for preview.
- **Nuke Button:** Opens the rendered file in Nuke for further adjustments.
- **Play Button:** Starts the render for the selected file.
- **Pause Button:** Pauses the render for the selected file.
- **Stop Button:** Stops the render completely. Restarting the render will begin from the first frame.
- **Open Directory:** Opens the directory containing the rendered output.

---

## **How to Use**
1. Launch AutoNukeRender.
2. Use the **Add File** button to select `.nk` files for rendering.
3. Manage your file list using:
   - **Remove File**: Remove a specific file from the list.
   - **Remove All**: Clear the entire file list.
4. Choose specific Write Nodes if needed.
5. Click **Render All** to begin rendering or use the Play button for individual files.
6. Monitor progress and status in the UI.
7. Use the operation buttons (RV Player, Nuke, etc.) for post-render tasks.

---

## **Getting Started**
To start using AutoNukeRender, ensure you have the following:
- **The Foundry Nuke:** Installed on your system.
- **RV Player:** Installed on your system to oens the rendered data directly in RV Player for preview .
- **Python 3:** The tool is built with Python (PySide2 or PyQt5 for the UI).