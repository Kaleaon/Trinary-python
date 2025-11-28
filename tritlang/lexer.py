"""
Lexer (tokenizer) for TritLang programming language.

Tokenizes source code into a stream of tokens for parsing.
"""

from enum import Enum
from typing import List, Optional


class TokenType(Enum):
    # Literals
    NUMBER = "NUMBER"  # Balanced ternary number: +, 0, -, or decimal
    STRING = "STRING"
    IDENTIFIER = "IDENTIFIER"
    
    # Operators
    PLUS = "PLUS"  # +
    MINUS = "MINUS"  # -
    MULTIPLY = "MULTIPLY"  # *
    DIVIDE = "DIVIDE"  # /
    MODULO = "MODULO"  # %
    POWER = "POWER"  # **
    EQUAL = "EQUAL"  # ==
    NOT_EQUAL = "NOT_EQUAL"  # !=
    LESS = "LESS"  # <
    LESS_EQUAL = "LESS_EQUAL"  # <=
    GREATER = "GREATER"  # >
    GREATER_EQUAL = "GREATER_EQUAL"  # >=
    AND = "AND"  # and
    OR = "OR"  # or
    NOT = "NOT"  # not
    
    # Assignment
    ASSIGN = "ASSIGN"  # =
    PLUS_ASSIGN = "PLUS_ASSIGN"  # +=
    MINUS_ASSIGN = "MINUS_ASSIGN"  # -=
    
    # Delimiters
    LPAREN = "LPAREN"  # (
    RPAREN = "RPAREN"  # )
    LBRACKET = "LBRACKET"  # [
    RBRACKET = "RBRACKET"  # ]
    LBRACE = "LBRACE"  # {
    RBRACE = "RBRACE"  # }
    COMMA = "COMMA"  # ,
    DOT = "DOT"  # .
    COLON = "COLON"  # :
    SEMICOLON = "SEMICOLON"  # ;
    
    # Keywords
    LET = "LET"
    VAR = "VAR"
    IF = "IF"
    ELIF = "ELIF"
    ELSE = "ELSE"
    WHILE = "WHILE"
    FOR = "FOR"
    IN = "IN"
    FUNCTION = "FUNCTION"
    RETURN = "RETURN"
    TRUE = "TRUE"
    FALSE = "FALSE"
    MAYBE = "MAYBE"  # Three-state logic
    PRINT = "PRINT"
    LEN = "LEN"
    
    # Special
    NEWLINE = "NEWLINE"
    EOF = "EOF"


class Token:
    """Represents a single token in the source code."""
    
    def __init__(self, type: TokenType, value: any, line: int, column: int):
        self.type = type
        self.value = value
        self.line = line
        self.column = column
    
    def __repr__(self):
        return f"Token({self.type.name}, {repr(self.value)}, {self.line}:{self.column})"


class Lexer:
    """Tokenizes TritLang source code."""
    
    KEYWORDS = {
        "let": TokenType.LET,
        "var": TokenType.VAR,
        "if": TokenType.IF,
        "elif": TokenType.ELIF,
        "else": TokenType.ELSE,
        "while": TokenType.WHILE,
        "for": TokenType.FOR,
        "in": TokenType.IN,
        "function": TokenType.FUNCTION,
        "fn": TokenType.FUNCTION,  # Alias
        "return": TokenType.RETURN,
        "true": TokenType.TRUE,
        "false": TokenType.FALSE,
        "maybe": TokenType.MAYBE,
        "print": TokenType.PRINT,
        "len": TokenType.LEN,
        "and": TokenType.AND,
        "or": TokenType.OR,
        "not": TokenType.NOT,
    }
    
    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []
    
    def current_char(self) -> Optional[str]:
        """Get the current character, or None if at EOF."""
        if self.pos >= len(self.source):
            return None
        return self.source[self.pos]
    
    def peek_char(self, offset: int = 1) -> Optional[str]:
        """Peek ahead by offset characters."""
        pos = self.pos + offset
        if pos >= len(self.source):
            return None
        return self.source[pos]
    
    def advance(self) -> Optional[str]:
        """Move to next character and return it."""
        if self.pos >= len(self.source):
            return None
        
        char = self.source[self.pos]
        self.pos += 1
        
        if char == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        
        return char
    
    def skip_whitespace(self):
        """Skip whitespace characters."""
        while self.current_char() and self.current_char() in ' \t\r':
            self.advance()
    
    def skip_comment(self):
        """Skip single-line comments (//) and multi-line comments (/* */)."""
        if self.current_char() == '/' and self.peek_char() == '/':
            # Single-line comment
            while self.current_char() and self.current_char() != '\n':
                self.advance()
        elif self.current_char() == '/' and self.peek_char() == '*':
            # Multi-line comment
            self.advance()  # Skip /
            self.advance()  # Skip *
            while self.current_char():
                if self.current_char() == '*' and self.peek_char() == '/':
                    self.advance()  # Skip *
                    self.advance()  # Skip /
                    break
                self.advance()
    
    def read_number(self) -> Token:
        """Read a number (decimal or balanced ternary)."""
        start_line = self.line
        start_col = self.column
        
        # Check for balanced ternary notation: +, 0, -, or T for -1
        if self.current_char() in '+-T':
            # Balanced ternary literal
            value = ""
            while self.current_char() and self.current_char() in '+-T01':
                char = self.current_char()
                if char == 'T':
                    value += '-'
                else:
                    value += char
                self.advance()
            
            # Convert balanced ternary to decimal for storage
            decimal = self._balanced_ternary_to_decimal(value)
            return Token(TokenType.NUMBER, decimal, start_line, start_col)
        
        # Decimal number
        num_str = ""
        while self.current_char() and (self.current_char().isdigit() or self.current_char() == '.'):
            num_str += self.advance()
        
        if '.' in num_str:
            return Token(TokenType.NUMBER, float(num_str), start_line, start_col)
        else:
            return Token(TokenType.NUMBER, int(num_str), start_line, start_col)
    
    def _balanced_ternary_to_decimal(self, bt_str: str) -> int:
        """Convert balanced ternary string to decimal."""
        decimal = 0
        for i, char in enumerate(reversed(bt_str)):
            if char == '+':
                trit = 1
            elif char == '0':
                trit = 0
            elif char == '-':
                trit = -1
            else:
                raise ValueError(f"Invalid balanced ternary character: {char}")
            decimal += trit * (3 ** i)
        return decimal
    
    def read_string(self) -> Token:
        """Read a string literal."""
        start_line = self.line
        start_col = self.column
        
        quote = self.advance()  # Skip opening quote
        value = ""
        
        while self.current_char() and self.current_char() != quote:
            if self.current_char() == '\\':
                self.advance()  # Skip backslash
                char = self.current_char()
                if char == 'n':
                    value += '\n'
                elif char == 't':
                    value += '\t'
                elif char == '\\':
                    value += '\\'
                elif char == quote:
                    value += quote
                else:
                    value += '\\' + char
                self.advance()
            else:
                value += self.advance()
        
        if self.current_char() == quote:
            self.advance()  # Skip closing quote
        else:
            raise SyntaxError(f"Unterminated string at {start_line}:{start_col}")
        
        return Token(TokenType.STRING, value, start_line, start_col)
    
    def read_identifier(self) -> Token:
        """Read an identifier or keyword."""
        start_line = self.line
        start_col = self.column
        
        value = ""
        while self.current_char() and (self.current_char().isalnum() or self.current_char() == '_'):
            value += self.advance()
        
        # Check if it's a keyword
        token_type = self.KEYWORDS.get(value.lower(), TokenType.IDENTIFIER)
        return Token(token_type, value, start_line, start_col)
    
    def tokenize(self) -> List[Token]:
        """Tokenize the entire source code."""
        self.tokens = []
        
        while self.current_char() is not None:
            # Skip whitespace
            if self.current_char() in ' \t\r':
                self.skip_whitespace()
                continue
            
            # Skip comments
            if self.current_char() == '/' and self.peek_char() in ['/', '*']:
                self.skip_comment()
                continue
            
            # Newline
            if self.current_char() == '\n':
                self.tokens.append(Token(TokenType.NEWLINE, '\n', self.line, self.column))
                self.advance()
                continue
            
            # Numbers - check for balanced ternary or decimal
            if self.current_char().isdigit():
                self.tokens.append(self.read_number())
                continue
            
            # Balanced ternary numbers (must start with +, -, or T and be followed by balanced ternary digits)
            if self.current_char() in '+-T' and self.peek_char() and self.peek_char() in '+-T01':
                # Check if previous token allows a number here
                can_be_number = (self.pos == 0 or not self.tokens or 
                                self.tokens[-1].type in [TokenType.PLUS, TokenType.MINUS, TokenType.MULTIPLY, 
                                                         TokenType.DIVIDE, TokenType.ASSIGN, TokenType.LPAREN, 
                                                         TokenType.LBRACKET, TokenType.COMMA, TokenType.NEWLINE, 
                                                         TokenType.SEMICOLON, TokenType.EQUAL, TokenType.LESS, 
                                                         TokenType.GREATER, TokenType.LESS_EQUAL, TokenType.GREATER_EQUAL])
                if can_be_number:
                    self.tokens.append(self.read_number())
                    continue
            
            # Decimal numbers starting with .
            if self.current_char() == '.' and self.peek_char() and self.peek_char().isdigit():
                self.tokens.append(self.read_number())
                continue
            
            # Strings
            if self.current_char() in '"\'':
                self.tokens.append(self.read_string())
                continue
            
            # Identifiers and keywords
            if self.current_char().isalpha() or self.current_char() == '_':
                self.tokens.append(self.read_identifier())
                continue
            
            # Operators and punctuation
            char = self.current_char()
            start_line = self.line
            start_col = self.column
            
            # Two-character operators
            if char == '=' and self.peek_char() == '=':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.EQUAL, "==", start_line, start_col))
                continue
            
            if char == '!' and self.peek_char() == '=':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.NOT_EQUAL, "!=", start_line, start_col))
                continue
            
            if char == '<' and self.peek_char() == '=':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.LESS_EQUAL, "<=", start_line, start_col))
                continue
            
            if char == '>' and self.peek_char() == '=':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.GREATER_EQUAL, ">=", start_line, start_col))
                continue
            
            if char == '+' and self.peek_char() == '=':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.PLUS_ASSIGN, "+=", start_line, start_col))
                continue
            
            if char == '-' and self.peek_char() == '=':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.MINUS_ASSIGN, "-=", start_line, start_col))
                continue
            
            if char == '*' and self.peek_char() == '*':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.POWER, "**", start_line, start_col))
                continue
            
            # Single-character operators
            operators = {
                '+': TokenType.PLUS,
                '-': TokenType.MINUS,
                '*': TokenType.MULTIPLY,
                '/': TokenType.DIVIDE,
                '%': TokenType.MODULO,
                '<': TokenType.LESS,
                '>': TokenType.GREATER,
                '=': TokenType.ASSIGN,
                '(': TokenType.LPAREN,
                ')': TokenType.RPAREN,
                '[': TokenType.LBRACKET,
                ']': TokenType.RBRACKET,
                '{': TokenType.LBRACE,
                '}': TokenType.RBRACE,
                ',': TokenType.COMMA,
                '.': TokenType.DOT,
                ':': TokenType.COLON,
                ';': TokenType.SEMICOLON,
            }
            
            if char in operators:
                self.advance()
                self.tokens.append(Token(operators[char], char, start_line, start_col))
                continue
            
            # Unknown character
            raise SyntaxError(f"Unexpected character '{char}' at {self.line}:{self.column}")
        
        # Add EOF token
        self.tokens.append(Token(TokenType.EOF, None, self.line, self.column))
        return self.tokens
