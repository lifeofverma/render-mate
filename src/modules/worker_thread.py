from PySide2.QtCore import QObject, Signal
import subprocess

class WorkerThread(QObject):
    """
    WorkerThread is responsible for handling a background rendering task using subprocess.
    It emits signals to report progress, error, and completion status to the main thread.
    """

    progress = Signal(int)         # Emits current frame number being rendered
    error = Signal(str)            # Emits error message if any error occurs
    completed = Signal(str)        # Emits when rendering is successfully completed

    def __init__(self):
        super().__init__()
        self.process = None
        self.nuke_process = None

    def set_process_param(self , process):
        """
        Sets the render command for the subprocess.

        Args:
            process (list): Command to be executed as a subprocess
        """
        self.process = process

    def render(self):
        """
        Starts the rendering process using subprocess.
        Continuously reads stdout to emit frame progress.
        Emits completion or error signals based on process result.
        """
        try:
            with subprocess.Popen(self.process, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) as nuke_process:
                self.nuke_process = nuke_process

                # Read and emit progress from stdout
                for line in nuke_process.stdout:
                    if line.startswith('Frame '):
                        frame_num = (int(line.split()[1]))
                        self.progress.emit(frame_num)

                # Emit error if any stderr lines are detected
                for error in nuke_process.stderr:
                    if error:
                        self.error.emit("Error")

                # Wait for process to complete
                nuke_process.wait()

                # Emit completed signal if process finished successfully
                if nuke_process.returncode == 0:
                    self.completed.emit("Completed")

        except Exception as e:
            # Log any unexpected exception for debugging
            print(f"Exception occurred: {str(e)}")

        finally:
           # Clear reference to the process
           self.nuke_process = None

    def terminate_process(self):
        """
        Terminates the currently running subprocess if it's still active.
        """
        if self.nuke_process and self.nuke_process.poll() is None:
            self.nuke_process.terminate()