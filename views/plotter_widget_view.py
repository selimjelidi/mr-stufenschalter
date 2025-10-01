from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QComboBox, QSpinBox
from PySide6.QtCore import QTimer, Signal
import sys
import os
import numpy as np
import pyqtgraph as pg

# Add the ressources directory to the path to import the UI
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "ressources"))
from ui_plotter_widget import Ui_PlotterWidget


class PlotterWidgetView(QWidget):
    """
    Plotter widget view class that provides plotting functionality using PyQtGraph.
    This class integrates with the generated UI and adds PlotWidget functionality.
    """
    
    # Signals for data requests
    data_requested = Signal(str)  # Signal to request data for plotting
    
    def __init__(self, parent=None):
        """
        Initialize the plotter widget view.
        
        Args:
            parent: Parent widget (optional)
        """
        super(PlotterWidgetView, self).__init__(parent)
        
        # Set up the UI from the generated UI file
        self.ui = Ui_PlotterWidget()
        self.ui.setupUi(self)
        
        # Configure PyQtGraph
        pg.setConfigOptions(antialias=True)
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')
        
        # Create the plot widget
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setLabel('left', 'Amplitude', units='V')
        self.plot_widget.setLabel('bottom', 'Time', units='s')
        self.plot_widget.setTitle('MR Detection Data')
        self.plot_widget.showGrid(x=True, y=True)
        self.plot_widget.addLegend()
        
        # Add plot widget to the layout
        self.ui.verticalLayout.addWidget(self.plot_widget)
        
        # Initialize data storage
        self.plot_data = {}
        self.plot_curves = {}
        
        # Set up initial styling
        self.setStyleSheet("""
            QWidget {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 8px;
            }
        """)
        
    def _add_plot_curve(self, data_type):
        """
        Add a new plot curve for the specified data type.
        
        Args:
            data_type (str): Type of data to plot
        """
        colors = {
            "Arc Detection": 'r',
            "Short Circuit": 'b', 
            "Voltage": 'g',
            "Current": 'm',
            "Power": 'c'
        }
        
        color = colors.get(data_type, 'k')
        curve = self.plot_widget.plot(pen=color, name=data_type)
        self.plot_curves[data_type] = curve
        self.plot_data[data_type] = {'x': [], 'y': []}
        
    def plot_static_data(self, x_data, y_data, data_type, clear_existing=True):
        """
        Plot static data on the widget.
        
        Args:
            x_data: X-axis data (time or sample points)
            y_data: Y-axis data (measurements)
            data_type (str): Type of data being plotted
            clear_existing (bool): Whether to clear existing plots
        """
        if clear_existing:
            self.plot_widget.clear()
            self.plot_data.clear()
            self.plot_curves.clear()
            
        if data_type not in self.plot_curves:
            self._add_plot_curve(data_type)
            
        self.plot_data[data_type]['x'] = list(x_data)
        self.plot_data[data_type]['y'] = list(y_data)
        
        self.plot_curves[data_type].setData(x_data, y_data)
        
    def add_marker(self, x_pos, label="Marker", color='r'):
        """
        Add a vertical marker line to the plot.
        
        Args:
            x_pos: X position for the marker
            label (str): Label for the marker
            color: Color of the marker line
        """
        line = pg.InfiniteLine(pos=x_pos, angle=90, pen=color, label=label)
        self.plot_widget.addItem(line)
        
    def set_plot_labels(self, x_label="Time", y_label="Amplitude", title="Data Plot"):
        """
        Set custom labels for the plot.
        
        Args:
            x_label (str): X-axis label
            y_label (str): Y-axis label  
            title (str): Plot title
        """
        self.plot_widget.setLabel('left', y_label)
        self.plot_widget.setLabel('bottom', x_label)
        self.plot_widget.setTitle(title)
