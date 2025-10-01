#!/usr/bin/env python3
"""
Test script for the enhanced SerialReader class
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from unittest.mock import Mock, patch, MagicMock
from queue import Queue
from utils.serial_reader import SerialReader, PacketConfig

class TestSerialReader(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures"""
        # Mock serial to avoid actual hardware dependency
        self.mock_serial_patcher = patch('utils.serial_reader.serial.Serial')
        self.mock_serial = self.mock_serial_patcher.start()
        
        # Configure mock serial instance
        self.mock_serial_instance = Mock()
        self.mock_serial_instance.is_open = True
        self.mock_serial_instance.in_waiting = 0
        self.mock_serial_instance.read.return_value = b''
        self.mock_serial.return_value = self.mock_serial_instance
    
    def tearDown(self):
        """Clean up after tests"""
        self.mock_serial_patcher.stop()
    
    def test_initialization(self):
        """Test that SerialReader initializes with empty configuration"""
        reader = SerialReader("/dev/ttyUSB0")
        
        # Check that no configurations are present initially
        self.assertEqual(len(reader.packet_configs), 0)
        self.assertEqual(len(reader.packet_stats), 0)
    
    def test_add_packet_config(self):
        """Test adding packet configurations"""
        reader = SerialReader("/dev/ttyUSB0")
        test_queue = Queue()
        test_callback = Mock()
        
        reader.add_packet_config(
            header=0xAA,
            size=15,
            queue=test_queue,
            callback=test_callback,
            name="Test_Packet"
        )
        
        # Verify configuration was added
        self.assertIn(0xAA, reader.packet_configs)
        config = reader.packet_configs[0xAA]
        self.assertEqual(config.header, 0xAA)
        self.assertEqual(config.size, 15)
        self.assertEqual(config.queue, test_queue)
        self.assertEqual(config.callback, test_callback)
        self.assertEqual(config.name, "Test_Packet")
        
        # Verify statistics were initialized
        self.assertIn(0xAA, reader.packet_stats)
        self.assertEqual(reader.packet_stats[0xAA]['count'], 0)
    
    def test_remove_packet_config(self):
        """Test removing packet configurations"""
        reader = SerialReader("/dev/ttyUSB0")
        test_queue = Queue()
        
        # Add a configuration
        reader.add_packet_config(header=0xBB, size=10, queue=test_queue)
        self.assertIn(0xBB, reader.packet_configs)
        
        # Remove the configuration
        reader.remove_packet_config(0xBB)
        self.assertNotIn(0xBB, reader.packet_configs)
        self.assertNotIn(0xBB, reader.packet_stats)
    
    def test_clear_packet_configs(self):
        """Test clearing all packet configurations"""
        reader = SerialReader("/dev/ttyUSB0")
        
        # Add some configurations first
        reader.add_packet_config(header=0xA0, size=10, queue=Queue())
        reader.add_packet_config(header=0xB0, size=15, queue=Queue())
        self.assertGreater(len(reader.packet_configs), 0)
        
        # Clear all configurations
        reader.clear_packet_configs()
        self.assertEqual(len(reader.packet_configs), 0)
        self.assertEqual(len(reader.packet_stats), 0)
    
    def test_get_queue_for_header(self):
        """Test getting queue for specific header"""
        reader = SerialReader("/dev/ttyUSB0")
        test_queue = Queue()
        
        reader.add_packet_config(header=0xCC, size=8, queue=test_queue)
        
        # Test existing header
        queue = reader.get_queue_for_header(0xCC)
        self.assertEqual(queue, test_queue)
        
        # Test non-existing header
        queue = reader.get_queue_for_header(0xFF)
        self.assertIsNone(queue)
    
    def test_buffer_processing_valid_packet(self):
        """Test buffer processing with valid packets"""
        reader = SerialReader("/dev/ttyUSB0")
        test_queue = Queue()
        test_callback = Mock()
        
        reader.add_packet_config(
            header=0xDD,
            size=5,
            queue=test_queue,
            callback=test_callback
        )
        
        # Simulate packet data
        packet_data = bytes([0xDD, 0x01, 0x02, 0x03, 0x04])
        reader.buffer.extend(packet_data)
        
        # Process buffer
        reader._process_buffer()
        
        # Verify packet was processed
        self.assertEqual(len(reader.buffer), 0)  # Buffer should be empty
        self.assertEqual(test_queue.qsize(), 1)  # Packet should be in queue
        test_callback.assert_called_once_with(packet_data)
        
        # Verify statistics
        self.assertEqual(reader.packet_stats[0xDD]['count'], 1)
    
    def test_buffer_processing_invalid_header(self):
        """Test buffer processing with invalid header"""
        reader = SerialReader("/dev/ttyUSB0")
        test_queue = Queue()
        
        reader.add_packet_config(header=0xEE, size=5, queue=test_queue)
        
        # Simulate data with invalid header
        reader.buffer.extend(bytes([0xFF, 0x01, 0x02, 0x03, 0x04]))
        
        # Process buffer
        reader._process_buffer()
        
        # Verify invalid byte was dropped
        self.assertEqual(len(reader.buffer), 4)  # One byte should be dropped
        self.assertEqual(test_queue.qsize(), 0)  # No packets should be queued
    
    def test_buffer_processing_insufficient_data(self):
        """Test buffer processing with insufficient data"""
        reader = SerialReader("/dev/ttyUSB0")
        test_queue = Queue()
        
        reader.add_packet_config(header=0xEE, size=10, queue=test_queue)
        
        # Simulate insufficient data
        reader.buffer.extend(bytes([0xEE, 0x01, 0x02]))  # Only 3 bytes, need 10
        
        # Process buffer
        reader._process_buffer()
        
        # Verify data remains in buffer
        self.assertEqual(len(reader.buffer), 3)
        self.assertEqual(test_queue.qsize(), 0)
    
    def test_handle_packet_with_callback_error(self):
        """Test packet handling when callback raises an exception"""
        reader = SerialReader("/dev/ttyUSB0")
        test_queue = Queue()
        error_callback = Mock(side_effect=Exception("Test error"))
        
        reader.add_packet_config(
            header=0xEF,
            size=3,
            queue=test_queue,
            callback=error_callback
        )
        
        packet = bytes([0xEF, 0x01, 0x02])
        config = reader.packet_configs[0xEF]
        
        # Handle packet (should not raise exception)
        reader._handle_packet(packet, config)
        
        # Verify packet still went to queue despite callback error
        self.assertEqual(test_queue.qsize(), 1)
        self.assertEqual(reader.packet_stats[0xEF]['errors'], 1)
    
    def test_get_packet_stats(self):
        """Test getting packet statistics"""
        reader = SerialReader("/dev/ttyUSB0")
        test_queue = Queue()
        
        reader.add_packet_config(header=0xF0, size=5, queue=test_queue)
        
        # Process a packet
        packet = bytes([0xF0, 0x01, 0x02, 0x03, 0x04])
        config = reader.packet_configs[0xF0]
        reader._handle_packet(packet, config)
        
        # Get stats
        stats = reader.get_packet_stats()
        
        # Verify stats
        self.assertIn(0xF0, stats)
        self.assertEqual(stats[0xF0]['count'], 1)
        self.assertEqual(stats[0xF0]['errors'], 0)
        self.assertIsNotNone(stats[0xF0]['last_received'])

class TestPacketConfig(unittest.TestCase):
    
    def test_packet_config_creation(self):
        """Test PacketConfig dataclass creation"""
        test_queue = Queue()
        test_callback = Mock()
        
        config = PacketConfig(
            header=0xAB,
            size=20,
            queue=test_queue,
            callback=test_callback,
            name="Test_Config"
        )
        
        self.assertEqual(config.header, 0xAB)
        self.assertEqual(config.size, 20)
        self.assertEqual(config.queue, test_queue)
        self.assertEqual(config.callback, test_callback)
        self.assertEqual(config.name, "Test_Config")

if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2)
