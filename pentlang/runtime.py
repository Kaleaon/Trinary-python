"""
Runtime values and data structures for PentLang.

Handles balanced quinary arithmetic and ML-friendly data structures optimized for PNPU.
"""

from typing import List, Any, Union
from pentary.core import BalancedQuinary
from pentary.operations import PentaryOperations
from pentary.pnpu import PNPUCore, ShiftAddMAC


class PentValue:
    """
    Runtime value wrapper that can hold any PentLang value.
    Supports balanced quinary arithmetic optimized for PNPU.
    """
    
    def __init__(self, value: Any):
        self.value = value
    
    def to_balanced_quinary(self) -> BalancedQuinary:
        """Convert numeric value to balanced quinary."""
        if isinstance(self.value, (int, float)):
            return BalancedQuinary(int(self.value))
        return BalancedQuinary(0)
    
    def __repr__(self):
        return f"PentValue({repr(self.value)})"
    
    def __str__(self):
        return str(self.value)
    
    def __add__(self, other):
        if isinstance(other, PentValue):
            return PentValue(self.value + other.value)
        return PentValue(self.value + other)
    
    def __sub__(self, other):
        if isinstance(other, PentValue):
            return PentValue(self.value - other.value)
        return PentValue(self.value - other)
    
    def __mul__(self, other):
        if isinstance(other, PentValue):
            return PentValue(self.value * other.value)
        return PentValue(self.value * other)
    
    def __truediv__(self, other):
        if isinstance(other, PentValue):
            if other.value == 0:
                raise ZeroDivisionError("Division by zero")
            return PentValue(self.value / other.value)
        if other == 0:
            raise ZeroDivisionError("Division by zero")
        return PentValue(self.value / other)
    
    def __mod__(self, other):
        if isinstance(other, PentValue):
            if other.value == 0:
                raise ZeroDivisionError("Modulo by zero")
            return PentValue(self.value % other.value)
        if other == 0:
            raise ZeroDivisionError("Modulo by zero")
        return PentValue(self.value % other)
    
    def __pow__(self, other):
        if isinstance(other, PentValue):
            return PentValue(self.value ** other.value)
        return PentValue(self.value ** other)
    
    def __eq__(self, other):
        if isinstance(other, PentValue):
            return PentValue(1 if self.value == other.value else 0)
        return PentValue(1 if self.value == other else 0)
    
    def __ne__(self, other):
        if isinstance(other, PentValue):
            return PentValue(1 if self.value != other.value else 0)
        return PentValue(1 if self.value != other else 0)
    
    def __lt__(self, other):
        if isinstance(other, PentValue):
            return PentValue(1 if self.value < other.value else 0)
        return PentValue(1 if self.value < other else 0)
    
    def __le__(self, other):
        if isinstance(other, PentValue):
            return PentValue(1 if self.value <= other.value else 0)
        return PentValue(1 if self.value <= other else 0)
    
    def __gt__(self, other):
        if isinstance(other, PentValue):
            return PentValue(1 if self.value > other.value else 0)
        return PentValue(1 if self.value > other else 0)
    
    def __ge__(self, other):
        if isinstance(other, PentValue):
            return PentValue(1 if self.value >= other.value else 0)
        return PentValue(1 if self.value >= other else 0)
    
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


class PentVector:
    """
    Vector data structure for ML operations optimized for PNPU.
    Supports element-wise operations and balanced quinary arithmetic.
    """
    
    def __init__(self, elements: List[Union[PentValue, Any]]):
        self.elements = [PentValue(e) if not isinstance(e, PentValue) else e for e in elements]
    
    def __getitem__(self, index: int) -> PentValue:
        if index < 0 or index >= len(self.elements):
            raise IndexError(f"Vector index {index} out of range")
        return self.elements[index]
    
    def __setitem__(self, index: int, value: PentValue):
        if index < 0 or index >= len(self.elements):
            raise IndexError(f"Vector index {index} out of range")
        self.elements[index] = PentValue(value.value) if isinstance(value, PentValue) else PentValue(value)
    
    def __len__(self) -> int:
        return len(self.elements)
    
    def __repr__(self):
        return f"PentVector({[e.value for e in self.elements]})"
    
    def __str__(self):
        return "[" + ", ".join(str(e.value) for e in self.elements) + "]"
    
    def __add__(self, other):
        """Element-wise addition."""
        if isinstance(other, PentVector):
            if len(self) != len(other):
                raise ValueError("Vectors must have same length for addition")
            return PentVector([self[i] + other[i] for i in range(len(self))])
        # Scalar addition
        return PentVector([e + other for e in self.elements])
    
    def __sub__(self, other):
        """Element-wise subtraction."""
        if isinstance(other, PentVector):
            if len(self) != len(other):
                raise ValueError("Vectors must have same length for subtraction")
            return PentVector([self[i] - other[i] for i in range(len(self))])
        # Scalar subtraction
        return PentVector([e - other for e in self.elements])
    
    def __mul__(self, other):
        """Element-wise multiplication or dot product."""
        if isinstance(other, PentVector):
            if len(self) != len(other):
                raise ValueError("Vectors must have same length for multiplication")
            # Dot product
            result = PentValue(0)
            for i in range(len(self)):
                result = result + (self[i] * other[i])
            return result
        # Scalar multiplication
        return PentVector([e * other for e in self.elements])
    
    def dot(self, other: 'PentVector') -> PentValue:
        """Dot product of two vectors."""
        return self * other
    
    def sum(self) -> PentValue:
        """Sum of all elements."""
        result = PentValue(0)
        for e in self.elements:
            result = result + e
        return result
    
    def mean(self) -> PentValue:
        """Mean of all elements."""
        if len(self) == 0:
            return PentValue(0)
        return self.sum() / PentValue(len(self))
    
    def mac(self, weights: 'PentVector', accumulator: PentValue = None) -> PentValue:
        """
        Multiply-Accumulate operation using PNPU shift-add logic.
        
        Args:
            weights: Weight vector (values must be -2, -1, 0, 1, or 2)
            accumulator: Initial accumulator value (default: 0)
        
        Returns:
            Accumulated result
        """
        if len(self) != len(weights):
            raise ValueError("Activation and weight vectors must have same length")
        
        if accumulator is None:
            acc = PentValue(0)
        else:
            acc = accumulator
        
        for activation, weight in zip(self.elements, weights.elements):
            acc = PentValue(PentaryOperations.shift_add_mac(
                int(activation.value), int(weight.value), int(acc.value)
            ))
        
        return acc


class PentMatrix:
    """
    Matrix data structure for ML operations optimized for PNPU.
    Supports matrix operations and balanced quinary arithmetic.
    """
    
    def __init__(self, rows: List[List[Union[PentValue, Any]]]):
        if not rows:
            raise ValueError("Matrix must have at least one row")
        row_len = len(rows[0])
        for row in rows:
            if len(row) != row_len:
                raise ValueError("All rows must have the same length")
        
        self.rows = [[PentValue(e) if not isinstance(e, PentValue) else e for e in row] for row in rows]
        self.height = len(rows)
        self.width = row_len
    
    def __getitem__(self, index: tuple) -> PentValue:
        row, col = index
        if row < 0 or row >= self.height or col < 0 or col >= self.width:
            raise IndexError(f"Matrix index ({row}, {col}) out of range")
        return self.rows[row][col]
    
    def __setitem__(self, index: tuple, value: PentValue):
        row, col = index
        if row < 0 or row >= self.height or col < 0 or col >= self.width:
            raise IndexError(f"Matrix index ({row}, {col}) out of range")
        self.rows[row][col] = PentValue(value.value) if isinstance(value, PentValue) else PentValue(value)
    
    def __repr__(self):
        return f"PentMatrix({self.rows})"
    
    def __str__(self):
        return "[\n  " + ",\n  ".join("[" + ", ".join(str(e.value) for e in row) + "]" for row in self.rows) + "\n]"
    
    def __add__(self, other):
        """Element-wise addition."""
        if isinstance(other, PentMatrix):
            if self.height != other.height or self.width != other.width:
                raise ValueError("Matrices must have same dimensions for addition")
            return PentMatrix([[self[(i, j)] + other[(i, j)] for j in range(self.width)] for i in range(self.height)])
        # Scalar addition
        return PentMatrix([[e + other for e in row] for row in self.rows])
    
    def __mul__(self, other):
        """Matrix multiplication or scalar multiplication."""
        if isinstance(other, PentMatrix):
            if self.width != other.height:
                raise ValueError(f"Cannot multiply {self.height}x{self.width} matrix by {other.height}x{other.width} matrix")
            
            result_rows = []
            for i in range(self.height):
                row = []
                for j in range(other.width):
                    sum_val = PentValue(0)
                    for k in range(self.width):
                        sum_val = sum_val + (self[(i, k)] * other[(k, j)])
                    row.append(sum_val)
                result_rows.append(row)
            
            return PentMatrix(result_rows)
        
        # Scalar multiplication
        return PentMatrix([[e * other for e in row] for row in self.rows])
    
    def transpose(self) -> 'PentMatrix':
        """Transpose the matrix."""
        return PentMatrix([[self[(j, i)] for j in range(self.height)] for i in range(self.width)])
    
    def matrix_vector_multiply(self, vector: PentVector) -> PentVector:
        """
        Matrix-vector multiplication using PNPU shift-add MAC operations.
        
        Args:
            vector: Input vector (length must match matrix width)
        
        Returns:
            Output vector
        """
        if len(vector) != self.width:
            raise ValueError(f"Vector length {len(vector)} must match matrix width {self.width}")
        
        outputs = []
        for i in range(self.height):
            row_vector = PentVector([self.rows[i][j] for j in range(self.width)])
            result = row_vector.mac(vector, PentValue(0))
            outputs.append(result)
        
        return PentVector(outputs)
