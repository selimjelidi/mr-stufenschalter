from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QProgressBar,
    QTextEdit,
    QFrame,
    QGridLayout,
    QSpinBox,
    QDoubleSpinBox,
    QCheckBox,
)
from PySide6.QtCore import QObject, QTimer
from PySide6.QtGui import QFont
import random
import numpy as np
from views.main_window_view import MainWindowView
from views.plotter_widget_view import PlotterWidgetView


class MainWindowController(QObject):
    """
    Controller class for the main window that manages the interaction between
    the view and the detection widgets.
    """

    def __init__(self):
        super().__init__()
        # Create and show the main window
        self.view = MainWindowView()
        self.current_widget = None

        # Connect to view signals
        self.view.arc_detection_requested.connect(self.show_arc_detection_ui)
        self.view.short_circuit_detection_requested.connect(
            self.show_short_circuit_detection_ui
        )

    def show_arc_detection_ui(self):
        """
        Show the Arc Detection UI in the main widget area.
        """
        self.clear_current_widget()

        # Create plotter widget for arc detection
        self.current_widget = PlotterWidgetView()
        self.current_widget.set_plot_labels(
            x_label="Time (s)", y_label="Arc Signal (V)", title="Arc Detection Analysis"
        )

        # Generate sample arc detection data
        time_data = np.linspace(0, 10, 1000)
        arc_data = 0.1 + 0.05 * np.sin(2 * np.pi * 0.5 * time_data)

        # Add some arc events
        for i in [200, 450, 750]:
            arc_data[i : i + 20] += np.random.uniform(0.5, 1.0, 20)

        # Add noise
        arc_data += np.random.normal(0, 0.02, len(arc_data))

        self.current_widget.plot_static_data(time_data, arc_data, "Arc Detection")

        # Add markers for detected arcs
        self.current_widget.add_marker(2.0, "Arc Event 1", "r")
        self.current_widget.add_marker(4.5, "Arc Event 2", "r")
        self.current_widget.add_marker(7.5, "Arc Event 3", "r")

        self.view.ui.mainWidgetLayout.addWidget(self.current_widget)
        # Update the main widget style
        self.view.ui.mainWidget.setStyleSheet(
            "QWidget { background-color: transparent; }"
        )

        print("Arc Detection UI with plotter displayed")

    def show_short_circuit_detection_ui(self):
        """
        Show the Short Circuit Detection UI in the main widget area.
        """
        self.clear_current_widget()

        # Create plotter widget for short circuit detection
        self.current_widget = PlotterWidgetView()
        self.current_widget.set_plot_labels(
            x_label="Time (s)",
            y_label="Current (A)",
            title="Short Circuit Detection Analysis",
        )

        # Generate sample short circuit detection data
        time_data = np.linspace(0, 5, 500)
        current_data = 10 + 2 * np.sin(2 * np.pi * 50 * time_data)  # Normal AC current

        # Add short circuit events
        for i in [150, 350]:
            current_data[i : i + 10] += np.random.uniform(
                40, 80, 10
            )  # High current spikes

        # Add noise
        current_data += np.random.normal(0, 0.5, len(current_data))

        self.current_widget.plot_static_data(time_data, current_data, "Short Circuit")

        # Add markers for detected short circuits
        self.current_widget.add_marker(1.5, "Short Circuit 1", "b")
        self.current_widget.add_marker(3.5, "Short Circuit 2", "b")

        # Add the widget to the main widget area
        self.view.ui.mainWidgetLayout.addWidget(self.current_widget)

        # Update the main widget style
        self.view.ui.mainWidget.setStyleSheet(
            "QWidget { background-color: transparent; }"
        )

        print("Short Circuit Detection UI with plotter displayed")

    def clear_current_widget(self):
        """
        Clear the current widget from the main widget area.
        """
        # Clear current widget reference first
        if self.current_widget:
            self.current_widget.setParent(None)
            self.current_widget.deleteLater()
            self.current_widget = None
            
        # Clear the layout contents safely
        layout = self.view.ui.mainWidgetLayout
        if layout:
            while layout.count():
                child = layout.takeAt(0)
                if child.widget():
                    child.widget().setParent(None)
                    child.widget().deleteLater()
