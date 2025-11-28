"""
Pentary - Balanced Quinary (Base-5) computing system for PNPU architecture.

This package provides:
- PentaryNumber: Core pentary number representation using {-2, -1, 0, +1, +2}
- PentaryInt: Integer operations in base 5
- PentaryFloat: Floating point representation in pentary
- PentaryBool: Five-state logic for neural network operations
- PentaryOperations: Shift-add operations optimized for PNPU
"""

from .core import PentaryNumber, BalancedQuinary
from .types import PentaryInt, PentaryFloat, PentaryBool
from .operations import PentaryOperations
from .pnpu import PNPUCore, ShiftAddMAC

__version__ = "0.1.0"
__all__ = [
    "PentaryNumber",
    "BalancedQuinary",
    "PentaryInt",
    "PentaryFloat",
    "PentaryBool",
    "PentaryOperations",
    "PNPUCore",
    "ShiftAddMAC",
]
