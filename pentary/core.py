"""
Core pentary number system implementation for PNPU architecture.

This module provides the fundamental PentaryNumber class that handles
conversion between decimal and pentary representations, supporting
balanced quinary (-2, -1, 0, +1, +2) systems optimized for neural networks.
"""

from typing import Union, List, Optional
import math


class PentaryNumber:
    """
    Base class for pentary number representation.
    
    Supports balanced quinary (-2, -1, 0, +1, +2) representation where each digit
    represents a power of 5, optimized for PNPU hardware.
    """
    
    def __init__(self, value: Union[int, str, List[int]]):
        """
        Initialize a pentary number.
        
        Args:
            value: Can be:
                - int: decimal value to convert to pentary
                - str: pentary string representation (e.g., "+2-10")
                - List[int]: list of pentary digits (-2, -1, 0, 1, 2)
        """
        if isinstance(value, int):
            self._pentits = self._decimal_to_pentary(value)
            self._decimal_value = value
        elif isinstance(value, str):
            self._pentits = self._parse_pentary_string(value)
            self._decimal_value = self._pentary_to_decimal(self._pentits)
        elif isinstance(value, list):
            self._pentits = value[:]
            self._decimal_value = self._pentary_to_decimal(self._pentits)
        else:
            raise TypeError(f"Unsupported type for PentaryNumber: {type(value)}")
    
    def _decimal_to_pentary(self, decimal: int) -> List[int]:
        """Convert a decimal number to balanced quinary representation."""
        if decimal == 0:
            return [0]
        
        pentits = []
        n = abs(decimal)
        
        while n > 0:
            remainder = n % 5
            if remainder == 0:
                pentits.append(0)
                n //= 5
            elif remainder == 1:
                pentits.append(1)
                n //= 5
            elif remainder == 2:
                pentits.append(2)
                n //= 5
            elif remainder == 3:
                pentits.append(-2)  # 3 = 5 - 2
                n = (n + 2) // 5
            else:  # remainder == 4
                pentits.append(-1)  # 4 = 5 - 1
                n = (n + 1) // 5
        
        if decimal < 0:
            # Negate all pentits
            pentits = [-p for p in pentits]
        
        pentits.reverse()
        return pentits
    
    def _pentary_to_decimal(self, pentits: List[int]) -> int:
        """Convert pentary digits to decimal value."""
        if not pentits:
            return 0
        
        decimal = 0
        for i, pentit in enumerate(reversed(pentits)):
            if pentit not in [-2, -1, 0, 1, 2]:
                raise ValueError(f"Invalid pentit value: {pentit}. Must be -2, -1, 0, 1, or 2.")
            decimal += pentit * (5 ** i)
        
        return decimal
    
    def _parse_pentary_string(self, pentary_str: str) -> List[int]:
        """Parse a pentary string into a list of pentits."""
        pentary_str = pentary_str.strip()
        is_negative = pentary_str.startswith('-')
        
        if is_negative:
            pentary_str = pentary_str[1:]
        
        pentits = []
        for char in pentary_str:
            if char == '+':
                # Next char should be 1 or 2
                continue
            elif char == '2':
                pentits.append(2)
            elif char == '1':
                pentits.append(1)
            elif char == '0':
                pentits.append(0)
            elif char == '-':
                # Check if it's -1 or -2
                if len(pentary_str) > pentary_str.index(char) + 1:
                    next_char = pentary_str[pentary_str.index(char) + 1]
                    if next_char == '2':
                        pentits.append(-2)
                    elif next_char == '1':
                        pentits.append(-1)
                    else:
                        pentits.append(-1)  # Default to -1
                else:
                    pentits.append(-1)
            else:
                raise ValueError(f"Invalid pentary character: {char}")
        
        if is_negative:
            # Negate all pentits
            pentits = [-p for p in pentits]
        
        return pentits
    
    @property
    def pentits(self) -> List[int]:
        """Get the pentary digits (pentits)."""
        return self._pentits[:]
    
    @property
    def decimal_value(self) -> int:
        """Get the decimal equivalent."""
        return self._decimal_value
    
    @property
    def is_negative(self) -> bool:
        """Check if the number is negative."""
        return self._decimal_value < 0
    
    def __str__(self) -> str:
        """String representation in pentary format."""
        if not self._pentits:
            return "0"
        
        result = ""
        for pentit in self._pentits:
            if pentit == 2:
                result += "+2"
            elif pentit == 1:
                result += "+1"
            elif pentit == 0:
                result += "0"
            elif pentit == -1:
                result += "-1"
            elif pentit == -2:
                result += "-2"
        
        return result
    
    def __repr__(self) -> str:
        """Official string representation."""
        return f"PentaryNumber('{str(self)}')"
    
    def __eq__(self, other) -> bool:
        """Equality comparison."""
        if isinstance(other, PentaryNumber):
            return self._decimal_value == other._decimal_value
        elif isinstance(other, int):
            return self._decimal_value == other
        return False
    
    def __lt__(self, other) -> bool:
        """Less than comparison."""
        if isinstance(other, PentaryNumber):
            return self._decimal_value < other._decimal_value
        elif isinstance(other, int):
            return self._decimal_value < other
        return NotImplemented
    
    def __add__(self, other) -> 'PentaryNumber':
        """Addition operation."""
        if isinstance(other, PentaryNumber):
            return PentaryNumber(self._decimal_value + other._decimal_value)
        elif isinstance(other, int):
            return PentaryNumber(self._decimal_value + other)
        return NotImplemented
    
    def __sub__(self, other) -> 'PentaryNumber':
        """Subtraction operation."""
        if isinstance(other, PentaryNumber):
            return PentaryNumber(self._decimal_value - other._decimal_value)
        elif isinstance(other, int):
            return PentaryNumber(self._decimal_value - other)
        return NotImplemented
    
    def __mul__(self, other) -> 'PentaryNumber':
        """Multiplication operation."""
        if isinstance(other, PentaryNumber):
            return PentaryNumber(self._decimal_value * other._decimal_value)
        elif isinstance(other, int):
            return PentaryNumber(self._decimal_value * other)
        return NotImplemented


class BalancedQuinary(PentaryNumber):
    """
    Balanced quinary number representation using digits {-2, -1, 0, +1, +2}.
    
    In balanced quinary, negative and positive values are represented
    symmetrically, making it ideal for PNPU hardware where operations
    are performed using shift-add logic.
    """
    
    def __init__(self, value: Union[int, str, List[int]]):
        """
        Initialize a balanced quinary number.
        
        Args:
            value: Can be:
                - int: decimal value to convert to balanced quinary
                - str: balanced quinary string using '+2', '+1', '0', '-1', '-2'
                - List[int]: list of balanced quinary digits (-2, -1, 0, 1, 2)
        """
        if isinstance(value, str):
            self._pentits = self._parse_balanced_string(value)
            self._decimal_value = self._balanced_to_decimal(self._pentits)
        elif isinstance(value, int):
            self._pentits = self._decimal_to_pentary(value)
            self._decimal_value = value
        elif isinstance(value, list):
            self._pentits = value[:]
            self._decimal_value = self._balanced_to_decimal(self._pentits)
        else:
            raise TypeError(f"Unsupported type for BalancedQuinary: {type(value)}")
    
    def _balanced_to_decimal(self, pentits: List[int]) -> int:
        """Convert balanced quinary digits to decimal."""
        decimal = 0
        for i, pentit in enumerate(reversed(pentits)):
            if pentit not in [-2, -1, 0, 1, 2]:
                raise ValueError(f"Invalid balanced quinary digit: {pentit}")
            decimal += pentit * (5 ** i)
        return decimal
    
    def _parse_balanced_string(self, bq_str: str) -> List[int]:
        """Parse balanced quinary string."""
        pentits = []
        i = 0
        while i < len(bq_str):
            char = bq_str[i]
            if char == '+':
                if i + 1 < len(bq_str):
                    next_char = bq_str[i + 1]
                    if next_char == '2':
                        pentits.append(2)
                        i += 2
                    elif next_char == '1':
                        pentits.append(1)
                        i += 2
                    else:
                        pentits.append(1)
                        i += 1
                else:
                    pentits.append(1)
                    i += 1
            elif char == '-':
                if i + 1 < len(bq_str):
                    next_char = bq_str[i + 1]
                    if next_char == '2':
                        pentits.append(-2)
                        i += 2
                    elif next_char == '1':
                        pentits.append(-1)
                        i += 2
                    else:
                        pentits.append(-1)
                        i += 1
                else:
                    pentits.append(-1)
                    i += 1
            elif char == '0':
                pentits.append(0)
                i += 1
            elif char == '1':
                pentits.append(1)
                i += 1
            elif char == '2':
                pentits.append(2)
                i += 1
            else:
                i += 1  # Skip unknown characters
        
        return pentits
    
    def __str__(self) -> str:
        """String representation using +2, +1, 0, -1, -2."""
        if not self._pentits:
            return "0"
        
        result = ""
        for pentit in self._pentits:
            if pentit == 2:
                result += "+2"
            elif pentit == 1:
                result += "+1"
            elif pentit == 0:
                result += "0"
            elif pentit == -1:
                result += "-1"
            elif pentit == -2:
                result += "-2"
        return result
    
    def __repr__(self) -> str:
        """Official string representation."""
        return f"BalancedQuinary('{str(self)}')"
