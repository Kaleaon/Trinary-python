"""
Trinary Python - A Python implementation for trinary (base-3) computing systems

This package provides:
- TrinaryNumber: Core trinary number representation and operations
- TrinaryInt: Integer operations in base 3
- TrinaryFloat: Floating point representation in trinary
- TrinaryBool: Three-state logic (True, False, Unknown/Maybe)
- Memory management for trinary systems using trits instead of bits
"""

from .core import TrinaryNumber, BalancedTernary
from .types import TrinaryInt, TrinaryFloat, TrinaryBool
from .operations import TrinaryOperations
from .memory import TrinaryMemory

__version__ = "0.1.0"
__all__ = [
    "TrinaryNumber",
    "BalancedTernary", 
    "TrinaryInt",
    "TrinaryFloat",
    "TrinaryBool",
    "TrinaryOperations",
    "TrinaryMemory",
]