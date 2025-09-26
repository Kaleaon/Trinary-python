"""
Core trinary number system implementation.

This module provides the fundamental TrinaryNumber class that handles
conversion between decimal and trinary representations, supporting both
standard ternary (0, 1, 2) and balanced ternary (-1, 0, 1) systems.
"""

from typing import Union, List, Optional
import math


class TrinaryNumber:
    """
    Base class for trinary number representation.
    
    Supports standard ternary (0, 1, 2) representation where each digit
    represents a power of 3.
    """
    
    def __init__(self, value: Union[int, str, List[int]]):
        """
        Initialize a trinary number.
        
        Args:
            value: Can be:
                - int: decimal value to convert to trinary
                - str: trinary string representation (e.g., "102")
                - List[int]: list of trinary digits
        """
        if isinstance(value, int):
            self._trits = self._decimal_to_trinary(value)
            self._decimal_value = value
        elif isinstance(value, str):
            self._trits = self._parse_trinary_string(value)
            self._decimal_value = self._trinary_to_decimal(self._trits)
        elif isinstance(value, list):
            self._trits = value[:]
            self._decimal_value = self._trinary_to_decimal(self._trits)
        else:
            raise TypeError(f"Unsupported type for TrinaryNumber: {type(value)}")
    
    def _decimal_to_trinary(self, decimal: int) -> List[int]:
        """Convert a decimal number to trinary representation."""
        if decimal == 0:
            return [0]
        
        trits = []
        is_negative = decimal < 0
        decimal = abs(decimal)
        
        while decimal > 0:
            remainder = decimal % 3
            trits.append(remainder)
            decimal //= 3
        
        trits.reverse()
        
        if is_negative:
            # For negative numbers, we'll use a sign bit approach for now
            # In a full implementation, balanced ternary would be preferred
            trits.insert(0, -1)  # -1 as sign indicator
        
        return trits
    
    def _trinary_to_decimal(self, trits: List[int]) -> int:
        """Convert trinary digits to decimal value."""
        if not trits:
            return 0
        
        is_negative = trits[0] == -1
        actual_trits = trits[1:] if is_negative else trits
        
        decimal = 0
        for i, trit in enumerate(reversed(actual_trits)):
            if trit not in [0, 1, 2]:
                raise ValueError(f"Invalid trit value: {trit}. Must be 0, 1, or 2.")
            decimal += trit * (3 ** i)
        
        return -decimal if is_negative else decimal
    
    def _parse_trinary_string(self, trinary_str: str) -> List[int]:
        """Parse a trinary string into a list of trits."""
        trinary_str = trinary_str.strip()
        is_negative = trinary_str.startswith('-')
        
        if is_negative:
            trinary_str = trinary_str[1:]
        
        trits = []
        for char in trinary_str:
            if char not in '012':
                raise ValueError(f"Invalid trinary character: {char}")
            trits.append(int(char))
        
        if is_negative:
            trits.insert(0, -1)
        
        return trits
    
    @property
    def trits(self) -> List[int]:
        """Get the trinary digits (trits)."""
        return self._trits[:]
    
    @property
    def decimal_value(self) -> int:
        """Get the decimal equivalent."""
        return self._decimal_value
    
    @property
    def is_negative(self) -> bool:
        """Check if the number is negative."""
        return self._trits and self._trits[0] == -1
    
    def __str__(self) -> str:
        """String representation in trinary format."""
        if not self._trits:
            return "0"
        
        if self.is_negative:
            return "-" + "".join(str(t) for t in self._trits[1:])
        else:
            return "".join(str(t) for t in self._trits)
    
    def __repr__(self) -> str:
        """Official string representation."""
        return f"TrinaryNumber('{str(self)}')"
    
    def __format__(self, format_spec: str) -> str:
        """Format the trinary number as a string."""
        return format(str(self), format_spec)
    
    def __eq__(self, other) -> bool:
        """Equality comparison."""
        if isinstance(other, TrinaryNumber):
            return self._decimal_value == other._decimal_value
        elif isinstance(other, int):
            return self._decimal_value == other
        return False
    
    def __lt__(self, other) -> bool:
        """Less than comparison."""
        if isinstance(other, TrinaryNumber):
            return self._decimal_value < other._decimal_value
        elif isinstance(other, int):
            return self._decimal_value < other
        return NotImplemented
    
    def __add__(self, other) -> 'TrinaryNumber':
        """Addition operation."""
        if isinstance(other, TrinaryNumber):
            return TrinaryNumber(self._decimal_value + other._decimal_value)
        elif isinstance(other, int):
            return TrinaryNumber(self._decimal_value + other)
        return NotImplemented
    
    def __sub__(self, other) -> 'TrinaryNumber':
        """Subtraction operation."""
        if isinstance(other, TrinaryNumber):
            return TrinaryNumber(self._decimal_value - other._decimal_value)
        elif isinstance(other, int):
            return TrinaryNumber(self._decimal_value - other)
        return NotImplemented
    
    def __mul__(self, other) -> 'TrinaryNumber':
        """Multiplication operation."""
        if isinstance(other, TrinaryNumber):
            return TrinaryNumber(self._decimal_value * other._decimal_value)
        elif isinstance(other, int):
            return TrinaryNumber(self._decimal_value * other)
        return NotImplemented


class BalancedTernary(TrinaryNumber):
    """
    Balanced ternary number representation using digits {-1, 0, 1}.
    
    In balanced ternary, negative and positive values are represented
    symmetrically, making it useful for certain computations.
    """
    
    def __init__(self, value: Union[int, str, List[int]]):
        """
        Initialize a balanced ternary number.
        
        Args:
            value: Can be:
                - int: decimal value to convert to balanced ternary
                - str: balanced ternary string using 'T' for -1, '0' for 0, '1' for 1
                - List[int]: list of balanced ternary digits (-1, 0, 1)
        """
        if isinstance(value, str):
            # Parse balanced ternary string notation (T for -1)
            self._trits = self._parse_balanced_string(value)
            self._decimal_value = self._balanced_to_decimal(self._trits)
        elif isinstance(value, int):
            self._trits = self._decimal_to_balanced(value)
            self._decimal_value = value
        elif isinstance(value, list):
            self._trits = value[:]
            self._decimal_value = self._balanced_to_decimal(self._trits)
        else:
            raise TypeError(f"Unsupported type for BalancedTernary: {type(value)}")
    
    def _decimal_to_balanced(self, decimal: int) -> List[int]:
        """Convert decimal to balanced ternary representation."""
        if decimal == 0:
            return [0]
        
        trits = []
        n = decimal
        
        while n != 0:
            if n % 3 == 0:
                trits.append(0)
                n //= 3
            elif n % 3 == 1:
                trits.append(1)
                n //= 3
            else:  # n % 3 == 2
                trits.append(-1)
                n = (n + 1) // 3
        
        trits.reverse()
        return trits
    
    def _balanced_to_decimal(self, trits: List[int]) -> int:
        """Convert balanced ternary digits to decimal."""
        decimal = 0
        for i, trit in enumerate(reversed(trits)):
            if trit not in [-1, 0, 1]:
                raise ValueError(f"Invalid balanced ternary digit: {trit}")
            decimal += trit * (3 ** i)
        return decimal
    
    def _parse_balanced_string(self, bt_str: str) -> List[int]:
        """Parse balanced ternary string (T for -1, 0 for 0, 1 for 1)."""
        trits = []
        for char in bt_str.strip():
            if char == 'T':
                trits.append(-1)
            elif char == '0':
                trits.append(0)
            elif char == '1':
                trits.append(1)
            else:
                raise ValueError(f"Invalid balanced ternary character: {char}")
        return trits
    
    def __str__(self) -> str:
        """String representation using T for -1."""
        if not self._trits:
            return "0"
        
        result = ""
        for trit in self._trits:
            if trit == -1:
                result += "T"
            else:
                result += str(trit)
        return result
    
    def __repr__(self) -> str:
        """Official string representation."""
        return f"BalancedTernary('{str(self)}')"
    
    def __format__(self, format_spec: str) -> str:
        """Format the balanced ternary number as a string."""
        return format(str(self), format_spec)
    
    @property
    def is_negative(self) -> bool:
        """Check if the number is negative based on balanced ternary value."""
        return self._decimal_value < 0