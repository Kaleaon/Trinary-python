"""
Runtime values and data structures for TritLang.

Handles balanced ternary arithmetic and ML-friendly data structures.
"""

from typing import List, Any, Union
from trinary.core import BalancedTernary


class TritValue:
    """
    Runtime value wrapper that can hold any TritLang value.
    Supports balanced ternary arithmetic.
    """
    
    def __init__(self, value: Any):
        self.value = value
    
    def to_balanced_ternary(self) -> BalancedTernary:
        """Convert numeric value to balanced ternary."""
        if isinstance(self.value, (int, float)):
            return BalancedTernary(int(self.value))
        return BalancedTernary(0)
    
    def __repr__(self):
        return f"TritValue({repr(self.value)})"
    
    def __str__(self):
        return str(self.value)
    
    def __add__(self, other):
        if isinstance(other, TritValue):
            return TritValue(self.value + other.value)
        return TritValue(self.value + other)
    
    def __sub__(self, other):
        if isinstance(other, TritValue):
            return TritValue(self.value - other.value)
        return TritValue(self.value - other)
    
    def __mul__(self, other):
        if isinstance(other, TritValue):
            return TritValue(self.value * other.value)
        return TritValue(self.value * other)
    
    def __truediv__(self, other):
        if isinstance(other, TritValue):
            if other.value == 0:
                raise ZeroDivisionError("Division by zero")
            return TritValue(self.value / other.value)
        if other == 0:
            raise ZeroDivisionError("Division by zero")
        return TritValue(self.value / other)
    
    def __mod__(self, other):
        if isinstance(other, TritValue):
            if other.value == 0:
                raise ZeroDivisionError("Modulo by zero")
            return TritValue(self.value % other.value)
        if other == 0:
            raise ZeroDivisionError("Modulo by zero")
        return TritValue(self.value % other)
    
    def __pow__(self, other):
        if isinstance(other, TritValue):
            return TritValue(self.value ** other.value)
        return TritValue(self.value ** other)
    
    def __eq__(self, other):
        if isinstance(other, TritValue):
            return TritValue(1 if self.value == other.value else 0)
        return TritValue(1 if self.value == other else 0)
    
    def __ne__(self, other):
        if isinstance(other, TritValue):
            return TritValue(1 if self.value != other.value else 0)
        return TritValue(1 if self.value != other else 0)
    
    def __lt__(self, other):
        if isinstance(other, TritValue):
            return TritValue(1 if self.value < other.value else 0)
        return TritValue(1 if self.value < other else 0)
    
    def __le__(self, other):
        if isinstance(other, TritValue):
            return TritValue(1 if self.value <= other.value else 0)
        return TritValue(1 if self.value <= other else 0)
    
    def __gt__(self, other):
        if isinstance(other, TritValue):
            return TritValue(1 if self.value > other.value else 0)
        return TritValue(1 if self.value > other else 0)
    
    def __ge__(self, other):
        if isinstance(other, TritValue):
            return TritValue(1 if self.value >= other.value else 0)
        return TritValue(1 if self.value >= other else 0)
    
    def is_truthy(self) -> bool:
        """Check if value is truthy (non-zero, non-empty)."""
        if isinstance(self.value, bool):
            return self.value
        if isinstance(self.value, (int, float)):
            return self.value != 0
        if isinstance(self.value, str):
            return len(self.value) > 0
        if isinstance(self.value, (list, tuple)):
            return len(self.value) > 0
        return self.value is not None


class TritVector:
    """
    Vector data structure for ML operations.
    Supports element-wise operations and balanced ternary arithmetic.
    """
    
    def __init__(self, elements: List[Union[TritValue, Any]]):
        self.elements = [TritValue(e) if not isinstance(e, TritValue) else e for e in elements]
    
    def __getitem__(self, index: int) -> TritValue:
        if index < 0 or index >= len(self.elements):
            raise IndexError(f"Vector index {index} out of range")
        return self.elements[index]
    
    def __setitem__(self, index: int, value: TritValue):
        if index < 0 or index >= len(self.elements):
            raise IndexError(f"Vector index {index} out of range")
        self.elements[index] = TritValue(value.value) if isinstance(value, TritValue) else TritValue(value)
    
    def __len__(self) -> int:
        return len(self.elements)
    
    def __repr__(self):
        return f"TritVector({[e.value for e in self.elements]})"
    
    def __str__(self):
        return "[" + ", ".join(str(e.value) for e in self.elements) + "]"
    
    def __add__(self, other):
        """Element-wise addition."""
        if isinstance(other, TritVector):
            if len(self) != len(other):
                raise ValueError("Vectors must have same length for addition")
            return TritVector([self[i] + other[i] for i in range(len(self))])
        # Scalar addition
        return TritVector([e + other for e in self.elements])
    
    def __sub__(self, other):
        """Element-wise subtraction."""
        if isinstance(other, TritVector):
            if len(self) != len(other):
                raise ValueError("Vectors must have same length for subtraction")
            return TritVector([self[i] - other[i] for i in range(len(self))])
        # Scalar subtraction
        return TritVector([e - other for e in self.elements])
    
    def __mul__(self, other):
        """Element-wise multiplication or dot product."""
        if isinstance(other, TritVector):
            if len(self) != len(other):
                raise ValueError("Vectors must have same length for multiplication")
            # Dot product
            result = TritValue(0)
            for i in range(len(self)):
                result = result + (self[i] * other[i])
            return result
        # Scalar multiplication
        return TritVector([e * other for e in self.elements])
    
    def dot(self, other: 'TritVector') -> TritValue:
        """Dot product of two vectors."""
        return self * other
    
    def sum(self) -> TritValue:
        """Sum of all elements."""
        result = TritValue(0)
        for e in self.elements:
            result = result + e
        return result
    
    def mean(self) -> TritValue:
        """Mean of all elements."""
        if len(self) == 0:
            return TritValue(0)
        return self.sum() / TritValue(len(self))


class TritMatrix:
    """
    Matrix data structure for ML operations.
    Supports matrix operations and balanced ternary arithmetic.
    """
    
    def __init__(self, rows: List[List[Union[TritValue, Any]]]):
        if not rows:
            raise ValueError("Matrix must have at least one row")
        row_len = len(rows[0])
        for row in rows:
            if len(row) != row_len:
                raise ValueError("All rows must have the same length")
        
        self.rows = [[TritValue(e) if not isinstance(e, TritValue) else e for e in row] for row in rows]
        self.height = len(rows)
        self.width = row_len
    
    def __getitem__(self, index: tuple) -> TritValue:
        row, col = index
        if row < 0 or row >= self.height or col < 0 or col >= self.width:
            raise IndexError(f"Matrix index ({row}, {col}) out of range")
        return self.rows[row][col]
    
    def __setitem__(self, index: tuple, value: TritValue):
        row, col = index
        if row < 0 or row >= self.height or col < 0 or col >= self.width:
            raise IndexError(f"Matrix index ({row}, {col}) out of range")
        self.rows[row][col] = TritValue(value.value) if isinstance(value, TritValue) else TritValue(value)
    
    def __repr__(self):
        return f"TritMatrix({self.rows})"
    
    def __str__(self):
        return "[\n  " + ",\n  ".join("[" + ", ".join(str(e.value) for e in row) + "]" for row in self.rows) + "\n]"
    
    def __add__(self, other):
        """Element-wise addition."""
        if isinstance(other, TritMatrix):
            if self.height != other.height or self.width != other.width:
                raise ValueError("Matrices must have same dimensions for addition")
            return TritMatrix([[self[(i, j)] + other[(i, j)] for j in range(self.width)] for i in range(self.height)])
        # Scalar addition
        return TritMatrix([[e + other for e in row] for row in self.rows])
    
    def __mul__(self, other):
        """Matrix multiplication or scalar multiplication."""
        if isinstance(other, TritMatrix):
            if self.width != other.height:
                raise ValueError(f"Cannot multiply {self.height}x{self.width} matrix by {other.height}x{other.width} matrix")
            
            result_rows = []
            for i in range(self.height):
                row = []
                for j in range(other.width):
                    sum_val = TritValue(0)
                    for k in range(self.width):
                        sum_val = sum_val + (self[(i, k)] * other[(k, j)])
                    row.append(sum_val)
                result_rows.append(row)
            
            return TritMatrix(result_rows)
        
        # Scalar multiplication
        return TritMatrix([[e * other for e in row] for row in self.rows])
    
    def transpose(self) -> 'TritMatrix':
        """Transpose the matrix."""
        return TritMatrix([[self[(j, i)] for j in range(self.height)] for i in range(self.width)])
