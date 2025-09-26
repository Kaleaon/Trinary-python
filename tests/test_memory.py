"""
Tests for trinary memory management.
"""

import pytest
from trinary.memory import TrinaryMemory
from trinary.types import TrinaryInt


class TestTrinaryMemory:
    """Test cases for TrinaryMemory class."""
    
    def test_memory_initialization(self):
        """Test memory system initialization."""
        memory = TrinaryMemory(address_width=6, word_size=3)
        
        assert memory.address_width == 6
        assert memory.word_size == 3
        assert memory.max_address == (3 ** 6) - 1  # 728
        
        stats = memory.get_memory_stats()
        assert stats['total_address_space'] == 3 ** 6
        assert stats['allocated_words'] == 0
        assert stats['free_words'] == 3 ** 6
    
    def test_basic_allocation_deallocation(self):
        """Test basic memory allocation and deallocation."""
        memory = TrinaryMemory(address_width=4, word_size=2)  # 81 addresses
        
        # Allocate memory
        addr = memory.allocate(10)
        assert addr is not None
        assert addr.decimal_value == 0  # First allocation should start at 0
        
        # Check statistics
        stats = memory.get_memory_stats()
        assert stats['allocated_words'] == 10
        assert stats['free_words'] == 81 - 10
        
        # Deallocate memory
        success = memory.deallocate(addr)
        assert success
        
        # Check statistics after deallocation
        stats = memory.get_memory_stats()
        assert stats['allocated_words'] == 0
        assert stats['free_words'] == 81
    
    def test_multiple_allocations(self):
        """Test multiple memory allocations."""
        memory = TrinaryMemory(address_width=4, word_size=2)
        
        allocations = []
        for size in [5, 3, 7, 2]:
            addr = memory.allocate(size)
            assert addr is not None
            allocations.append((addr, size))
        
        # Verify all allocations are different
        addresses = [addr.decimal_value for addr, _ in allocations]
        assert len(set(addresses)) == len(addresses)  # All unique
        
        # Verify total allocation
        total_allocated = sum(size for _, size in allocations)
        stats = memory.get_memory_stats()
        assert stats['allocated_words'] == total_allocated
    
    def test_memory_read_write(self):
        """Test memory read and write operations."""
        memory = TrinaryMemory(address_width=4, word_size=4)  # Use larger word size
        
        # Allocate memory
        addr = memory.allocate(5)
        assert addr is not None
        
        # Test writing and reading TrinaryInt
        test_data = TrinaryInt(42)  # "1120" in trinary, 4 trits
        success = memory.write(addr, test_data)
        assert success
        
        read_data = memory.read_as_trinary_int(addr)
        assert read_data is not None
        assert read_data.decimal_value == 42
        
        # Test writing and reading raw trits
        test_trits = [1, 2, 0, 1]
        success = memory.write(TrinaryInt(addr.decimal_value + 1), test_trits)
        assert success
        
        read_trits = memory.read(TrinaryInt(addr.decimal_value + 1))
        assert read_trits == test_trits
        
        # Test writing regular integers
        success = memory.write(TrinaryInt(addr.decimal_value + 2), 27)  # Smaller number
        assert success
        
        read_data = memory.read_as_trinary_int(TrinaryInt(addr.decimal_value + 2))
        assert read_data.decimal_value == 27
    
    def test_memory_bounds_checking(self):
        """Test memory bounds checking."""
        memory = TrinaryMemory(address_width=3, word_size=2)  # 27 addresses
        
        # Test reading/writing to unallocated memory
        unallocated_addr = TrinaryInt(5)
        
        success = memory.write(unallocated_addr, TrinaryInt(42))
        assert not success  # Should fail - not allocated
        
        data = memory.read(unallocated_addr)
        assert data is None  # Should fail - not allocated
        
        # Test out-of-bounds addresses
        out_of_bounds = TrinaryInt(100)  # > max_address
        
        success = memory.write(out_of_bounds, TrinaryInt(42))
        assert not success
        
        data = memory.read(out_of_bounds)
        assert data is None
    
    def test_block_copy(self):
        """Test block copy operations."""
        memory = TrinaryMemory(address_width=4, word_size=3)
        
        # Allocate source and destination blocks
        src_addr = memory.allocate(5)
        dest_addr = memory.allocate(5)
        assert src_addr is not None and dest_addr is not None
        
        # Fill source block with test data
        test_data = [TrinaryInt(i * 10) for i in range(5)]
        for i, data in enumerate(test_data):
            addr = TrinaryInt(src_addr.decimal_value + i)
            memory.write(addr, data)
        
        # Copy block
        success = memory.copy_block(src_addr, dest_addr, 5)
        assert success
        
        # Verify copy
        for i in range(5):
            src_data = memory.read_as_trinary_int(TrinaryInt(src_addr.decimal_value + i))
            dest_data = memory.read_as_trinary_int(TrinaryInt(dest_addr.decimal_value + i))
            assert src_data.decimal_value == dest_data.decimal_value
    
    def test_memory_fragmentation(self):
        """Test memory fragmentation and defragmentation."""
        memory = TrinaryMemory(address_width=4, word_size=2)
        
        # Allocate several blocks
        blocks = []
        for i in range(5):
            addr = memory.allocate(3)
            blocks.append(addr)
        
        # Deallocate every other block to create fragmentation
        for i in range(0, len(blocks), 2):
            memory.deallocate(blocks[i])
        
        # Check fragmentation
        stats = memory.get_memory_stats()
        initial_fragments = stats['fragmentation_blocks']
        
        # Defragment
        final_fragments = memory.defragment()
        
        # Fragmentation should be reduced or stay the same
        assert final_fragments <= initial_fragments
    
    def test_word_size_handling(self):
        """Test proper handling of word size limits."""
        memory = TrinaryMemory(address_width=4, word_size=2)
        
        addr = memory.allocate(1)
        assert addr is not None
        
        # Test writing data larger than word size
        large_data = TrinaryInt(100)  # "10201" - 5 trits
        success = memory.write(addr, large_data)
        assert success
        
        # Should be truncated to word size
        read_data = memory.read(addr)
        assert len(read_data) == 2  # Word size limit
        
        # Test writing data smaller than word size
        small_data = TrinaryInt(1)  # "1" - 1 trit
        success = memory.write(addr, small_data)
        assert success
        
        # Should be padded to word size
        read_data = memory.read(addr)
        assert len(read_data) == 2  # Word size
        assert read_data == [0, 1]  # Padded with leading zeros
    
    def test_memory_dump(self):
        """Test memory dump functionality."""
        memory = TrinaryMemory(address_width=3, word_size=2)
        
        # Allocate and fill some memory
        addr = memory.allocate(3)
        for i in range(3):
            memory.write(TrinaryInt(addr.decimal_value + i), TrinaryInt(i + 1))
        
        # Generate memory dump
        dump = memory.dump_memory(0, 5, show_empty=True)
        
        # Verify dump contains expected information
        assert "Memory Dump" in dump
        assert str(addr) in dump
        
        # Test selective dump
        selective_dump = memory.dump_memory(addr.decimal_value, addr.decimal_value + 1)
        assert len(selective_dump.split('\n')) < len(dump.split('\n'))
    
    def test_allocation_failure(self):
        """Test allocation failure when memory is full."""
        memory = TrinaryMemory(address_width=2, word_size=1)  # Only 9 addresses
        
        # Allocate all available memory
        addr = memory.allocate(9)
        assert addr is not None
        
        # Try to allocate more - should fail
        failed_addr = memory.allocate(1)
        assert failed_addr is None
        
        # Deallocate and try again
        memory.deallocate(addr)
        new_addr = memory.allocate(5)
        assert new_addr is not None


if __name__ == "__main__":
    pytest.main([__file__])