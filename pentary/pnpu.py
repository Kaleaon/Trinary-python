"""
PNPU (Pentary Neural Processing Unit) simulation and hardware abstraction.

This module provides simulation of the PNPU architecture including:
- Shift-Add MAC cores
- Memory management
- Neural network layer operations
"""

from typing import List, Optional, Tuple
from .operations import PentaryOperations
from .types import PentaryInt


class ShiftAddMAC:
    """
    Shift-Add Multiply-Accumulate unit simulation.
    
    This simulates the core PNPU operation that eliminates multipliers
    by using shift-add logic.
    """
    
    def __init__(self, data_width: int = 16):
        """
        Initialize a Shift-Add MAC unit.
        
        Args:
            data_width: Bit width for activation data
        """
        self.data_width = data_width
        self.accumulator = 0
    
    def reset(self):
        """Reset the accumulator."""
        self.accumulator = 0
    
    def mac(self, activation: int, weight: int) -> int:
        """
        Perform Multiply-Accumulate operation.
        
        Args:
            activation: Input activation (signed integer)
            weight: Weight value (-2, -1, 0, 1, or 2)
        
        Returns:
            New accumulator value
        """
        self.accumulator = PentaryOperations.shift_add_mac(
            activation, weight, self.accumulator
        )
        return self.accumulator
    
    def get_accumulator(self) -> int:
        """Get current accumulator value."""
        return self.accumulator


class PNPUCore:
    """
    PNPU Core simulation - represents a single processing tile.
    
    Each core contains multiple MAC units and local memory.
    """
    
    def __init__(self, num_macs: int = 64, memory_size: int = 1024):
        """
        Initialize a PNPU core.
        
        Args:
            num_macs: Number of MAC units in this core
            memory_size: Local memory size (in words)
        """
        self.num_macs = num_macs
        self.macs = [ShiftAddMAC() for _ in range(num_macs)]
        self.memory: List[int] = [0] * memory_size
        self.memory_size = memory_size
    
    def reset(self):
        """Reset all MAC units."""
        for mac in self.macs:
            mac.reset()
    
    def matrix_vector_multiply(self, weights: List[List[int]], activations: List[int]) -> List[int]:
        """
        Perform matrix-vector multiplication using shift-add MACs.
        
        This is the core operation for neural network layers.
        
        Args:
            weights: Weight matrix (each row is a list of weights: -2, -1, 0, 1, or 2)
            activations: Input activation vector
        
        Returns:
            Output activation vector
        """
        if len(weights[0]) != len(activations):
            raise ValueError("Weight matrix columns must match activation vector length")
        
        outputs = []
        
        for i, weight_row in enumerate(weights):
            # Reset MAC for this output
            mac = self.macs[i % self.num_macs]
            mac.reset()
            
            # Perform dot product using shift-add
            for activation, weight in zip(activations, weight_row):
                mac.mac(activation, weight)
            
            outputs.append(mac.get_accumulator())
        
        return outputs
    
    def load_weights(self, weights: List[int], address: int = 0):
        """
        Load weights into local memory.
        
        Args:
            weights: List of weight values
            address: Starting memory address
        """
        if address + len(weights) > self.memory_size:
            raise ValueError("Weights exceed available memory")
        
        for i, weight in enumerate(weights):
            self.memory[address + i] = weight
    
    def read_memory(self, address: int) -> int:
        """Read from local memory."""
        if address >= self.memory_size:
            raise ValueError("Memory address out of range")
        return self.memory[address]
    
    def write_memory(self, address: int, value: int):
        """Write to local memory."""
        if address >= self.memory_size:
            raise ValueError("Memory address out of range")
        self.memory[address] = value
