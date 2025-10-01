from dataclasses import dataclass
from queue import Queue
from typing import Optional, Callable
from PySide6.QtCore import Signal


@dataclass
class PacketConfig:
    """Configuration for a packet type"""

    header: int
    size: int
    queue: Queue
    callback: Optional[Callable[[bytes], None]] = None
    signal: Optional[Signal] = None
    name: str = ""
