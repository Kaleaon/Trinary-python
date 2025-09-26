"""
Trinary memory management system.

This module provides memory management for trinary systems using trits
instead of bits, including address space management and data storage.
"""

from typing import List, Dict, Optional, Union, Any
from .core import TrinaryNumber
from .types import TrinaryInt


class TrinaryMemory:
    """
    Memory management system for trinary computing.
    
    Manages memory addresses using trinary representation and stores
    data in trits instead of bits. Provides allocation, deallocation,
    and access methods.
    """
    
    def __init__(self, address_width: int = 9, word_size: int = 3):
        """
        Initialize trinary memory system.
        
        Args:
            address_width: Number of trits for memory addresses (default: 9 = 3^9 = 19683 addresses)
            word_size: Number of trits per memory word (default: 3)
        """
        self.address_width = address_width
        self.word_size = word_size
        self.max_address = (3 ** address_width) - 1
        
        # Memory storage - dictionary mapping addresses to data
        self._memory: Dict[int, List[int]] = {}
        
        # Allocation tracking
        self._allocated_blocks: Dict[int, int] = {}  # start_address -> size
        self._free_blocks: List[tuple] = [(0, self.max_address + 1)]  # (start, size) tuples
    
    def allocate(self, size: int) -> Optional[TrinaryInt]:
        """
        Allocate a block of memory.
        
        Args:
            size: Number of words to allocate
        
        Returns:
            Starting address as TrinaryInt, or None if allocation failed
        """
        # Find a suitable free block
        for i, (start, block_size) in enumerate(self._free_blocks):
            if block_size >= size:
                # Allocate from this block
                self._allocated_blocks[start] = size
                
                # Update free blocks
                if block_size == size:
                    # Exact fit - remove the free block
                    del self._free_blocks[i]
                else:
                    # Partial allocation - update the free block
                    self._free_blocks[i] = (start + size, block_size - size)
                
                return TrinaryInt(start)
        
        return None  # No suitable block found
    
    def deallocate(self, address: Union[TrinaryInt, int]) -> bool:
        """
        Deallocate a memory block.
        
        Args:
            address: Starting address of the block to deallocate
        
        Returns:
            True if successful, False if address was not allocated
        """
        addr = address.decimal_value if isinstance(address, TrinaryInt) else address
        
        if addr not in self._allocated_blocks:
            return False
        
        size = self._allocated_blocks[addr]
        del self._allocated_blocks[addr]
        
        # Clear the memory
        for i in range(addr, addr + size):
            if i in self._memory:
                del self._memory[i]
        
        # Add back to free blocks and merge adjacent blocks
        self._free_blocks.append((addr, size))
        self._merge_free_blocks()
        
        return True
    
    def _merge_free_blocks(self):
        """Merge adjacent free blocks to reduce fragmentation."""
        if len(self._free_blocks) <= 1:
            return
        
        # Sort free blocks by start address
        self._free_blocks.sort(key=lambda x: x[0])
        
        merged = []
        current_start, current_size = self._free_blocks[0]
        
        for start, size in self._free_blocks[1:]:
            if current_start + current_size == start:
                # Adjacent blocks - merge them
                current_size += size
            else:
                # Non-adjacent - add current and start new
                merged.append((current_start, current_size))
                current_start, current_size = start, size
        
        # Add the last block
        merged.append((current_start, current_size))
        self._free_blocks = merged
    
    def write(self, address: Union[TrinaryInt, int], data: Union[List[int], TrinaryInt, int]) -> bool:
        """
        Write data to memory.
        
        Args:
            address: Memory address to write to
            data: Data to write (trits, TrinaryInt, or int)
        
        Returns:
            True if successful, False if address is out of bounds or not allocated
        """
        addr = address.decimal_value if isinstance(address, TrinaryInt) else address
        
        if addr < 0 or addr > self.max_address:
            return False
        
        # Check if address is in an allocated block
        allocated = False
        for start, size in self._allocated_blocks.items():
            if start <= addr < start + size:
                allocated = True
                break
        
        if not allocated:
            return False
        
        # Convert data to trits
        if isinstance(data, list):
            trits = data[:self.word_size]  # Truncate to word size
        elif isinstance(data, TrinaryInt):
            trits = data.trits[:self.word_size]
        elif isinstance(data, int):
            temp_trinary = TrinaryInt(data)
            trits = temp_trinary.trits[:self.word_size]
        else:
            return False
        
        # Pad to word size if necessary
        while len(trits) < self.word_size:
            trits.insert(0, 0)
        
        self._memory[addr] = trits
        return True
    
    def read(self, address: Union[TrinaryInt, int]) -> Optional[List[int]]:
        """
        Read data from memory.
        
        Args:
            address: Memory address to read from
        
        Returns:
            List of trits, or None if address is invalid or not allocated
        """
        addr = address.decimal_value if isinstance(address, TrinaryInt) else address
        
        if addr < 0 or addr > self.max_address:
            return None
        
        # Check if address is in an allocated block
        allocated = False
        for start, size in self._allocated_blocks.items():
            if start <= addr < start + size:
                allocated = True
                break
        
        if not allocated:
            return None
        
        return self._memory.get(addr, [0] * self.word_size)
    
    def read_as_trinary_int(self, address: Union[TrinaryInt, int]) -> Optional[TrinaryInt]:
        """
        Read data from memory and return as TrinaryInt.
        
        Args:
            address: Memory address to read from
        
        Returns:
            TrinaryInt representation of the data, or None if read failed
        """
        trits = self.read(address)
        if trits is None:
            return None
        
        return TrinaryInt(trits)
    
    def copy_block(self, src_addr: Union[TrinaryInt, int], dest_addr: Union[TrinaryInt, int], size: int) -> bool:
        """
        Copy a block of memory from source to destination.
        
        Args:
            src_addr: Source starting address
            dest_addr: Destination starting address
            size: Number of words to copy
        
        Returns:
            True if successful, False otherwise
        """
        src = src_addr.decimal_value if isinstance(src_addr, TrinaryInt) else src_addr
        dest = dest_addr.decimal_value if isinstance(dest_addr, TrinaryInt) else dest_addr
        
        # Read all source data first (in case of overlapping regions)
        source_data = []
        for i in range(size):
            data = self.read(src + i)
            if data is None:
                return False
            source_data.append(data)
        
        # Write to destination
        for i, data in enumerate(source_data):
            if not self.write(dest + i, data):
                return False
        
        return True
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """
        Get memory usage statistics.
        
        Returns:
            Dictionary with memory statistics
        """
        total_memory = self.max_address + 1
        allocated_words = sum(self._allocated_blocks.values())
        free_words = sum(size for _, size in self._free_blocks)
        used_words = len(self._memory)
        
        return {
            'total_address_space': total_memory,
            'address_width_trits': self.address_width,
            'word_size_trits': self.word_size,
            'allocated_words': allocated_words,
            'free_words': free_words,
            'actually_used_words': used_words,
            'fragmentation_blocks': len(self._free_blocks),
            'allocation_efficiency': (used_words / max(allocated_words, 1)) * 100
        }
    
    def dump_memory(self, start_addr: int = 0, end_addr: int = None, show_empty: bool = False) -> str:
        """
        Create a memory dump for debugging.
        
        Args:
            start_addr: Starting address for dump
            end_addr: Ending address for dump (None for all allocated)
            show_empty: Whether to show uninitialized addresses
        
        Returns:
            String representation of memory contents
        """
        if end_addr is None:
            if self._memory:
                end_addr = max(self._memory.keys())
            else:
                end_addr = start_addr
        
        dump_lines = []
        dump_lines.append(f"Memory Dump (Address {start_addr} to {end_addr})")
        dump_lines.append("=" * 50)
        
        for addr in range(start_addr, min(end_addr + 1, self.max_address + 1)):
            if addr in self._memory or show_empty:
                addr_trinary = TrinaryInt(addr)
                data = self._memory.get(addr, [0] * self.word_size)
                data_str = "".join(str(t) for t in data)
                dump_lines.append(f"[{addr_trinary}] {addr:6d}: {data_str}")
        
        return "\n".join(dump_lines)
    
    def defragment(self) -> int:
        """
        Defragment memory by merging adjacent free blocks.
        
        Returns:
            Number of free blocks after defragmentation
        """
        self._merge_free_blocks()
        return len(self._free_blocks)