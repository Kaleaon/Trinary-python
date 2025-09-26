#!/usr/bin/env python3
"""
Trinary memory management demonstration.

This script shows how to use the TrinaryMemory system for managing
data in a trinary computing environment with trit-based addressing.
"""

from trinary import TrinaryMemory, TrinaryInt


def demonstrate_memory_allocation():
    """Show basic memory allocation and deallocation."""
    print("=== Memory Allocation Demo ===")
    
    # Create memory system with 6-trit addresses (729 addresses)
    memory = TrinaryMemory(address_width=6, word_size=3)
    
    print(f"Created memory system:")
    print(f"  Address width: {memory.address_width} trits")
    print(f"  Max addresses: {memory.max_address + 1}")
    print(f"  Word size: {memory.word_size} trits")
    print()
    
    # Allocate some memory blocks
    allocations = []
    
    print("Allocating memory blocks:")
    for i, size in enumerate([10, 5, 20, 3], 1):
        addr = memory.allocate(size)
        if addr:
            allocations.append((addr, size))
            print(f"  Block {i}: {size:2d} words at address {addr} (decimal: {addr.decimal_value})")
        else:
            print(f"  Block {i}: Failed to allocate {size} words")
    
    print()
    
    # Show memory statistics
    stats = memory.get_memory_stats()
    print("Memory Statistics:")
    for key, value in stats.items():
        if isinstance(value, float):
            print(f"  {key.replace('_', ' ').title()}: {value:.2f}")
        else:
            print(f"  {key.replace('_', ' ').title()}: {value}")
    
    print()
    
    # Deallocate some blocks
    print("Deallocating every other block:")
    for i, (addr, size) in enumerate(allocations[::2], 1):
        success = memory.deallocate(addr)
        print(f"  Deallocated block at {addr}: {'Success' if success else 'Failed'}")
    
    # Show updated statistics
    stats = memory.get_memory_stats()
    print(f"\nAfter deallocation:")
    print(f"  Allocated words: {stats['allocated_words']}")
    print(f"  Free words: {stats['free_words']}")
    print(f"  Fragmentation blocks: {stats['fragmentation_blocks']}")
    
    print()
    return memory, allocations[1::2]  # Return memory and remaining allocations


def demonstrate_memory_operations(memory, allocations):
    """Show memory read/write operations."""
    print("=== Memory Read/Write Demo ===")
    
    if not allocations:
        print("No allocations available for demo")
        return
    
    addr, size = allocations[0]
    print(f"Using memory block at address {addr} (decimal: {addr.decimal_value})")
    print()
    
    # Write some trinary data
    test_data = [
        TrinaryInt(42),
        TrinaryInt(100),
        TrinaryInt(7),
        TrinaryInt(255),
        TrinaryInt(13)
    ]
    
    print("Writing data:")
    for i, data in enumerate(test_data[:min(size, len(test_data))]):
        write_addr = TrinaryInt(addr.decimal_value + i)
        success = memory.write(write_addr, data)
        print(f"  Address {write_addr}: {data} (decimal: {data.decimal_value}) - {'OK' if success else 'FAIL'}")
    
    print()
    
    # Read data back
    print("Reading data back:")
    for i in range(min(size, len(test_data))):
        read_addr = TrinaryInt(addr.decimal_value + i)
        data = memory.read_as_trinary_int(read_addr)
        if data:
            print(f"  Address {read_addr}: {data} (decimal: {data.decimal_value})")
        else:
            print(f"  Address {read_addr}: Failed to read")
    
    print()


def demonstrate_memory_dump(memory, allocations):
    """Show memory dump functionality."""
    print("=== Memory Dump Demo ===")
    
    if not allocations:
        print("No allocations available for demo")
        return
    
    addr, size = allocations[0]
    start_addr = addr.decimal_value
    end_addr = start_addr + min(size, 10) - 1
    
    # Create memory dump
    dump = memory.dump_memory(start_addr, end_addr, show_empty=True)
    print(dump)
    print()


def demonstrate_block_operations(memory):
    """Show block copy and other operations."""
    print("=== Block Operations Demo ===")
    
    # Allocate two blocks for copying
    source_addr = memory.allocate(5)
    dest_addr = memory.allocate(5)
    
    if not (source_addr and dest_addr):
        print("Failed to allocate blocks for demo")
        return
    
    print(f"Source block: {source_addr} (decimal: {source_addr.decimal_value})")
    print(f"Destination block: {dest_addr} (decimal: {dest_addr.decimal_value})")
    print()
    
    # Fill source block with data
    source_data = [TrinaryInt(i * 3 + 1) for i in range(5)]
    print("Filling source block:")
    for i, data in enumerate(source_data):
        addr = TrinaryInt(source_addr.decimal_value + i)
        memory.write(addr, data)
        print(f"  [{addr}] = {data}")
    
    print()
    
    # Copy block
    print("Copying block...")
    success = memory.copy_block(source_addr, dest_addr, 5)
    print(f"Copy operation: {'Success' if success else 'Failed'}")
    print()
    
    # Verify copy
    print("Verifying copy in destination block:")
    for i in range(5):
        addr = TrinaryInt(dest_addr.decimal_value + i)
        data = memory.read_as_trinary_int(addr)
        print(f"  [{addr}] = {data}")
    
    print()
    
    # Clean up
    memory.deallocate(source_addr)
    memory.deallocate(dest_addr)


def demonstrate_fragmentation():
    """Show memory fragmentation and defragmentation."""
    print("=== Fragmentation Demo ===")
    
    # Use smaller memory for clearer demonstration
    memory = TrinaryMemory(address_width=4, word_size=2)  # 81 addresses
    
    print(f"Created smaller memory system with {memory.max_address + 1} addresses")
    print()
    
    # Allocate many small blocks
    allocations = []
    print("Allocating many small blocks:")
    for i in range(10):
        addr = memory.allocate(3)
        if addr:
            allocations.append(addr)
            print(f"  Block {i+1}: Address {addr}")
        else:
            print(f"  Block {i+1}: Allocation failed")
    
    print()
    
    # Deallocate every other block to create fragmentation
    print("Creating fragmentation by deallocating every other block:")
    for i in range(0, len(allocations), 2):
        addr = allocations[i]
        memory.deallocate(addr)
        print(f"  Deallocated block at {addr}")
    
    print()
    
    # Show fragmentation stats
    stats = memory.get_memory_stats()
    print(f"Fragmentation blocks before defragmentation: {stats['fragmentation_blocks']}")
    
    # Defragment
    blocks_after = memory.defragment()
    print(f"Fragmentation blocks after defragmentation: {blocks_after}")
    
    print()


def main():
    """Run all memory demonstrations."""
    print("Trinary Python - Memory Management Demo")
    print("=" * 50)
    print()
    
    # Basic allocation demo
    memory, remaining_allocs = demonstrate_memory_allocation()
    
    # Memory operations
    demonstrate_memory_operations(memory, remaining_allocs)
    
    # Memory dump
    demonstrate_memory_dump(memory, remaining_allocs)
    
    # Block operations
    demonstrate_block_operations(memory)
    
    # Fragmentation demo
    demonstrate_fragmentation()
    
    print("All memory demonstrations completed!")


if __name__ == "__main__":
    main()