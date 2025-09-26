"""
Tests for the core trinary number system.
"""

import pytest
from trinary.core import TrinaryNumber, BalancedTernary


class TestTrinaryNumber:
    """Test cases for TrinaryNumber class."""
    
    def test_decimal_to_trinary_conversion(self):
        """Test conversion from decimal to trinary."""
        # Test basic conversions
        assert str(TrinaryNumber(0)) == "0"
        assert str(TrinaryNumber(1)) == "1"
        assert str(TrinaryNumber(2)) == "2"
        assert str(TrinaryNumber(3)) == "10"
        assert str(TrinaryNumber(4)) == "11"
        assert str(TrinaryNumber(5)) == "12"
        assert str(TrinaryNumber(9)) == "100"
        assert str(TrinaryNumber(27)) == "1000"
    
    def test_negative_numbers(self):
        """Test negative number handling."""
        assert str(TrinaryNumber(-1)) == "-1"
        assert str(TrinaryNumber(-5)) == "-12"
        assert str(TrinaryNumber(-9)) == "-100"
    
    def test_string_parsing(self):
        """Test parsing trinary strings."""
        assert TrinaryNumber("102").decimal_value == 11  # 1*9 + 0*3 + 2*1
        assert TrinaryNumber("210").decimal_value == 21  # 2*9 + 1*3 + 0*1
        assert TrinaryNumber("-12").decimal_value == -5
    
    def test_list_initialization(self):
        """Test initialization from trit lists."""
        trits = [1, 0, 2]  # 102 in trinary = 11 in decimal
        tn = TrinaryNumber(trits)
        assert tn.decimal_value == 11
        assert tn.trits == [1, 0, 2]
    
    def test_arithmetic_operations(self):
        """Test basic arithmetic operations."""
        a = TrinaryNumber(5)  # "12"
        b = TrinaryNumber(3)  # "10"
        
        # Addition
        result = a + b
        assert result.decimal_value == 8
        assert str(result) == "22"
        
        # Subtraction
        result = a - b
        assert result.decimal_value == 2
        assert str(result) == "2"
        
        # Multiplication
        result = a * b
        assert result.decimal_value == 15
        assert str(result) == "120"
    
    def test_comparison_operations(self):
        """Test comparison operations."""
        a = TrinaryNumber(5)
        b = TrinaryNumber(3)
        c = TrinaryNumber(5)
        
        assert a == c
        assert a != b
        assert a > b
        assert b < a
        assert a == 5
        assert b == 3
    
    def test_properties(self):
        """Test number properties."""
        positive = TrinaryNumber(5)
        negative = TrinaryNumber(-5)
        zero = TrinaryNumber(0)
        
        assert not positive.is_negative
        assert negative.is_negative
        assert not zero.is_negative
        
        assert positive.decimal_value == 5
        assert negative.decimal_value == -5
        assert zero.decimal_value == 0


class TestBalancedTernary:
    """Test cases for BalancedTernary class."""
    
    def test_decimal_to_balanced_conversion(self):
        """Test conversion from decimal to balanced ternary."""
        # Test basic conversions
        assert str(BalancedTernary(0)) == "0"
        assert str(BalancedTernary(1)) == "1"
        assert str(BalancedTernary(2)) == "1T"  # 1*3 + (-1)*1 = 2
        assert str(BalancedTernary(3)) == "10"
        assert str(BalancedTernary(4)) == "11"
        assert str(BalancedTernary(5)) == "1TT"  # 1*9 + (-1)*3 + (-1)*1 = 5
    
    def test_negative_numbers_balanced(self):
        """Test negative numbers in balanced ternary."""
        assert str(BalancedTernary(-1)) == "T"
        assert str(BalancedTernary(-2)) == "T1"  # -1*3 + 1*1 = -2
        assert str(BalancedTernary(-3)) == "T0"  # -1*3 + 0*1 = -3
        assert str(BalancedTernary(-4)) == "TT"  # -1*3 + (-1)*1 = -4
    
    def test_string_parsing_balanced(self):
        """Test parsing balanced ternary strings."""
        assert BalancedTernary("1T").decimal_value == 2  # 1*3 + (-1)*1
        assert BalancedTernary("T1").decimal_value == -2  # (-1)*3 + 1*1
        assert BalancedTernary("10T").decimal_value == 8  # 1*9 + 0*3 + (-1)*1
    
    def test_symmetry(self):
        """Test the symmetry property of balanced ternary."""
        for i in range(-10, 11):
            bt = BalancedTernary(i)
            assert bt.decimal_value == i
            
            # Test that negation works symmetrically
            neg_bt = BalancedTernary(-i)
            assert neg_bt.decimal_value == -i
    
    def test_list_initialization_balanced(self):
        """Test initialization from balanced trit lists."""
        trits = [1, -1, 0]  # 1T0 = 1*9 + (-1)*3 + 0*1 = 6
        bt = BalancedTernary(trits)
        assert bt.decimal_value == 6
        assert bt.trits == [1, -1, 0]


if __name__ == "__main__":
    pytest.main([__file__])