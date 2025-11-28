# TritLang - A Programming Language for LLMs and Machine Learning

TritLang is a simple, easy-to-program language explicitly designed for LLMs and Machine Learning, using balanced ternary (+1, 0, -1) arithmetic as its foundation.

## Features

- **Balanced Ternary Numbers**: Native support for balanced ternary representation using `+` (1), `0`, and `-` (-1)
- **Three-State Logic**: Built-in support for `true`, `false`, and `maybe` values
- **ML-Friendly**: Built-in vector and matrix operations optimized for machine learning
- **LLM-Friendly**: Clear, intuitive syntax that's easy for language models to generate and understand
- **Simple Syntax**: Minimal, readable syntax inspired by modern languages

## Installation

```bash
# From the workspace root
pip install -e .
```

## Quick Start

### Running a Program

```bash
# Run a TritLang file
python -m tritlang examples/hello_world.trit

# Start interactive REPL
python -m tritlang -i
```

### Hello World

```tritlang
print("Hello, World!")
```

## Language Syntax

### Numbers

TritLang supports both decimal numbers and balanced ternary notation:

```tritlang
// Decimal numbers
let x = 42
let y = 3.14

// Balanced ternary: + (1), 0, - (-1)
let a = +0-   // 8 in decimal: 1*3² + 0*3¹ + (-1)*3⁰ = 9 + 0 - 1 = 8
let b = +-0   // 6 in decimal: 1*3² + (-1)*3¹ + 0*3⁰ = 9 - 3 + 0 = 6
```

### Three-State Logic

```tritlang
let x = true   // 1
let y = false  // 0
let z = maybe  // -1

// Three-state operations
let result1 = x and y   // maybe (if either is maybe)
let result2 = x or z    // maybe
let result3 = not y     // true
```

### Variables

```tritlang
// Immutable variable
let x = 10

// Mutable variable
var y = 20
y = 30

// Assignment operators
y += 5
y -= 10
```

### Vectors (ML Operations)

```tritlang
// Create vectors
let v1 = [1, 2, 3, 4, 5]
let v2 = [10, 20, 30, 40, 50]

// Element-wise operations
let v3 = v1 + v2
let v4 = v1 * 2  // Scalar multiplication

// Dot product
let dot = v1 * v2

// Vector methods
let sum = v1.sum()
let mean = v1.mean()
let length = v1.len

// Index access
let first = v1[0]
```

### Control Flow

```tritlang
// If-elif-else
if x > 10 {
    print("x is greater than 10")
} elif x > 5 {
    print("x is greater than 5")
} else {
    print("x is 5 or less")
}

// While loop
let i = 0
while i < 10 {
    print(i)
    i = i + 1
}

// For loop
let numbers = [1, 2, 3, 4, 5]
for num in numbers {
    print(num)
}
```

### Functions

```tritlang
function add(a, b) {
    return a + b
}

function factorial(n) {
    if n <= 1 {
        return 1
    } else {
        return n * factorial(n - 1)
    }
}

// Call function
let result = add(5, 3)
print(result)
```

### Comments

```tritlang
// Single-line comment

/* Multi-line
   comment */
```

## Built-in Functions

- `print(...)`: Print values to console
- `len(value)`: Get length of vector, string, or array

## Vector Methods

- `vector.sum()`: Sum of all elements
- `vector.mean()`: Mean of all elements
- `vector.len`: Length of vector

## Examples

See the `examples/` directory for complete examples:

- `hello_world.trit`: Basic introduction
- `three_state_logic.trit`: Three-state boolean operations
- `vectors.trit`: Vector operations
- `functions.trit`: Function definitions
- `loops.trit`: Control flow
- `ml_example.trit`: Machine learning operations

## Balanced Ternary Conversion

Balanced ternary uses three digits:
- `+` represents +1
- `0` represents 0
- `-` represents -1

Each position represents a power of 3:
- Position 0: 3⁰ = 1
- Position 1: 3¹ = 3
- Position 2: 3² = 9
- Position 3: 3³ = 27
- etc.

Example: `+-0` = 1×9 + (-1)×3 + 0×1 = 9 - 3 + 0 = 6

## Why Balanced Ternary?

1. **Symmetric Representation**: Negative and positive numbers are represented symmetrically
2. **Efficient Arithmetic**: Some operations are more efficient in balanced ternary
3. **Three-State Logic**: Natural support for true/false/maybe logic
4. **ML Applications**: Useful for ternary neural networks and fuzzy logic systems
5. **LLM-Friendly**: Simple notation that's easy for language models to understand and generate

## Design Philosophy

TritLang is designed with these principles:

1. **Simplicity**: Minimal syntax, easy to learn
2. **Clarity**: Code should be self-explanatory
3. **LLM-Friendly**: Syntax that's natural for language models to generate
4. **ML-Optimized**: Built-in support for common ML operations
5. **Balanced Ternary First**: Native support for balanced ternary arithmetic

## Contributing

Contributions are welcome! Please see the main project README for contribution guidelines.

## License

This project is part of the Trinary Python project and follows the same license.
