from PySide6.QtCore import QObject, Signal, QThread
from typing import Dict, Callable, Optional, Any
from queue import Queue
import time
from utils.serial.serial_worker import SerialWorker
from utils.serial.types import PacketConfig


class SerialReader(QObject):
    """Main SerialReader class using Qt threading"""

    # Public signals
    packet_received = Signal(bytes)
    error_occurred = Signal(str)
    connection_status_changed = Signal(bool)
    desync_detected = Signal(int)

    def __init__(self, port: str, baudrate: int = 115200):
        super().__init__()

        # Configuration
        self.port = port
        self.baudrate = baudrate

        # Packet configuration management
        self.packet_configs: Dict[int, PacketConfig] = {}
        self.packet_stats = {}  # Statistics for each packet type

        # Qt threading components
        self.worker_thread = QThread()
        self.worker = SerialWorker(port, baudrate)

        # Move worker to thread
        self.worker.moveToThread(self.worker_thread)

        # Connect worker signals
        self._connect_worker_signals()

        # Update worker with initial configuration
        self._sync_worker_config()

    def _connect_worker_signals(self):
        """Connect worker signals to main thread handlers"""
        self.worker.packet_ready.connect(self._handle_packet)
        self.worker.error_occurred.connect(self.error_occurred.emit)
        self.worker.connection_status.connect(self.connection_status_changed.emit)
        self.worker.desync_detected.connect(self._handle_desync)

        # Connect thread lifecycle
        self.worker_thread.started.connect(self.worker.start_reading)
        self.worker_thread.finished.connect(self.worker.stop_reading)

    def _sync_worker_config(self):
        """Synchronize packet configuration with worker thread"""
        self.worker.update_packet_configs(self.packet_configs, self.packet_stats)

    def start(self):
        """Start the serial reading in worker thread"""
        if not self.worker_thread.isRunning():
            self.worker_thread.start()

    def stop(self):
        """Stop the serial reading and worker thread"""
        if self.worker_thread.isRunning():
            # Request worker to stop
            self.worker.stop_reading()
            # Wait for thread to finish
            self.worker_thread.quit()
            self.worker_thread.wait(5000)  # Wait up to 5 seconds

    def add_packet_config(
        self,
        header: int,
        size: int,
        queue: Queue,
        callback: Optional[Callable[[bytes], None]] = None,
        signal: Optional[Signal] = None,
        name: str = "",
    ):
        """Add a new packet configuration for a specific header"""
        if not name:
            name = f"Packet_{header:02X}"

        config = PacketConfig(
            header=header,
            size=size,
            queue=queue,
            callback=callback,
            signal=signal,
            name=name,
        )

        self.packet_configs[header] = config
        self.packet_stats[header] = {"count": 0, "last_received": None, "errors": 0}
        print(
            f"[CONFIG] Added packet config for header 0x{header:02X}: {name} (size: {size})"
        )

        # Sync with worker thread
        self._sync_worker_config()

    def remove_packet_config(self, header: int):
        """Remove a packet configuration"""
        if header in self.packet_configs:
            name = self.packet_configs[header].name
            del self.packet_configs[header]
            del self.packet_stats[header]
            print(f"[CONFIG] Removed packet config for header 0x{header:02X}: {name}")

            # Sync with worker thread
            self._sync_worker_config()

    def get_packet_stats(self) -> Dict[int, Dict[str, Any]]:
        """Get statistics for all packet types"""
        return self.packet_stats.copy()

    def clear_packet_configs(self):
        """Clear all packet configurations"""
        self.packet_configs.clear()
        self.packet_stats.clear()
        print("[CONFIG] Cleared all packet configurations")

        # Sync with worker thread
        self._sync_worker_config()

    def get_queue_for_header(self, header: int) -> Optional[Queue]:
        """Get the queue associated with a specific header"""
        config = self.packet_configs.get(header)
        return config.queue if config else None

    def send_signal(self, signal_bytes: bytes):
        """Send signal through worker thread"""
        self.worker.send_data(signal_bytes)

    def _handle_packet(self, packet: bytes, config: PacketConfig):
        """Handle a received packet according to its configuration (runs in main thread)"""
        try:
            # Update statistics
            self.packet_stats[config.header]["count"] += 1
            self.packet_stats[config.header]["last_received"] = time.time()

            # Log the packet
            self._log_packet(packet, config)

            # Put packet in queue
            if config.queue:
                try:
                    config.queue.put_nowait(packet)
                except:
                    # Queue might be full, handle gracefully
                    print(f"[WARNING] Queue full for {config.name}, dropping packet")

            # Call callback if provided
            if config.callback:
                try:
                    config.callback(packet)
                except Exception as e:
                    print(f"[ERROR] Callback error for {config.name}: {e}")
                    self.packet_stats[config.header]["errors"] += 1

            # Emit signal if provided
            if config.signal:
                try:
                    config.signal.emit(packet)
                except Exception as e:
                    print(f"[ERROR] Signal error for {config.name}: {e}")
                    self.packet_stats[config.header]["errors"] += 1

        except Exception as e:
            print(f"[ERROR] Error handling packet for {config.name}: {e}")
            self.packet_stats[config.header]["errors"] += 1

    def _handle_desync(self, byte: int):
        """Handle desync detection"""
        print(f"[DESYNC] Dropped byte: {byte:02X}")
        self.desync_detected.emit(byte)

    def _log_packet(self, packet: bytes, config: PacketConfig):
        """Log received packet"""
        hex_str = " ".join(f"{b:02X}" for b in packet)
        print(f"[PACKET] {config.name}: {hex_str}")

    def __del__(self):
        """Cleanup when object is destroyed"""
        self.stop()
