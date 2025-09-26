"""
Trinary data types implementation.

This module provides specialized trinary types:
- TrinaryInt: Integer operations in base 3
- TrinaryFloat: Floating point representation in trinary
- TrinaryBool: Three-state logic (True, False, Unknown/Maybe)
"""

from typing import Union, Optional, Any
from .core import TrinaryNumber, BalancedTernary


class TrinaryInt(TrinaryNumber):
    """
    Integer type that operates in trinary base.
    
    Extends TrinaryNumber with integer-specific operations like
    floor division, modulo, and bitwise operations adapted for trinary.
    """
    
    def __init__(self, value: Union[int, str, list]):
        """Initialize a TrinaryInt."""
        super().__init__(value)
        # Ensure we're working with integer values
        self._decimal_value = int(self._decimal_value)
    
    def __floordiv__(self, other) -> 'TrinaryInt':
        """Floor division operation."""
        if isinstance(other, (TrinaryNumber, int)):
            other_val = other.decimal_value if hasattr(other, 'decimal_value') else other
            if other_val == 0:
                raise ZeroDivisionError("Division by zero")
            return TrinaryInt(self._decimal_value // other_val)
        return NotImplemented
    
    def __mod__(self, other) -> 'TrinaryInt':
        """Modulo operation."""
        if isinstance(other, (TrinaryNumber, int)):
            other_val = other.decimal_value if hasattr(other, 'decimal_value') else other
            if other_val == 0:
                raise ZeroDivisionError("Modulo by zero")
            return TrinaryInt(self._decimal_value % other_val)
        return NotImplemented
    
    def __pow__(self, other) -> 'TrinaryInt':
        """Power operation."""
        if isinstance(other, (TrinaryNumber, int)):
            other_val = other.decimal_value if hasattr(other, 'decimal_value') else other
            return TrinaryInt(self._decimal_value ** other_val)
        return NotImplemented
    
    def trit_shift_left(self, positions: int) -> 'TrinaryInt':
        """
        Shift trits to the left (equivalent to multiplying by 3^positions).
        
        Args:
            positions: Number of positions to shift left
        """
        return TrinaryInt(self._decimal_value * (3 ** positions))
    
    def trit_shift_right(self, positions: int) -> 'TrinaryInt':
        """
        Shift trits to the right (equivalent to floor division by 3^positions).
        
        Args:
            positions: Number of positions to shift right
        """
        return TrinaryInt(self._decimal_value // (3 ** positions))
    
    def count_trits(self) -> int:
        """Count the number of trits in the representation."""
        return len(self._trits) - (1 if self.is_negative else 0)
    
    def to_balanced_ternary(self) -> BalancedTernary:
        """Convert to balanced ternary representation."""
        return BalancedTernary(self._decimal_value)


class TrinaryFloat:
    """
    Floating point representation in trinary.
    
    Represents fractional numbers using trinary digits with a radix point.
    Format: integer_part.fractional_part in base 3
    """
    
    def __init__(self, value: Union[float, str, int], precision: int = 10):
        """
        Initialize a TrinaryFloat.
        
        Args:
            value: Decimal float, string representation, or integer
            precision: Number of fractional trits to maintain
        """
        self.precision = precision
        
        if isinstance(value, (int, float)):
            self._decimal_value = float(value)
            self._integer_part = TrinaryInt(int(value))
            self._fractional_trits = self._decimal_fraction_to_trinary(
                abs(value) - abs(int(value))
            )
        elif isinstance(value, str):
            self._parse_trinary_float_string(value)
        else:
            raise TypeError(f"Unsupported type for TrinaryFloat: {type(value)}")
    
    def _decimal_fraction_to_trinary(self, fraction: float) -> list:
        """Convert decimal fraction to trinary fractional digits."""
        trits = []
        for _ in range(self.precision):
            if fraction == 0:
                break
            fraction *= 3
            digit = int(fraction)
            trits.append(digit)
            fraction -= digit
        return trits
    
    def _trinary_fraction_to_decimal(self, trits: list) -> float:
        """Convert trinary fractional digits to decimal fraction."""
        decimal = 0.0
        for i, trit in enumerate(trits):
            decimal += trit * (3 ** -(i + 1))
        return decimal
    
    def _parse_trinary_float_string(self, float_str: str):
        """Parse trinary float string like '102.12' or '-21.201'."""
        float_str = float_str.strip()
        is_negative = float_str.startswith('-')
        
        if is_negative:
            float_str = float_str[1:]
        
        if '.' not in float_str:
            # No fractional part
            self._integer_part = TrinaryInt(float_str)
            self._fractional_trits = []
        else:
            integer_str, fractional_str = float_str.split('.', 1)
            self._integer_part = TrinaryInt(integer_str if integer_str else "0")
            
            self._fractional_trits = []
            for char in fractional_str:
                if char not in '012':
                    raise ValueError(f"Invalid trinary character: {char}")
                self._fractional_trits.append(int(char))
        
        # Calculate decimal value
        integer_val = self._integer_part.decimal_value
        fractional_val = self._trinary_fraction_to_decimal(self._fractional_trits)
        
        self._decimal_value = integer_val + fractional_val
        if is_negative:
            self._decimal_value = -self._decimal_value
    
    @property
    def decimal_value(self) -> float:
        """Get the decimal equivalent."""
        return self._decimal_value
    
    @property
    def integer_part(self) -> TrinaryInt:
        """Get the integer part as TrinaryInt."""
        return self._integer_part
    
    @property
    def fractional_trits(self) -> list:
        """Get the fractional trits."""
        return self._fractional_trits[:]
    
    def __str__(self) -> str:
        """String representation in trinary format."""
        sign = "-" if self._decimal_value < 0 else ""
        integer_str = str(abs(self._integer_part.decimal_value))
        integer_trinary = TrinaryInt(int(integer_str))
        
        if not self._fractional_trits:
            return f"{sign}{integer_trinary}"
        else:
            fractional_str = "".join(str(t) for t in self._fractional_trits)
            return f"{sign}{integer_trinary}.{fractional_str}"
    
    def __repr__(self) -> str:
        """Official string representation."""
        return f"TrinaryFloat('{str(self)}')"
    
    def __add__(self, other) -> 'TrinaryFloat':
        """Addition operation."""
        if isinstance(other, (TrinaryFloat, float, int)):
            other_val = other.decimal_value if hasattr(other, 'decimal_value') else other
            return TrinaryFloat(self._decimal_value + other_val, self.precision)
        return NotImplemented
    
    def __sub__(self, other) -> 'TrinaryFloat':
        """Subtraction operation."""
        if isinstance(other, (TrinaryFloat, float, int)):
            other_val = other.decimal_value if hasattr(other, 'decimal_value') else other
            return TrinaryFloat(self._decimal_value - other_val, self.precision)
        return NotImplemented
    
    def __mul__(self, other) -> 'TrinaryFloat':
        """Multiplication operation."""
        if isinstance(other, (TrinaryFloat, float, int)):
            other_val = other.decimal_value if hasattr(other, 'decimal_value') else other
            return TrinaryFloat(self._decimal_value * other_val, self.precision)
        return NotImplemented
    
    def __truediv__(self, other) -> 'TrinaryFloat':
        """Division operation."""
        if isinstance(other, (TrinaryFloat, float, int)):
            other_val = other.decimal_value if hasattr(other, 'decimal_value') else other
            if other_val == 0:
                raise ZeroDivisionError("Division by zero")
            return TrinaryFloat(self._decimal_value / other_val, self.precision)
        return NotImplemented


class TrinaryBool:
    """
    Three-state logic implementation.
    
    Unlike binary boolean logic, trinary boolean supports three states:
    - True (1): Definitely true
    - False (0): Definitely false  
    - Maybe/Unknown (-1): Unknown or indeterminate state
    """
    
    TRUE = 1
    FALSE = 0
    MAYBE = -1
    
    def __init__(self, value: Union[bool, int, str, None]):
        """
        Initialize a TrinaryBool.
        
        Args:
            value: Can be:
                - bool: True/False maps to TRUE/FALSE
                - int: 1=TRUE, 0=FALSE, -1=MAYBE
                - str: "true"/"false"/"maybe" (case insensitive)
                - None: maps to MAYBE
        """
        if isinstance(value, bool):
            self._value = self.TRUE if value else self.FALSE
        elif isinstance(value, int):
            if value not in [-1, 0, 1]:
                raise ValueError("TrinaryBool integer value must be -1, 0, or 1")
            self._value = value
        elif isinstance(value, str):
            value_lower = value.lower().strip()
            if value_lower in ("true", "t", "1"):
                self._value = self.TRUE
            elif value_lower in ("false", "f", "0"):
                self._value = self.FALSE
            elif value_lower in ("maybe", "unknown", "m", "-1"):
                self._value = self.MAYBE
            else:
                raise ValueError(f"Invalid string value for TrinaryBool: {value}")
        elif value is None:
            self._value = self.MAYBE
        else:
            raise TypeError(f"Unsupported type for TrinaryBool: {type(value)}")
    
    @property
    def value(self) -> int:
        """Get the numeric value (-1, 0, or 1)."""
        return self._value
    
    @property
    def is_true(self) -> bool:
        """Check if the value is definitely true."""
        return self._value == self.TRUE
    
    @property
    def is_false(self) -> bool:
        """Check if the value is definitely false."""
        return self._value == self.FALSE
    
    @property
    def is_maybe(self) -> bool:
        """Check if the value is unknown/maybe."""
        return self._value == self.MAYBE
    
    def __bool__(self) -> bool:
        """Convert to Python bool (MAYBE becomes False for safety)."""
        return self._value == self.TRUE
    
    def __str__(self) -> str:
        """String representation."""
        if self._value == self.TRUE:
            return "True"
        elif self._value == self.FALSE:
            return "False"
        else:
            return "Maybe"
    
    def __repr__(self) -> str:
        """Official string representation."""
        return f"TrinaryBool({str(self)})"
    
    def __eq__(self, other) -> 'TrinaryBool':
        """Equality comparison (returns TrinaryBool)."""
        if isinstance(other, TrinaryBool):
            if self._value == other._value:
                if self._value == self.MAYBE:
                    # Maybe == Maybe is still Maybe (unknown)
                    return TrinaryBool(None)
                else:
                    return TrinaryBool(True)
            elif self._value == self.MAYBE or other._value == self.MAYBE:
                return TrinaryBool(None)  # Maybe
            else:
                return TrinaryBool(False)
        return TrinaryBool(False)
    
    def __and__(self, other) -> 'TrinaryBool':
        """Logical AND operation."""
        if not isinstance(other, TrinaryBool):
            other = TrinaryBool(other)
        
        # Trinary AND truth table
        if self._value == self.FALSE or other._value == self.FALSE:
            return TrinaryBool(False)
        elif self._value == self.TRUE and other._value == self.TRUE:
            return TrinaryBool(True)
        else:
            return TrinaryBool(None)  # Maybe
    
    def __or__(self, other) -> 'TrinaryBool':
        """Logical OR operation."""
        if not isinstance(other, TrinaryBool):
            other = TrinaryBool(other)
        
        # Trinary OR truth table
        if self._value == self.TRUE or other._value == self.TRUE:
            return TrinaryBool(True)
        elif self._value == self.FALSE and other._value == self.FALSE:
            return TrinaryBool(False)
        else:
            return TrinaryBool(None)  # Maybe
    
    def __invert__(self) -> 'TrinaryBool':
        """Logical NOT operation."""
        if self._value == self.TRUE:
            return TrinaryBool(False)
        elif self._value == self.FALSE:
            return TrinaryBool(True)
        else:
            return TrinaryBool(None)  # Maybe stays Maybe