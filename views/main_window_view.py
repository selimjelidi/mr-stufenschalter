from PySide6.QtWidgets import QMainWindow, QMessageBox
from PySide6.QtCore import QObject, Signal
import sys
import os

# Add the ressources directory to the path to import the UI
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "ressources"))
from ui_main_window import Ui_MainWindow


class MainWindowView(QMainWindow):
    """
    Main window view class that handles the UI and user interactions.
    This class follows the MVC pattern and acts as the View component.
    """

    # Signals for communicating with controllers
    arc_detection_requested = Signal()
    short_circuit_detection_requested = Signal()

    def __init__(self, parent=None):
        """
        Initialize the main window view.

        Args:
            parent: Parent widget (optional)
        """
        super(MainWindowView, self).__init__(parent)

        # Set up the UI from the generated UI file
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Connect signals to slots
        self._connect_signals()

        # Set window properties
        self.setWindowTitle("MR Detection System")

    def _connect_signals(self):
        """
        Connect UI signals to their respective slot methods.
        """
        self.ui.arcDetectionBtn.clicked.connect(self._on_arc_detection_clicked)
        self.ui.shorCircuitDetectionBtn.clicked.connect(
            self._on_short_circuit_detection_clicked
        )

    def _on_arc_detection_clicked(self):
        """
        Handle arc detection button click.
        Emits signal to notify controllers.
        """
        self.arc_detection_requested.emit()
        # self._show_info_message("Arc Detection", "Arc detection process initiated...")

    def _on_short_circuit_detection_clicked(self):
        """
        Handle short circuit detection button click.
        Emits signal to notify controllers.
        """
        self.short_circuit_detection_requested.emit()
        # self._show_info_message(
        #     "Short Circuit Detection", "Short circuit detection process initiated..."
        # )

    def _show_info_message(self, title, message):
        """
        Display an information message box.

        Args:
            title (str): Title of the message box
            message (str): Message content
        """
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.exec()

    def show_error_message(self, title, message):
        """
        Display an error message box.

        Args:
            title (str): Title of the message box
            message (str): Error message content
        """
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(QMessageBox.Icon.Critical)
        msg_box.exec()

    def show_success_message(self, title, message):
        """
        Display a success message box.

        Args:
            title (str): Title of the message box
            message (str): Success message content
        """
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.exec()

    def set_detection_buttons_enabled(self, enabled):
        """
        Enable or disable detection buttons.

        Args:
            enabled (bool): True to enable buttons, False to disable
        """
        self.ui.arcDetectionBtn.setEnabled(enabled)
        self.ui.shorCircuitDetectionBtn.setEnabled(enabled)

    def update_detection_status(self, detection_type, status):
        """
        Update the status of detection operations.
        This method can be extended to update UI elements based on detection status.

        Args:
            detection_type (str): Type of detection ("arc" or "short_circuit")
            status (str): Status of the detection process
        """
        # This method can be extended to update progress bars, status labels, etc.
        print(f"{detection_type} detection status: {status}")
