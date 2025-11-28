# PentLang - Programming Language for PNPU Architecture

PentLang is a programming language designed for the **Pentary Neural Processing Unit (PNPU)** architecture, using balanced quinary (-2, -1, 0, +1, +2) arithmetic optimized for edge AI inference.

## Overview

PentLang extends the concept of TritLang to support **balanced quinary (base-5)** number systems, providing:

- **Five-State Logic**: AbsoluteYes (+2), MaybeYes (+1), Unknown (0), MaybeNo (-1), AbsoluteNo (-2)
- **PNPU-Optimized Operations**: Shift-add MAC operations that eliminate multipliers
- **ML-Friendly**: Built-in vector and matrix operations for neural networks
- **LLM-Friendly**: Clear, intuitive syntax

## Quick Start

```bash
# Run a PentLang program
python3 -m pentlang examples/hello_pentary.pent

# Start interactive REPL
python3 -m pentlang -i
```

## Language Features

### Balanced Quinary Numbers

```pentlang
// Balanced quinary: +2, +1, 0, -1, -2
let a = +2+1   // 2×5¹ + 1×5⁰ = 10 + 1 = 11
let b = +1-1   // 1×5¹ + (-1)×5⁰ = 5 - 1 = 4
let c = -2-1   // (-2)×5¹ + (-1)×5⁰ = -10 - 1 = -11

print("a =", a)
print("b =", b)
print("c =", c)
```

### Five-State Logic

```pentlang
let x = absolute_yes   // +2: Strong activation
let y = maybe_yes       // +1: Weak activation
let z = unknown         // 0: No signal
let w = maybe_no        // -1: Weak inhibition
let v = absolute_no     // -2: Strong inhibition

// Five-state operations
let result1 = x and y   // Returns minimum
let result2 = x or z    // Returns maximum
```

### PNPU Shift-Add Operations

```pentlang
// Multiply-Accumulate using shift-add (no multipliers!)
let activations = [10, 20, 30]
let weights = [+2, -1, +1]  // Must be -2, -1, 0, +1, or +2

let result = activations.mac(weights)
// Uses shift-add: 10<<1 + (-20) + 30 = 20 - 20 + 30 = 30
```

### Vector Operations

```pentlang
let v1 = [1, 2, 3, 4, 5]
let v2 = [10, 20, 30, 40, 50]

// Element-wise operations
let v3 = v1 + v2
let v4 = v1 * 2

// Dot product
let dot = v1 * v2

// PNPU MAC operation
let weights = [+2, -1, +1, 0, +2]
let mac_result = v1.mac(weights)
```

### Matrix Operations

```pentlang
let matrix = [[+2, -1, 0], [+1, +2, -1], [0, +1, +2]]
let vector = [10, 20, 30]

// Matrix-vector multiplication using PNPU MAC
let output = matrix.matrix_vector_multiply(vector)
```

## PNPU Architecture Benefits

### 1. No Multipliers
- Standard GPUs: ~3,000 transistors per FP16 multiplier
- PNPU: ~150 transistors per shift-add MAC (20x reduction)

### 2. Memory Efficiency
- Binary SRAM: 6 transistors = 1 bit
- Pentary SRAM: 12 transistors = 2.32 bits
- **~40% higher information density**

### 3. Power Efficiency
- Zero state (0) physically disconnects circuits
- Massive sparsity and power savings
- ~25W TDP for 24B parameter models

### 4. Symmetric Representation
- Negative and positive numbers are symmetric
- Natural for excitatory/inhibitory neural networks

## Example: Neural Network Layer

```pentlang
// Simple neural network layer using PNPU
function neural_layer(weights, activations) {
    let outputs = []
    
    for weight_row in weights {
        let row_vector = weight_row
        let result = activations.mac(row_vector)
        outputs = outputs + [result]
    }
    
    return outputs
}

// Example usage
let weights = [[+2, -1, +1], [-1, +2, 0], [+1, -1, +2]]
let inputs = [10, 20, 30]

let outputs = neural_layer(weights, inputs)
print("Layer outputs:", outputs)
```

## Comparison: TritLang vs PentLang

| Feature | TritLang | PentLang |
|---------|----------|----------|
| Base | Balanced Ternary (-1, 0, +1) | Balanced Quinary (-2, -1, 0, +1, +2) |
| States | 3 | 5 |
| Logic | True/False/Maybe | AbsoluteYes/MaybeYes/Unknown/MaybeNo/AbsoluteNo |
| Use Case | General trinary computing | PNPU neural network inference |
| Operations | Standard arithmetic | Shift-add MAC optimized |

## Installation

```bash
# From workspace root
pip install -e .
```

## Examples

See the `examples/` directory for complete examples:
- `hello_pentary.pent` - Basic introduction
- `five_state_logic.pent` - Five-state boolean operations
- `pnpu_mac.pent` - Shift-add MAC operations
- `neural_layer.pent` - Neural network layer simulation

## Documentation

For complete documentation, see the main project README and the PentLang source code.

## License

This project is part of the Trinary/Pentary Python project and follows the same license.
