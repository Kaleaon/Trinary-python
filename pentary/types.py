"""
Pentary data types implementation for PNPU architecture.

This module provides specialized pentary types:
- PentaryInt: Integer operations in base 5
- PentaryFloat: Floating point representation in pentary
- PentaryBool: Five-state logic for neural networks
"""

from typing import Union, Optional, Any
from .core import PentaryNumber, BalancedQuinary


class PentaryInt(PentaryNumber):
    """
    Integer type that operates in pentary base.
    
    Extends PentaryNumber with integer-specific operations optimized
    for PNPU shift-add architecture.
    """
    
    def __init__(self, value: Union[int, str, list]):
        """Initialize a PentaryInt."""
        super().__init__(value)
        self._decimal_value = int(self._decimal_value)
    
    def __floordiv__(self, other) -> 'PentaryInt':
        """Floor division operation."""
        if isinstance(other, (PentaryNumber, int)):
            other_val = other.decimal_value if hasattr(other, 'decimal_value') else other
            if other_val == 0:
                raise ZeroDivisionError("Division by zero")
            return PentaryInt(self._decimal_value // other_val)
        return NotImplemented
    
    def __mod__(self, other) -> 'PentaryInt':
        """Modulo operation."""
        if isinstance(other, (PentaryNumber, int)):
            other_val = other.decimal_value if hasattr(other, 'decimal_value') else other
            if other_val == 0:
                raise ZeroDivisionError("Modulo by zero")
            return PentaryInt(self._decimal_value % other_val)
        return NotImplemented
    
    def __pow__(self, other) -> 'PentaryInt':
        """Power operation."""
        if isinstance(other, (PentaryNumber, int)):
            other_val = other.decimal_value if hasattr(other, 'decimal_value') else other
            return PentaryInt(self._decimal_value ** other_val)
        return NotImplemented
    
    def pentit_shift_left(self, positions: int) -> 'PentaryInt':
        """
        Shift pentits to the left (equivalent to multiplying by 5^positions).
        
        Args:
            positions: Number of positions to shift left
        """
        return PentaryInt(self._decimal_value * (5 ** positions))
    
    def pentit_shift_right(self, positions: int) -> 'PentaryInt':
        """
        Shift pentits to the right (equivalent to floor division by 5^positions).
        
        Args:
            positions: Number of positions to shift right
        """
        return PentaryInt(self._decimal_value // (5 ** positions))
    
    def count_pentits(self) -> int:
        """Count the number of pentits in the representation."""
        return len(self._pentits)
    
    def to_balanced_quinary(self) -> BalancedQuinary:
        """Convert to balanced quinary representation."""
        return BalancedQuinary(self._decimal_value)


class PentaryFloat:
    """
    Floating point representation in pentary.
    
    Represents fractional numbers using pentary digits with a radix point.
    Format: integer_part.fractional_part in base 5
    """
    
    def __init__(self, value: Union[float, str, int], precision: int = 10):
        """
        Initialize a PentaryFloat.
        
        Args:
            value: Decimal float, string representation, or integer
            precision: Number of fractional pentits to maintain
        """
        self.precision = precision
        
        if isinstance(value, (int, float)):
            self._decimal_value = float(value)
            self._integer_part = PentaryInt(int(value))
            self._fractional_pentits = self._decimal_fraction_to_pentary(
                abs(value) - abs(int(value))
            )
        elif isinstance(value, str):
            self._parse_pentary_float_string(value)
        else:
            raise TypeError(f"Unsupported type for PentaryFloat: {type(value)}")
    
    def _decimal_fraction_to_pentary(self, fraction: float) -> list:
        """Convert decimal fraction to pentary fractional digits."""
        pentits = []
        for _ in range(self.precision):
            if fraction == 0:
                break
            fraction *= 5
            digit = int(fraction)
            # Convert to balanced quinary
            if digit >= 3:
                pentits.append(digit - 5)  # Convert 3->-2, 4->-1
            else:
                pentits.append(digit)
            fraction -= int(fraction)
        return pentits
    
    def _pentary_fraction_to_decimal(self, pentits: list) -> float:
        """Convert pentary fractional digits to decimal fraction."""
        decimal = 0.0
        for i, pentit in enumerate(pentits):
            decimal += pentit * (5 ** -(i + 1))
        return decimal
    
    def _parse_pentary_float_string(self, float_str: str):
        """Parse pentary float string."""
        float_str = float_str.strip()
        is_negative = float_str.startswith('-')
        
        if is_negative:
            float_str = float_str[1:]
        
        if '.' not in float_str:
            self._integer_part = PentaryInt(float_str if float_str else "0")
            self._fractional_pentits = []
        else:
            integer_str, fractional_str = float_str.split('.', 1)
            self._integer_part = PentaryInt(integer_str if integer_str else "0")
            
            self._fractional_pentits = []
            i = 0
            while i < len(fractional_str):
                if fractional_str[i] == '+':
                    if i + 1 < len(fractional_str):
                        next_char = fractional_str[i + 1]
                        if next_char == '2':
                            self._fractional_pentits.append(2)
                            i += 2
                        elif next_char == '1':
                            self._fractional_pentits.append(1)
                            i += 2
                        else:
                            self._fractional_pentits.append(1)
                            i += 1
                    else:
                        self._fractional_pentits.append(1)
                        i += 1
                elif fractional_str[i] == '-':
                    if i + 1 < len(fractional_str):
                        next_char = fractional_str[i + 1]
                        if next_char == '2':
                            self._fractional_pentits.append(-2)
                            i += 2
                        elif next_char == '1':
                            self._fractional_pentits.append(-1)
                            i += 2
                        else:
                            self._fractional_pentits.append(-1)
                            i += 1
                    else:
                        self._fractional_pentits.append(-1)
                        i += 1
                elif fractional_str[i] == '0':
                    self._fractional_pentits.append(0)
                    i += 1
                else:
                    i += 1
        
        integer_val = self._integer_part.decimal_value
        fractional_val = self._pentary_fraction_to_decimal(self._fractional_pentits)
        
        self._decimal_value = integer_val + fractional_val
        if is_negative:
            self._decimal_value = -self._decimal_value
    
    @property
    def decimal_value(self) -> float:
        """Get the decimal equivalent."""
        return self._decimal_value
    
    def __str__(self) -> str:
        """String representation in pentary format."""
        sign = "-" if self._decimal_value < 0 else ""
        integer_str = str(abs(self._integer_part.decimal_value))
        integer_pentary = PentaryInt(int(integer_str))
        
        if not self._fractional_pentits:
            return f"{sign}{integer_pentary}"
        else:
            fractional_str = "".join(
                "+2" if p == 2 else "+1" if p == 1 else "0" if p == 0 else "-1" if p == -1 else "-2"
                for p in self._fractional_pentits
            )
            return f"{sign}{integer_pentary}.{fractional_str}"
    
    def __add__(self, other) -> 'PentaryFloat':
        """Addition operation."""
        if isinstance(other, (PentaryFloat, float, int)):
            other_val = other.decimal_value if hasattr(other, 'decimal_value') else other
            return PentaryFloat(self._decimal_value + other_val, self.precision)
        return NotImplemented


class PentaryBool:
    """
    Five-state logic implementation for neural networks.
    
    Unlike binary boolean logic, pentary boolean supports five states:
    - +2: Absolute Yes (Strong activation)
    - +1: Maybe Yes (Weak activation)
    - 0: Unknown/Null (No signal)
    - -1: Maybe No (Weak inhibition)
    - -2: Absolute No (Strong inhibition)
    """
    
    ABSOLUTE_YES = 2
    MAYBE_YES = 1
    UNKNOWN = 0
    MAYBE_NO = -1
    ABSOLUTE_NO = -2
    
    def __init__(self, value: Union[bool, int, str, None]):
        """
        Initialize a PentaryBool.
        
        Args:
            value: Can be:
                - bool: True/False maps to ABSOLUTE_YES/ABSOLUTE_NO
                - int: 2=ABSOLUTE_YES, 1=MAYBE_YES, 0=UNKNOWN, -1=MAYBE_NO, -2=ABSOLUTE_NO
                - str: "yes"/"maybe_yes"/"unknown"/"maybe_no"/"no" (case insensitive)
                - None: maps to UNKNOWN
        """
        if isinstance(value, bool):
            self._value = self.ABSOLUTE_YES if value else self.ABSOLUTE_NO
        elif isinstance(value, int):
            if value not in [-2, -1, 0, 1, 2]:
                raise ValueError("PentaryBool integer value must be -2, -1, 0, 1, or 2")
            self._value = value
        elif isinstance(value, str):
            value_lower = value.lower().strip()
            if value_lower in ("yes", "absolute_yes", "2", "+2"):
                self._value = self.ABSOLUTE_YES
            elif value_lower in ("maybe_yes", "weak_yes", "1", "+1"):
                self._value = self.MAYBE_YES
            elif value_lower in ("unknown", "null", "0", "none"):
                self._value = self.UNKNOWN
            elif value_lower in ("maybe_no", "weak_no", "-1"):
                self._value = self.MAYBE_NO
            elif value_lower in ("no", "absolute_no", "-2"):
                self._value = self.ABSOLUTE_NO
            else:
                raise ValueError(f"Invalid string value for PentaryBool: {value}")
        elif value is None:
            self._value = self.UNKNOWN
        else:
            raise TypeError(f"Unsupported type for PentaryBool: {type(value)}")
    
    @property
    def value(self) -> int:
        """Get the numeric value (-2, -1, 0, 1, or 2)."""
        return self._value
    
    def __str__(self) -> str:
        """String representation."""
        if self._value == self.ABSOLUTE_YES:
            return "AbsoluteYes"
        elif self._value == self.MAYBE_YES:
            return "MaybeYes"
        elif self._value == self.UNKNOWN:
            return "Unknown"
        elif self._value == self.MAYBE_NO:
            return "MaybeNo"
        else:
            return "AbsoluteNo"
    
    def __repr__(self) -> str:
        """Official string representation."""
        return f"PentaryBool({str(self)})"
    
    def __bool__(self) -> bool:
        """Convert to Python bool (only ABSOLUTE_YES is True)."""
        return self._value == self.ABSOLUTE_YES
