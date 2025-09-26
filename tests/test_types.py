"""
Tests for trinary data types.
"""

import pytest
from trinary.types import TrinaryInt, TrinaryFloat, TrinaryBool


class TestTrinaryInt:
    """Test cases for TrinaryInt class."""
    
    def test_integer_operations(self):
        """Test integer-specific operations."""
        a = TrinaryInt(10)
        b = TrinaryInt(3)
        
        # Floor division
        assert (a // b).decimal_value == 3
        
        # Modulo
        assert (a % b).decimal_value == 1
        
        # Power
        assert (b ** 2).decimal_value == 9
    
    def test_trit_shifting(self):
        """Test trit shifting operations."""
        a = TrinaryInt(5)  # "12" in trinary
        
        # Left shift (multiply by 3^n)
        left_shifted = a.trit_shift_left(1)
        assert left_shifted.decimal_value == 15  # 5 * 3
        
        left_shifted_2 = a.trit_shift_left(2)
        assert left_shifted_2.decimal_value == 45  # 5 * 9
        
        # Right shift (divide by 3^n)
        b = TrinaryInt(15)
        right_shifted = b.trit_shift_right(1)
        assert right_shifted.decimal_value == 5  # 15 // 3
    
    def test_trit_counting(self):
        """Test counting trits in representation."""
        assert TrinaryInt(0).count_trits() == 1
        assert TrinaryInt(1).count_trits() == 1
        assert TrinaryInt(3).count_trits() == 2  # "10"
        assert TrinaryInt(9).count_trits() == 3  # "100"
        assert TrinaryInt(-5).count_trits() == 2  # Sign + "12"
    
    def test_balanced_ternary_conversion(self):
        """Test conversion to balanced ternary."""
        a = TrinaryInt(5)
        bt = a.to_balanced_ternary()
        assert bt.decimal_value == 5


class TestTrinaryFloat:
    """Test cases for TrinaryFloat class."""
    
    def test_float_initialization(self):
        """Test initialization of trinary floats."""
        # From decimal
        tf = TrinaryFloat(3.5, precision=6)
        assert abs(tf.decimal_value - 3.5) < 0.01
        
        # From string
        tf2 = TrinaryFloat("10.12")  # 3 + 1/3 + 2/9 = 3.555...
        expected = 3 + 1/3 + 2/9
        assert abs(tf2.decimal_value - expected) < 0.001
    
    def test_float_operations(self):
        """Test floating point operations."""
        a = TrinaryFloat(2.5)
        b = TrinaryFloat(1.5)
        
        # Addition
        result = a + b
        assert abs(result.decimal_value - 4.0) < 0.01
        
        # Subtraction
        result = a - b
        assert abs(result.decimal_value - 1.0) < 0.01
        
        # Multiplication
        result = a * b
        assert abs(result.decimal_value - 3.75) < 0.01
        
        # Division
        result = a / b
        assert abs(result.decimal_value - (5/3)) < 0.01
    
    def test_properties(self):
        """Test float properties."""
        tf = TrinaryFloat("12.21")  # 5 + 2/3 + 1/9 = 5.777...
        
        assert tf.integer_part.decimal_value == 5
        assert len(tf.fractional_trits) > 0
    
    def test_precision_handling(self):
        """Test precision handling in conversions."""
        # Test with different precisions
        tf1 = TrinaryFloat(1.0/3.0, precision=3)
        tf2 = TrinaryFloat(1.0/3.0, precision=6)
        
        # Higher precision should be more accurate
        assert abs(tf2.decimal_value - 1.0/3.0) <= abs(tf1.decimal_value - 1.0/3.0)


class TestTrinaryBool:
    """Test cases for TrinaryBool class."""
    
    def test_initialization(self):
        """Test different ways to initialize TrinaryBool."""
        # From bool
        assert TrinaryBool(True).is_true
        assert TrinaryBool(False).is_false
        
        # From int
        assert TrinaryBool(1).is_true
        assert TrinaryBool(0).is_false
        assert TrinaryBool(-1).is_maybe
        
        # From string
        assert TrinaryBool("true").is_true
        assert TrinaryBool("false").is_false
        assert TrinaryBool("maybe").is_maybe
        
        # From None
        assert TrinaryBool(None).is_maybe
    
    def test_logical_operations(self):
        """Test three-state logical operations."""
        true_val = TrinaryBool(True)
        false_val = TrinaryBool(False)
        maybe_val = TrinaryBool(None)
        
        # AND operations
        assert (true_val & true_val).is_true
        assert (true_val & false_val).is_false
        assert (true_val & maybe_val).is_maybe
        assert (false_val & false_val).is_false
        assert (false_val & maybe_val).is_false
        assert (maybe_val & maybe_val).is_maybe
        
        # OR operations
        assert (true_val | true_val).is_true
        assert (true_val | false_val).is_true
        assert (true_val | maybe_val).is_true
        assert (false_val | false_val).is_false
        assert (false_val | maybe_val).is_maybe
        assert (maybe_val | maybe_val).is_maybe
        
        # NOT operations
        assert (~true_val).is_false
        assert (~false_val).is_true
        assert (~maybe_val).is_maybe
    
    def test_equality_comparison(self):
        """Test equality comparison returning TrinaryBool."""
        true_val = TrinaryBool(True)
        false_val = TrinaryBool(False)
        maybe_val = TrinaryBool(None)
        
        # Equal values
        assert (true_val == TrinaryBool(True)).is_true
        assert (false_val == TrinaryBool(False)).is_true
        
        # Different values
        assert (true_val == false_val).is_false
        
        # Maybe comparisons
        assert (true_val == maybe_val).is_maybe
        assert (maybe_val == maybe_val).is_maybe
    
    def test_python_bool_conversion(self):
        """Test conversion to Python bool."""
        assert bool(TrinaryBool(True)) is True
        assert bool(TrinaryBool(False)) is False
        assert bool(TrinaryBool(None)) is False  # Maybe becomes False for safety
    
    def test_string_representations(self):
        """Test string representations."""
        assert str(TrinaryBool(True)) == "True"
        assert str(TrinaryBool(False)) == "False"
        assert str(TrinaryBool(None)) == "Maybe"
        
        assert repr(TrinaryBool(True)) == "TrinaryBool(True)"
        assert repr(TrinaryBool(False)) == "TrinaryBool(False)"
        assert repr(TrinaryBool(None)) == "TrinaryBool(Maybe)"


if __name__ == "__main__":
    pytest.main([__file__])