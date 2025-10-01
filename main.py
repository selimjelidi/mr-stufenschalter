#!/usr/bin/env python3
"""
Main entry point for the MR Detection System application.
"""

import sys
from PySide6.QtWidgets import QApplication
from controllers.main_window_controller import MainWindowController


def main():
    """
    Main function to run the MR Detection System application.
    """
    # Create the Qt application
    app = QApplication(sys.argv)

    # Create the controller and connect it to the view
    controller = MainWindowController()
    controller.view.show()

    # Run the application event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
