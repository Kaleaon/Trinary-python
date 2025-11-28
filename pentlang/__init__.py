"""
PentLang - A programming language for PNPU (Pentary Neural Processing Unit)
using balanced quinary (-2, -1, 0, +1, +2) arithmetic.

PentLang is designed to be:
- Easy to program and understand
- LLM-friendly with clear, intuitive syntax
- Optimized for PNPU hardware with shift-add operations
- Based on balanced quinary number system
"""

from .lexer import Lexer
from .parser import Parser
from .interpreter import Interpreter
from .runtime import PentValue, PentVector, PentMatrix, PNPUCore

__version__ = "0.1.0"
__all__ = [
    "Lexer",
    "Parser",
    "Interpreter",
    "PentValue",
    "PentVector",
    "PentMatrix",
    "PNPUCore",
]
