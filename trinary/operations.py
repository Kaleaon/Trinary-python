"""
Advanced trinary operations and algorithms.

This module provides specialized trinary operations including:
- Trinary arithmetic with carry/borrow logic
- Bitwise operations adapted for trinary (trits)
- Advanced mathematical functions in trinary base
"""

from typing import List, Union, Tuple
from .core import TrinaryNumber, BalancedTernary
from .types import TrinaryInt, TrinaryBool


class TrinaryOperations:
    """
    Collection of advanced trinary operations and algorithms.
    
    Provides low-level trinary arithmetic and bitwise operations
    that work directly with trit representations.
    """
    
    @staticmethod
    def add_trits(a_trits: List[int], b_trits: List[int]) -> List[int]:
        """
        Add two trinary numbers at the trit level with proper carry logic.
        
        Args:
            a_trits: First number's trits (least significant first)
            b_trits: Second number's trits (least significant first)
        
        Returns:
            Result trits with carry propagation
        """
        # Ensure both lists are the same length
        max_len = max(len(a_trits), len(b_trits))
        a_trits = a_trits + [0] * (max_len - len(a_trits))
        b_trits = b_trits + [0] * (max_len - len(b_trits))
        
        result = []
        carry = 0
        
        for i in range(max_len):
            total = a_trits[i] + b_trits[i] + carry
            
            if total >= 3:
                carry = total // 3
                digit = total % 3
            else:
                carry = 0
                digit = total
            
            result.append(digit)
        
        # Handle final carry
        while carry > 0:
            if carry >= 3:
                result.append(carry % 3)
                carry = carry // 3
            else:
                result.append(carry)
                carry = 0
        
        return result
    
    @staticmethod
    def subtract_trits(a_trits: List[int], b_trits: List[int]) -> Tuple[List[int], bool]:
        """
        Subtract two trinary numbers at the trit level with borrow logic.
        
        Args:
            a_trits: Minuend trits (least significant first)
            b_trits: Subtrahend trits (least significant first)
        
        Returns:
            Tuple of (result trits, is_negative)
        """
        # Ensure both lists are the same length
        max_len = max(len(a_trits), len(b_trits))
        a_trits = a_trits + [0] * (max_len - len(a_trits))
        b_trits = b_trits + [0] * (max_len - len(b_trits))
        
        result = []
        borrow = 0
        
        for i in range(max_len):
            diff = a_trits[i] - b_trits[i] - borrow
            
            if diff < 0:
                borrow = (-diff + 2) // 3  # Calculate borrow needed
                digit = diff + borrow * 3
            else:
                borrow = 0
                digit = diff
            
            result.append(digit)
        
        # Check if final result is negative
        is_negative = borrow > 0
        
        return result, is_negative
    
    @staticmethod
    def multiply_trits(a_trits: List[int], b_trits: List[int]) -> List[int]:
        """
        Multiply two trinary numbers using elementary multiplication.
        
        Args:
            a_trits: First multiplicand (least significant first)
            b_trits: Second multiplicand (least significant first)
        
        Returns:
            Product trits
        """
        if not a_trits or not b_trits:
            return [0]
        
        result = [0] * (len(a_trits) + len(b_trits))
        
        for i in range(len(a_trits)):
            for j in range(len(b_trits)):
                product = a_trits[i] * b_trits[j]
                position = i + j
                
                # Add product to result with carry propagation
                result[position] += product
                
                # Handle carries
                k = position
                while k < len(result) and result[k] >= 3:
                    carry = result[k] // 3
                    result[k] = result[k] % 3
                    if k + 1 < len(result):
                        result[k + 1] += carry
                    else:
                        result.append(carry)
                    k += 1
        
        # Remove leading zeros but keep at least one digit
        while len(result) > 1 and result[-1] == 0:
            result.pop()
        
        return result
    
    @staticmethod
    def trit_and(a: int, b: int) -> int:
        """
        Trinary AND operation on individual trits.
        
        Truth table:
        0 AND 0 = 0, 0 AND 1 = 0, 0 AND 2 = 0
        1 AND 0 = 0, 1 AND 1 = 1, 1 AND 2 = 1  
        2 AND 0 = 0, 2 AND 1 = 1, 2 AND 2 = 2
        """
        return min(a, b)
    
    @staticmethod
    def trit_or(a: int, b: int) -> int:
        """
        Trinary OR operation on individual trits.
        
        Truth table:
        0 OR 0 = 0, 0 OR 1 = 1, 0 OR 2 = 2
        1 OR 0 = 1, 1 OR 1 = 1, 1 OR 2 = 2
        2 OR 0 = 2, 2 OR 1 = 2, 2 OR 2 = 2
        """
        return max(a, b)
    
    @staticmethod
    def trit_not(a: int) -> int:
        """
        Trinary NOT operation on individual trit.
        
        Truth table:
        NOT 0 = 2
        NOT 1 = 1 (stays the same)
        NOT 2 = 0
        """
        if a == 0:
            return 2
        elif a == 1:
            return 1
        elif a == 2:
            return 0
        else:
            raise ValueError(f"Invalid trit value: {a}")
    
    @staticmethod
    def trit_xor(a: int, b: int) -> int:
        """
        Trinary XOR operation on individual trits.
        
        Returns the "distance" between trits in modular arithmetic.
        """
        return (a + b) % 3
    
    @staticmethod
    def bitwise_and(a: TrinaryInt, b: TrinaryInt) -> TrinaryInt:
        """Bitwise AND operation on TrinaryInt objects."""
        a_trits = list(reversed(a.trits))
        b_trits = list(reversed(b.trits))
        
        max_len = max(len(a_trits), len(b_trits))
        a_trits.extend([0] * (max_len - len(a_trits)))
        b_trits.extend([0] * (max_len - len(b_trits)))
        
        result_trits = []
        for i in range(max_len):
            result_trits.append(TrinaryOperations.trit_and(a_trits[i], b_trits[i]))
        
        result_trits.reverse()
        return TrinaryInt(result_trits)
    
    @staticmethod
    def bitwise_or(a: TrinaryInt, b: TrinaryInt) -> TrinaryInt:
        """Bitwise OR operation on TrinaryInt objects."""
        a_trits = list(reversed(a.trits))
        b_trits = list(reversed(b.trits))
        
        max_len = max(len(a_trits), len(b_trits))
        a_trits.extend([0] * (max_len - len(a_trits)))
        b_trits.extend([0] * (max_len - len(b_trits)))
        
        result_trits = []
        for i in range(max_len):
            result_trits.append(TrinaryOperations.trit_or(a_trits[i], b_trits[i]))
        
        result_trits.reverse()
        return TrinaryInt(result_trits)
    
    @staticmethod
    def bitwise_not(a: TrinaryInt) -> TrinaryInt:
        """Bitwise NOT operation on TrinaryInt object."""
        a_trits = a.trits[:]
        
        result_trits = []
        for trit in a_trits:
            if trit == -1:  # Handle negative sign
                result_trits.append(trit)
            else:
                result_trits.append(TrinaryOperations.trit_not(trit))
        
        return TrinaryInt(result_trits)
    
    @staticmethod
    def rotate_left(a: TrinaryInt, positions: int, width: int = None) -> TrinaryInt:
        """
        Rotate trits to the left.
        
        Args:
            a: TrinaryInt to rotate
            positions: Number of positions to rotate
            width: Fixed width for rotation (default: actual width)
        """
        trits = a.trits[:]
        if a.is_negative:
            trits = trits[1:]  # Remove sign bit for rotation
        
        if width is None:
            width = len(trits)
        else:
            # Pad or truncate to specified width
            if len(trits) < width:
                trits = [0] * (width - len(trits)) + trits
            else:
                trits = trits[-width:]
        
        positions = positions % width  # Handle over-rotation
        rotated = trits[positions:] + trits[:positions]
        
        if a.is_negative:
            rotated.insert(0, -1)  # Restore sign bit
        
        return TrinaryInt(rotated)
    
    @staticmethod
    def rotate_right(a: TrinaryInt, positions: int, width: int = None) -> TrinaryInt:
        """
        Rotate trits to the right.
        
        Args:
            a: TrinaryInt to rotate
            positions: Number of positions to rotate
            width: Fixed width for rotation (default: actual width)
        """
        trits = a.trits[:]
        if a.is_negative:
            trits = trits[1:]  # Remove sign bit for rotation
        
        if width is None:
            width = len(trits)
        else:
            # Pad or truncate to specified width
            if len(trits) < width:
                trits = [0] * (width - len(trits)) + trits
            else:
                trits = trits[-width:]
        
        positions = positions % width  # Handle over-rotation
        rotated = trits[-positions:] + trits[:-positions]
        
        if a.is_negative:
            rotated.insert(0, -1)  # Restore sign bit
        
        return TrinaryInt(rotated)
    
    @staticmethod
    def greatest_trit_divisor(a: TrinaryInt, b: TrinaryInt) -> TrinaryInt:
        """
        Find the greatest common divisor using Euclidean algorithm.
        
        Args:
            a: First TrinaryInt
            b: Second TrinaryInt
        
        Returns:
            Greatest common divisor as TrinaryInt
        """
        a_val = abs(a.decimal_value)
        b_val = abs(b.decimal_value)
        
        while b_val != 0:
            a_val, b_val = b_val, a_val % b_val
        
        return TrinaryInt(a_val)
    
    @staticmethod
    def to_balanced_ternary_ops(trinary_int: TrinaryInt) -> BalancedTernary:
        """
        Convert TrinaryInt to BalancedTernary with optimized algorithm.
        
        Args:
            trinary_int: TrinaryInt to convert
        
        Returns:
            Equivalent BalancedTernary representation
        """
        return BalancedTernary(trinary_int.decimal_value)