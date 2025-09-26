#!/usr/bin/env python3
"""
Basic usage examples for Trinary Python.

This script demonstrates the fundamental features of the trinary computing
system including number representation, arithmetic, and type conversions.
"""

from trinary import TrinaryNumber, TrinaryInt, TrinaryFloat, TrinaryBool, BalancedTernary


def demonstrate_basic_numbers():
    """Show basic trinary number creation and representation."""
    print("=== Basic Trinary Numbers ===")
    
    # Creating trinary numbers from decimal
    numbers = [0, 1, 2, 3, 9, 27, 100]
    
    for decimal in numbers:
        trinary = TrinaryNumber(decimal)
        print(f"Decimal {decimal:3d} = Trinary {trinary}")
    
    print()
    
    # Creating from trinary strings
    trinary_strings = ["0", "1", "2", "10", "102", "1201", "22222"]
    
    for tri_str in trinary_strings:
        trinary = TrinaryNumber(tri_str)
        print(f"Trinary '{tri_str}' = Decimal {trinary.decimal_value}")
    
    print()


def demonstrate_arithmetic():
    """Show arithmetic operations in trinary."""
    print("=== Trinary Arithmetic ===")
    
    a = TrinaryInt(13)  # "111" in trinary
    b = TrinaryInt(8)   # "22" in trinary
    
    print(f"a = {a} (decimal: {a.decimal_value})")
    print(f"b = {b} (decimal: {b.decimal_value})")
    print()
    
    operations = [
        ("Addition", a + b),
        ("Subtraction", a - b),
        ("Multiplication", a * b),
        ("Floor Division", a // b),
        ("Modulo", a % b),
        ("Power", TrinaryInt(3) ** TrinaryInt(3)),
    ]
    
    for name, result in operations:
        print(f"{name:15}: {result} (decimal: {result.decimal_value})")
    
    print()


def demonstrate_balanced_ternary():
    """Show balanced ternary representation."""
    print("=== Balanced Ternary ===")
    print("Using digits: T (-1), 0, 1")
    print()
    
    numbers = [-5, -3, -1, 0, 1, 3, 5, 10, 13]
    
    for decimal in numbers:
        bt = BalancedTernary(decimal)
        std_ternary = TrinaryNumber(decimal)
        print(f"Decimal {decimal:3d} = Standard: {std_ternary:>6} | Balanced: {bt:>6}")
    
    print()
    
    # Show symmetry property
    print("Symmetry demonstration:")
    for i in [4, 7, 12]:
        pos_bt = BalancedTernary(i)
        neg_bt = BalancedTernary(-i)
        print(f"+{i}: {pos_bt:>6} | -{i}: {neg_bt:>6}")
    
    print()


def demonstrate_floating_point():
    """Show trinary floating point numbers."""
    print("=== Trinary Floating Point ===")
    
    # Create from decimal
    decimal_values = [3.5, 1.333, 0.75, 10.25]
    
    for decimal in decimal_values:
        tf = TrinaryFloat(decimal, precision=8)
        print(f"Decimal {decimal:6.3f} ≈ Trinary {tf}")
    
    print()
    
    # Create from trinary string
    trinary_floats = ["10.1", "2.22", "101.012"]
    
    for tri_str in trinary_floats:
        tf = TrinaryFloat(tri_str)
        print(f"Trinary '{tri_str}' = Decimal {tf.decimal_value:.6f}")
    
    print()
    
    # Arithmetic with floats
    a = TrinaryFloat(2.5)
    b = TrinaryFloat(1.25)
    
    print(f"Float arithmetic:")
    print(f"{a} + {b} = {a + b}")
    print(f"{a} * {b} = {a * b}")
    print(f"{a} / {b} = {a / b}")
    
    print()


def demonstrate_three_state_logic():
    """Show three-state boolean logic."""
    print("=== Three-State Logic ===")
    
    # Create different boolean states
    true_val = TrinaryBool(True)
    false_val = TrinaryBool(False)
    maybe_val = TrinaryBool("maybe")
    
    print(f"True:  {true_val}")
    print(f"False: {false_val}")
    print(f"Maybe: {maybe_val}")
    print()
    
    # Truth tables
    values = [true_val, false_val, maybe_val]
    names = ["True", "False", "Maybe"]
    
    print("AND Truth Table:")
    print("      |  True  | False | Maybe")
    print("------|--------|-------|-------")
    
    for i, a in enumerate(values):
        row = f"{names[i]:5} |"
        for b in values:
            result = a & b
            row += f" {str(result):5} |"
        print(row)
    
    print()
    print("OR Truth Table:")
    print("      |  True  | False | Maybe")
    print("------|--------|-------|-------")
    
    for i, a in enumerate(values):
        row = f"{names[i]:5} |"
        for b in values:
            result = a | b
            row += f" {str(result):5} |"
        print(row)
    
    print()
    
    # NOT operation
    print("NOT Operation:")
    for i, val in enumerate(values):
        print(f"NOT {names[i]:5} = {~val}")
    
    print()


def demonstrate_trit_operations():
    """Show trit-level operations."""
    print("=== Trit Operations ===")
    
    a = TrinaryInt(10)  # "101"
    b = TrinaryInt(6)   # "20"
    
    print(f"a = {a} (decimal: {a.decimal_value})")
    print(f"b = {b} (decimal: {b.decimal_value})")
    print()
    
    # Trit shifting
    print("Trit Shifting:")
    print(f"a << 1 trit: {a.trit_shift_left(1)} (decimal: {a.trit_shift_left(1).decimal_value})")
    print(f"a << 2 trits: {a.trit_shift_left(2)} (decimal: {a.trit_shift_left(2).decimal_value})")
    
    larger = TrinaryInt(27)  # "1000"
    print(f"{larger} >> 1 trit: {larger.trit_shift_right(1)} (decimal: {larger.trit_shift_right(1).decimal_value})")
    
    print()
    
    # Trit counting
    test_numbers = [1, 3, 9, 27, 100]
    print("Trit counting:")
    for num in test_numbers:
        ti = TrinaryInt(num)
        print(f"Number {num:3d} ({ti}) has {ti.count_trits()} trits")
    
    print()


def main():
    """Run all demonstrations."""
    print("Trinary Python - Basic Usage Examples")
    print("=" * 50)
    print()
    
    demonstrate_basic_numbers()
    demonstrate_arithmetic()
    demonstrate_balanced_ternary()
    demonstrate_floating_point()
    demonstrate_three_state_logic()
    demonstrate_trit_operations()
    
    print("All demonstrations completed!")


if __name__ == "__main__":
    main()