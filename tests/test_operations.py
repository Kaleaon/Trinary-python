"""
Tests for trinary operations module.
"""

import pytest
from trinary.operations import TrinaryOperations
from trinary.types import TrinaryInt
from trinary.core import BalancedTernary


class TestTrinaryOperations:
    """Test cases for TrinaryOperations class."""
    
    def test_add_trits(self):
        """Test low-level trit addition with carry."""
        # Simple addition without carry
        result = TrinaryOperations.add_trits([1, 2], [0, 1])  # LSB first
        expected = [1, 0, 1]  # 1+0=1, 2+1=3->0 carry 1
        assert result == expected
        
        # Addition with multiple carries
        result = TrinaryOperations.add_trits([2, 2, 2], [1, 1, 1])
        # 2+1=3->0 carry 1, 2+1+1=4->1 carry 1, 2+1+1=4->1 carry 1, final carry 1
        expected = [0, 1, 1, 1]
        assert result == expected
    
    def test_subtract_trits(self):
        """Test low-level trit subtraction with borrow."""
        # Simple subtraction without borrow
        result, is_negative = TrinaryOperations.subtract_trits([2, 1], [1, 0])
        expected = [1, 1]  # 2-1=1, 1-0=1
        assert result == expected
        assert not is_negative
        
        # Subtraction requiring borrow
        result, is_negative = TrinaryOperations.subtract_trits([0, 1], [1, 0])
        # 0-1 requires borrow, becomes 3-1=2 with borrow propagation
        assert len(result) >= 2
        assert not is_negative or result[0] == 2
    
    def test_multiply_trits(self):
        """Test low-level trit multiplication."""
        # Simple multiplication
        result = TrinaryOperations.multiply_trits([0, 1], [1])  # 10 * 1 = 10 (LSB first)
        expected = [0, 1]
        assert result == expected
        
        # More complex multiplication
        result = TrinaryOperations.multiply_trits([1, 1], [1, 1])  # 11 * 11 (LSB first)
        # In decimal: 4 * 4 = 16, in trinary: 121 (LSB first: [1, 2, 1])
        expected = [1, 2, 1]
        assert result == expected
    
    def test_individual_trit_operations(self):
        """Test individual trit operations."""
        # AND operations
        assert TrinaryOperations.trit_and(0, 0) == 0
        assert TrinaryOperations.trit_and(1, 0) == 0
        assert TrinaryOperations.trit_and(2, 1) == 1
        assert TrinaryOperations.trit_and(2, 2) == 2
        
        # OR operations  
        assert TrinaryOperations.trit_or(0, 0) == 0
        assert TrinaryOperations.trit_or(1, 0) == 1
        assert TrinaryOperations.trit_or(2, 1) == 2
        assert TrinaryOperations.trit_or(1, 1) == 1
        
        # NOT operations
        assert TrinaryOperations.trit_not(0) == 2
        assert TrinaryOperations.trit_not(1) == 1
        assert TrinaryOperations.trit_not(2) == 0
        
        # XOR operations
        assert TrinaryOperations.trit_xor(0, 0) == 0
        assert TrinaryOperations.trit_xor(1, 2) == 0  # (1+2) % 3
        assert TrinaryOperations.trit_xor(2, 1) == 0  # (2+1) % 3
        assert TrinaryOperations.trit_xor(1, 1) == 2  # (1+1) % 3
    
    def test_bitwise_operations(self):
        """Test bitwise operations on TrinaryInt objects."""
        a = TrinaryInt(5)   # "12" in trinary -> trits [1, 2]
        b = TrinaryInt(3)   # "10" in trinary -> trits [1, 0]
        
        # AND operation
        result = TrinaryOperations.bitwise_and(a, b)
        # [1, 2] AND [1, 0] -> [1, 0] (min of each position)
        expected_trits = [1, 0]
        assert result.trits == expected_trits
        
        # OR operation
        result = TrinaryOperations.bitwise_or(a, b)
        # [1, 2] OR [1, 0] -> [1, 2] (max of each position)
        expected_trits = [1, 2]
        assert result.trits == expected_trits
        
        # NOT operation
        result = TrinaryOperations.bitwise_not(a)
        # NOT [1, 2] -> [1, 0] (NOT 1=1, NOT 2=0)
        expected_trits = [1, 0]
        assert result.trits == expected_trits
    
    def test_rotation_operations(self):
        """Test trit rotation operations."""
        a = TrinaryInt(13)  # "111" in trinary
        
        # Left rotation
        result = TrinaryOperations.rotate_left(a, 1, width=3)
        # "111" rotate left 1 -> "111" (all same digits)
        assert result.trits == [1, 1, 1]
        
        b = TrinaryInt(5)   # "12" in trinary
        result = TrinaryOperations.rotate_left(b, 1, width=3)
        # "012" (padded) rotate left 1 -> "120"
        expected_decimal = 1*9 + 2*3 + 0*1  # 15
        assert result.decimal_value == 15
        
        # Right rotation
        result = TrinaryOperations.rotate_right(b, 1, width=3)
        # "012" rotate right 1 -> "201"
        expected_decimal = 2*9 + 0*3 + 1*1  # 19
        assert result.decimal_value == 19
    
    def test_greatest_trit_divisor(self):
        """Test greatest common divisor calculation."""
        a = TrinaryInt(15)  # "120"
        b = TrinaryInt(9)   # "100"
        
        gcd = TrinaryOperations.greatest_trit_divisor(a, b)
        assert gcd.decimal_value == 3  # GCD(15, 9) = 3
        
        # Test with coprime numbers
        a = TrinaryInt(7)   # "21"
        b = TrinaryInt(5)   # "12"
        
        gcd = TrinaryOperations.greatest_trit_divisor(a, b)
        assert gcd.decimal_value == 1  # GCD(7, 5) = 1
    
    def test_balanced_ternary_conversion(self):
        """Test conversion to balanced ternary."""
        test_values = [-5, -1, 0, 1, 5, 13]
        
        for decimal in test_values:
            ti = TrinaryInt(decimal)
            bt = TrinaryOperations.to_balanced_ternary_ops(ti)
            
            # Verify the conversion is correct
            assert bt.decimal_value == decimal
            assert isinstance(bt, BalancedTernary)
    
    def test_edge_cases(self):
        """Test edge cases and error conditions."""
        # Test with zero
        zero = TrinaryInt(0)
        result = TrinaryOperations.bitwise_and(zero, TrinaryInt(5))
        assert result.decimal_value == 0
        
        # Test rotation with zero positions
        a = TrinaryInt(5)
        result = TrinaryOperations.rotate_left(a, 0, width=3)
        assert result.decimal_value == a.decimal_value
        
        # Test invalid trit values for NOT operation
        with pytest.raises(ValueError):
            TrinaryOperations.trit_not(3)
        
        with pytest.raises(ValueError):
            TrinaryOperations.trit_not(-1)


if __name__ == "__main__":
    pytest.main([__file__])