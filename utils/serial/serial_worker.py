import serial
from PySide6.QtCore import QObject, Signal, QThread, QMutex, QMutexLocker
from typing import Dict, Set, Callable, Optional, Any
from dataclasses import dataclass
from queue import Queue
from utils.serial.types import PacketConfig
import time


class SerialWorker(QObject):
    """Worker class that handles serial communication in a separate thread"""

    # Signals for communication with main thread
    packet_ready = Signal(bytes, object)  # packet data and config
    error_occurred = Signal(str)
    desync_detected = Signal(int)
    connection_status = Signal(bool)

    def __init__(self, port: str, baudrate: int = 115200):
        super().__init__()
        self.port = port
        self.baudrate = baudrate
        self.ser = None
        self.buffer = bytearray()
        self.running = False
        self.packet_configs = {}
        self.packet_stats = {}
        self.config_mutex = QMutex()

    def initialize_serial(self):
        """Initialize serial connection"""
        try:
            self.ser = serial.Serial(
                self.port,
                baudrate=self.baudrate,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_EVEN,
                stopbits=serial.STOPBITS_ONE,
                timeout=0.1,  # Non-blocking with short timeout
            )
            self.connection_status.emit(True)
            return True
        except serial.SerialException as e:
            self.error_occurred.emit(f"Failed to initialize serial: {e}")
            self.connection_status.emit(False)
            return False

    def update_packet_configs(self, configs: Dict[int, PacketConfig], stats: Dict):
        """Update packet configurations (thread-safe)"""
        with QMutexLocker(self.config_mutex):
            self.packet_configs = configs.copy()
            self.packet_stats = stats.copy()

    def start_reading(self):
        """Start the reading loop"""
        if not self.initialize_serial():
            return

        self.running = True
        self._read_loop()

    def stop_reading(self):
        """Stop the reading loop"""
        self.running = False
        if self.ser and self.ser.is_open:
            self.ser.close()
        self.connection_status.emit(False)

    def send_data(self, data: bytes):
        """Send data through serial port"""
        if self.ser and self.ser.is_open:
            try:
                self.ser.write(data)
            except serial.SerialException as e:
                self.error_occurred.emit(f"Failed to send data: {e}")

    def _read_loop(self):
        """Main reading loop running in worker thread"""
        while self.running:
            try:
                if not self.ser or not self.ser.is_open:
                    break

                # Read available data
                data = self.ser.read(self.ser.in_waiting or 1)
                if not data:
                    continue

                self.buffer.extend(data)
                self._process_buffer()

            except serial.SerialException as e:
                self.error_occurred.emit(f"Serial exception: {e}")
                self.running = False
                break
            except Exception as e:
                self.error_occurred.emit(f"Unexpected exception: {e}")
                self.running = False
                break

    def _process_buffer(self):
        """Process the buffer to extract packets based on configured headers"""
        with QMutexLocker(self.config_mutex):
            configs = self.packet_configs.copy()

        while len(self.buffer) > 0:
            # Check if we have a valid header
            header = self.buffer[0]
            config = configs.get(header)

            if config is None:
                # Unknown header, drop byte and continue
                self.desync_detected.emit(header)
                self.buffer.pop(0)
                continue

            # Check if we have enough bytes for this packet type
            if len(self.buffer) < config.size:
                # Not enough data yet, wait for more
                break

            # Extract the packet
            packet = bytes(self.buffer[: config.size])
            self.buffer = self.buffer[config.size :]

            # Emit packet for processing in main thread
            self.packet_ready.emit(packet, config)
