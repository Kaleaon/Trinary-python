"""
TritLang - A simple programming language designed for LLMs and Machine Learning
using balanced ternary (+1, 0, -1) arithmetic.

TritLang is designed to be:
- Easy to program and understand
- LLM-friendly with clear, intuitive syntax
- Optimized for ML operations with built-in vector/matrix support
- Based on balanced ternary number system
"""

from .lexer import Lexer
from .parser import Parser
from .interpreter import Interpreter
from .runtime import TritValue, TritVector, TritMatrix

__version__ = "0.1.0"
__all__ = [
    "Lexer",
    "Parser", 
    "Interpreter",
    "TritValue",
    "TritVector",
    "TritMatrix",
]
