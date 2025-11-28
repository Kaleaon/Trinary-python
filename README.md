# Trinary Python

A comprehensive Python implementation for trinary (base-3) computing systems, including **TritLang** - a programming language designed for LLMs and Machine Learning using balanced ternary (+1, 0, -1) arithmetic.

## Overview

Trinary Python provides a complete framework for working with trinary (base-3) number systems and computing. Unlike binary systems that use bits (0, 1), trinary systems use **trits** with three possible states. This implementation supports both standard ternary (0, 1, 2) and balanced ternary (-1, 0, 1) representations.

## Features

### Core Trinary Types
- **TrinaryNumber**: Base trinary number representation with automatic conversion
- **BalancedTernary**: Balanced ternary using digits {-1, 0, 1} for symmetric representation
- **TrinaryInt**: Integer operations optimized for trinary arithmetic
- **TrinaryFloat**: Floating-point numbers with trinary fractional parts
- **TrinaryBool**: Three-state logic (True, False, Maybe/Unknown)

### Advanced Operations
- **TrinaryOperations**: Low-level trit manipulation and specialized algorithms
- **TrinaryMemory**: Memory management using trinary addresses and trit-based storage
- Bitwise operations adapted for trinary (tritwise operations)
- Arithmetic with proper carry/borrow logic in base-3

### Key Capabilities
- ✅ Conversion between decimal, trinary, and balanced ternary
- ✅ Full arithmetic operations (+, -, *, /, //, %, **)
- ✅ Trinary bitwise operations (AND, OR, NOT, XOR)
- ✅ Three-state boolean logic with Maybe/Unknown state
- ✅ Memory management with trinary addressing
- ✅ Trit shifting and rotation operations
- ✅ Floating-point support with trinary fractions

## Installation

```bash
# Clone the repository
git clone https://github.com/Kaleaon/Trinary-python.git
cd Trinary-python

# Install in development mode
pip install -e .

# Or install with development dependencies
pip install -e ".[dev]"
```

## Quick Start

```python
from trinary import TrinaryNumber, TrinaryInt, TrinaryFloat, TrinaryBool, BalancedTernary

# Basic trinary numbers
num = TrinaryNumber(10)
print(f"Decimal 10 = Trinary {num}")  # Output: "101"

# Arithmetic operations
a = TrinaryInt(5)  # "12" in trinary
b = TrinaryInt(3)  # "10" in trinary
print(f"{a} + {b} = {a + b}")  # "12 + 10 = 22"

# Balanced ternary (symmetric representation)
bt = BalancedTernary(5)
print(f"Balanced ternary of 5: {bt}")  # "1TT" where T = -1

# Three-state boolean logic
maybe_true = TrinaryBool("maybe")
definite_true = TrinaryBool(True)
result = maybe_true & definite_true
print(f"Maybe AND True = {result}")  # "Maybe"

# Floating point in trinary
tf = TrinaryFloat("10.12")  # 3 + 1/3 + 2/9 ≈ 3.556
print(f"Trinary float value: {tf.decimal_value}")
```

## Advanced Usage

### Memory Management

```python
from trinary import TrinaryMemory, TrinaryInt

# Create memory system with 9-trit addresses (19683 possible addresses)
memory = TrinaryMemory(address_width=9, word_size=3)

# Allocate memory block
start_addr = memory.allocate(10)  # 10 words
if start_addr:
    # Write data
    memory.write(start_addr, TrinaryInt(42))
    
    # Read data back
    data = memory.read_as_trinary_int(start_addr)
    print(f"Stored value: {data.decimal_value}")
    
    # Get memory statistics
    stats = memory.get_memory_stats()
    print(f"Memory efficiency: {stats['allocation_efficiency']:.1f}%")
```

### Bitwise Operations

```python
from trinary import TrinaryOperations, TrinaryInt

a = TrinaryInt(10)  # "101" in trinary
b = TrinaryInt(6)   # "20" in trinary

# Tritwise AND operation
result = TrinaryOperations.bitwise_and(a, b)
print(f"Tritwise AND: {result}")

# Trit shifting (equivalent to multiplying/dividing by powers of 3)
shifted = a.trit_shift_left(2)  # Multiply by 3²
print(f"Left shift by 2: {shifted.decimal_value}")  # 10 * 9 = 90

# Rotation operations
rotated = TrinaryOperations.rotate_left(a, 1, width=6)
print(f"Rotated left: {rotated}")
```

## Applications

### Where Trinary Computing Excels

1. **Fuzzy Logic Systems**: Natural three-state logic (True/False/Unknown)
2. **Error Correction**: Balanced ternary's symmetric properties aid in error detection
3. **Quantum Computing Simulation**: Qutrit (3-state quantum bit) simulation
4. **AI/ML Research**: Ternary neural networks for efficient computation
5. **Digital Signal Processing**: Ternary representations for certain algorithms

### Use Cases

- **Research**: Exploring alternative number systems and their computational properties
- **Education**: Understanding base-3 arithmetic and non-binary logic systems
- **Specialized Computing**: Applications where three-state logic is natural
- **Algorithm Development**: Implementing algorithms designed for ternary systems

## Architecture

```
trinary/
├── core.py         # Basic TrinaryNumber and BalancedTernary classes
├── types.py        # Specialized types (Int, Float, Bool)
├── operations.py   # Advanced trinary operations and algorithms
├── memory.py       # Memory management system
└── __init__.py     # Package exports

tests/              # Comprehensive test suite
examples/           # Usage examples and tutorials
docs/              # Documentation
```

## Testing

```bash
# Run all tests
python -m pytest tests/

# Run with coverage
python -m pytest tests/ --cov=trinary --cov-report=html

# Run specific test file
python -m pytest tests/test_core.py -v
```

## Performance Considerations

- **Conversion Overhead**: Converting between decimal and trinary has computational cost
- **Memory Usage**: Trinary representations may use more space than binary for large numbers
- **Algorithm Efficiency**: Some algorithms are more efficient in trinary, others in binary
- **Use Cases**: Best suited for applications where three-state logic is natural

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes with tests
4. Run the test suite (`python -m pytest`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## TritLang Programming Language

**TritLang** is a simple, easy-to-program language explicitly designed for LLMs and Machine Learning, using balanced ternary (+1, 0, -1) arithmetic.

### Features

- **Balanced Ternary Numbers**: Native support using `+` (1), `0`, and `-` (-1)
- **Three-State Logic**: Built-in `true`, `false`, and `maybe` values
- **ML-Friendly**: Built-in vector and matrix operations
- **LLM-Friendly**: Clear, intuitive syntax

### Quick Start

```bash
# Run a TritLang program
python -m tritlang examples/hello_world.trit

# Start interactive REPL
python -m tritlang -i
```

### Example

```tritlang
// Balanced ternary numbers
let a = +0-   // 8 in decimal
let b = +-0   // 6 in decimal

// Three-state logic
let x = true
let y = maybe
let result = x and y  // maybe

// Vectors for ML
let v1 = [1, 2, 3, 4, 5]
let sum = v1.sum()
let mean = v1.mean()
```

See [TRITLANG_README.md](TRITLANG_README.md) for complete documentation.

## Roadmap

- [x] TritLang programming language interpreter
- [ ] Trinary bytecode compiler for TritLang
- [ ] Integration with Python's `decimal` module
- [ ] SIMD optimizations for trinary operations
- [ ] Trinary neural network utilities
- [ ] Export/import formats for trinary data
- [ ] Performance optimizations and C extensions

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Research on ternary computing systems and balanced ternary arithmetic
- The Python community for excellent development tools and practices
- Academic papers on multi-valued logic systems

## Further Reading

- [Ternary numeral system](https://en.wikipedia.org/wiki/Ternary_numeral_system)
- [Balanced ternary](https://en.wikipedia.org/wiki/Balanced_ternary)
- [Three-valued logic](https://en.wikipedia.org/wiki/Three-valued_logic)
- [Ternary computer](https://en.wikipedia.org/wiki/Ternary_computer)