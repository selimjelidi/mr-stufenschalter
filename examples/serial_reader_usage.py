#!/usr/bin/env python3
"""
Example usage of the enhanced SerialReader class with multiple queue processes
and dynamic headers for different purposes.
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.serial.serial_reader import SerialReader, PacketConfig
from PySide6.QtCore import QObject, Signal, QCoreApplication
from queue import Queue
import time


class ArcDetectionProcessor(QObject):
    """Example processor for arc detection packets"""

    arc_detected = Signal(float)  # Signal with arc intensity

    def __init__(self):
        super().__init__()
        self.arc_queue = Queue()

    def process_arc_packet(self, packet: bytes):
        """Process arc detection packet"""
        if len(packet) >= 5:
            # Example: extract arc intensity from bytes 1-4 (little endian float)
            intensity = int.from_bytes(packet[1:5], byteorder="little") / 1000.0
            print(f"Arc Detection: Intensity = {intensity:.3f}")
            self.arc_detected.emit(intensity)


class ShortCircuitProcessor(QObject):
    """Example processor for short circuit detection packets"""

    short_circuit_detected = Signal(int, float)  # Signal with location and current

    def __init__(self):
        super().__init__()
        self.sc_queue = Queue()

    def process_sc_packet(self, packet: bytes):
        """Process short circuit detection packet"""
        if len(packet) >= 6:
            # Example: extract location (byte 1) and current (bytes 2-5)
            location = packet[1]
            current = int.from_bytes(packet[2:6], byteorder="little") / 100.0
            print(f"Short Circuit: Location = {location}, Current = {current:.2f}A")
            self.short_circuit_detected.emit(location, current)


class TemperatureProcessor(QObject):
    """Example processor for temperature monitoring packets"""

    temperature_updated = Signal(int, float)  # Signal with sensor ID and temperature

    def __init__(self):
        super().__init__()
        self.temp_queue = Queue()

    def process_temp_packet(self, packet: bytes):
        """Process temperature monitoring packet"""
        if len(packet) >= 4:
            # Example: extract sensor ID (byte 1) and temperature (bytes 2-3)
            sensor_id = packet[1]
            temp = int.from_bytes(packet[2:4], byteorder="little") / 10.0
            print(f"Temperature: Sensor {sensor_id} = {temp:.1f}°C")
            self.temperature_updated.emit(sensor_id, temp)


def example_basic_usage():
    """Example of basic SerialReader usage with manual configuration"""
    print("=== Basic Usage Example ===")

    # Create reader
    reader = SerialReader("/dev/ttyUSB0", baudrate=115200)

    # Create a basic queue for all packets
    basic_queue = Queue()

    # Configure some basic packet types
    reader.add_packet_config(
        header=0xA0,
        size=21,
        queue=basic_queue,
        signal=reader.packet_received,
        name="Basic_A0",
    )
    reader.add_packet_config(
        header=0xB0,
        size=21,
        queue=basic_queue,
        signal=reader.packet_received,
        name="Basic_B0",
    )

    # Connect to the signal
    reader.packet_received.connect(
        lambda packet: print(f"Basic packet: {packet.hex()}")
    )

    # Start reading
    reader.start()

    # Simulate some work
    time.sleep(2)

    # Stop reading
    reader.stop()
    print("Basic usage example completed\n")


if __name__ == "__main__":
    app = QCoreApplication(sys.argv)

    print("SerialReader Basic Usage Examples")
    print("=" * 50)

    # Note: These examples assume a serial device is connected
    # In real usage, replace "/dev/ttyUSB0" with your actual serial port

    try:
        print("Running Qt-based basic example...")
        print("(This will attempt to connect to /dev/ttyUSB0)")
        print("Press Ctrl+C to stop if no device is connected")

        # Run the Qt-based example
        example_basic_usage()

        # Start the Qt event loop
        app.exec()

    except KeyboardInterrupt:
        print("\nExample interrupted by user")
    except Exception as e:
        print(f"Error running examples: {e}")
        print("Make sure your serial device is connected and accessible")
        print("\nTo run these examples with a real serial device:")
        print("1. Connect your serial device")
        print("2. Update the port name in the examples")
        print("3. Run this script")
