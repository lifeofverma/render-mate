from PySide2.QtCore import QObject, Signal
import subprocess

class WorkerThread(QObject):
    progress = Signal(int)
    error = Signal(str)
    completed = Signal(str)

    def __init__(self):
        super().__init__()
        self.process = None

    def set_process_param(self , process):
        self.process = process

    def render(self):
        with subprocess.Popen(self.process, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) as nuke_process:
            for line in nuke_process.stdout:
                if line.startswith('Frame '):
                    frame_num = (int(line.split()[1]))
                    self.progress.emit(frame_num)

            for error in nuke_process.stderr:
                if error:
                    self.error.emit("Error")

            nuke_process.wait()

            if nuke_process.returncode == 0:
                self.completed.emit("Completed") 
