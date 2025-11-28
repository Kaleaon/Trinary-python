"""
Advanced pentary operations and algorithms optimized for PNPU architecture.

This module provides specialized pentary operations including:
- Shift-add MAC operations (no multipliers)
- Pentary arithmetic with carry/borrow logic
- Operations optimized for neural network inference
"""

from typing import List, Union, Tuple
from .core import PentaryNumber, BalancedQuinary
from .types import PentaryInt, PentaryBool


class PentaryOperations:
    """
    Collection of advanced pentary operations optimized for PNPU.
    
    Provides shift-add operations that eliminate the need for multipliers,
    matching the hardware design of the Pentary Neural Processing Unit.
    """
    
    @staticmethod
    def shift_add_mac(activation: int, weight: int, accumulator: int = 0) -> int:
        """
        Shift-Add Multiply-Accumulate operation (PNPU core operation).
        
        This implements the "No-Multiplier" core logic:
        - If weight is 0: output 0
        - If weight is ±1: pass input through
        - If weight is ±2: shift input left (multiply by 2)
        - Check sign and invert if negative
        - Accumulate into register
        
        Args:
            activation: Input activation value
            weight: Weight value (-2, -1, 0, 1, or 2)
            accumulator: Current accumulator value
        
        Returns:
            New accumulator value after MAC operation
        """
        if weight == 0:
            product = 0
        elif weight == 1:
            product = activation
        elif weight == 2:
            product = activation << 1  # Shift left (multiply by 2)
        elif weight == -1:
            product = -activation
        elif weight == -2:
            product = -(activation << 1)  # Shift left and negate
        else:
            raise ValueError(f"Invalid weight value: {weight}. Must be -2, -1, 0, 1, or 2")
        
        return accumulator + product
    
    @staticmethod
    def add_pentits(a_pentits: List[int], b_pentits: List[int]) -> List[int]:
        """
        Add two pentary numbers at the pentit level with proper carry logic.
        
        Args:
            a_pentits: First number's pentits (least significant first)
            b_pentits: Second number's pentits (least significant first)
        
        Returns:
            Result pentits with carry propagation
        """
        max_len = max(len(a_pentits), len(b_pentits))
        a_pentits = list(reversed(a_pentits)) + [0] * (max_len - len(a_pentits))
        b_pentits = list(reversed(b_pentits)) + [0] * (max_len - len(b_pentits))
        
        result = []
        carry = 0
        
        for i in range(max_len):
            total = a_pentits[i] + b_pentits[i] + carry
            
            # Handle carry in base 5
            if total > 2:
                # Positive carry
                carry = (total + 2) // 5
                digit = total - carry * 5
            elif total < -2:
                # Negative carry
                carry = (total - 2) // 5
                digit = total - carry * 5
            else:
                carry = 0
                digit = total
            
            result.append(digit)
        
        # Handle final carry
        while carry != 0:
            if carry > 2:
                result.append(carry % 5)
                carry = carry // 5
            elif carry < -2:
                result.append(carry % 5)
                carry = (carry + 2) // 5
            else:
                result.append(carry)
                carry = 0
        
        result.reverse()
        return result
    
    @staticmethod
    def pentit_shift_left(value: PentaryInt, positions: int) -> PentaryInt:
        """
        Shift pentits left (multiply by 5^positions).
        
        This is a fundamental PNPU operation - shifting is much cheaper
        than multiplication in hardware.
        """
        return value.pentit_shift_left(positions)
    
    @staticmethod
    def pentit_shift_right(value: PentaryInt, positions: int) -> PentaryInt:
        """
        Shift pentits right (divide by 5^positions).
        """
        return value.pentit_shift_right(positions)
    
    @staticmethod
    def pentit_and(a: int, b: int) -> int:
        """
        Pentary AND operation on individual pentits.
        
        Returns the minimum value (most negative if both negative).
        """
        return min(a, b) if (a >= 0 and b >= 0) or (a < 0 and b < 0) else 0
    
    @staticmethod
    def pentit_or(a: int, b: int) -> int:
        """
        Pentary OR operation on individual pentits.
        
        Returns the maximum value (most positive if both positive).
        """
        return max(a, b) if (a >= 0 and b >= 0) or (a < 0 and b < 0) else 0
    
    @staticmethod
    def to_balanced_quinary_ops(pentary_int: PentaryInt) -> BalancedQuinary:
        """
        Convert PentaryInt to BalancedQuinary with optimized algorithm.
        """
        return BalancedQuinary(pentary_int.decimal_value)
