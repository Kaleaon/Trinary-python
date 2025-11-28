# TritLang - Programming Language for LLMs and ML

TritLang is a simple, easy-to-program language explicitly designed for LLMs and Machine Learning, using balanced ternary (+1, 0, -1) arithmetic.

## Quick Start

```bash
# Run a program
python -m tritlang examples/hello_world.trit

# Interactive REPL
python -m tritlang -i
```

## Language Overview

### Balanced Ternary Numbers

```tritlang
let a = +0-   // 8: 1×3² + 0×3¹ + (-1)×3⁰ = 9 + 0 - 1 = 8
let b = +-0   // 6: 1×3² + (-1)×3¹ + 0×3⁰ = 9 - 3 + 0 = 6
```

### Three-State Logic

```tritlang
let x = true   // 1
let y = false  // 0
let z = maybe  // -1

let result = x and y  // maybe (if either is maybe)
```

### Vectors and ML Operations

```tritlang
let v1 = [1, 2, 3, 4, 5]
let v2 = [10, 20, 30, 40, 50]

// Element-wise operations
let v3 = v1 + v2
let v4 = v1 * 2

// Dot product
let dot = v1 * v2

// Methods
let sum = v1.sum()
let mean = v1.mean()
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
```

### Control Flow

```tritlang
// If-elif-else
if x > 10 {
    print("large")
} elif x > 5 {
    print("medium")
} else {
    print("small")
}

// Loops
let i = 0
while i < 10 {
    print(i)
    i = i + 1
}

for num in [1, 2, 3, 4, 5] {
    print(num)
}
```

## Why Balanced Ternary?

1. **Symmetric Representation**: Negative and positive numbers are represented symmetrically
2. **Three-State Logic**: Natural support for true/false/maybe logic
3. **ML Applications**: Useful for ternary neural networks and fuzzy logic
4. **LLM-Friendly**: Simple notation that's easy for language models to understand

## Examples

See the `examples/` directory:
- `hello_world.trit` - Basic introduction
- `three_state_logic.trit` - Three-state boolean operations
- `vectors.trit` - Vector operations
- `functions.trit` - Function definitions
- `loops.trit` - Control flow
- `ml_example.trit` - Machine learning operations

## Documentation

For complete documentation, see [TRITLANG_README.md](../TRITLANG_README.md).
