"""
Lexer (tokenizer) for PentLang programming language.

Tokenizes source code into a stream of tokens for parsing.
Supports balanced quinary numbers: +2, +1, 0, -1, -2
"""

from enum import Enum
from typing import List, Optional


class TokenType(Enum):
    # Literals
    NUMBER = "NUMBER"  # Balanced quinary number: +2, +1, 0, -1, -2, or decimal
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
    ABSOLUTE_YES = "ABSOLUTE_YES"  # +2
    MAYBE_YES = "MAYBE_YES"  # +1
    UNKNOWN = "UNKNOWN"  # 0
    MAYBE_NO = "MAYBE_NO"  # -1
    ABSOLUTE_NO = "ABSOLUTE_NO"  # -2
    PRINT = "PRINT"
    LEN = "LEN"
    SHIFT_LEFT = "SHIFT_LEFT"  # PNPU operation
    SHIFT_RIGHT = "SHIFT_RIGHT"  # PNPU operation
    MAC = "MAC"  # Multiply-Accumulate
    
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
    """Tokenizes PentLang source code."""
    
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
        "fn": TokenType.FUNCTION,
        "return": TokenType.RETURN,
        "absolute_yes": TokenType.ABSOLUTE_YES,
        "maybe_yes": TokenType.MAYBE_YES,
        "unknown": TokenType.UNKNOWN,
        "maybe_no": TokenType.MAYBE_NO,
        "absolute_no": TokenType.ABSOLUTE_NO,
        "print": TokenType.PRINT,
        "len": TokenType.LEN,
        "and": TokenType.AND,
        "or": TokenType.OR,
        "not": TokenType.NOT,
        "shift_left": TokenType.SHIFT_LEFT,
        "shift_right": TokenType.SHIFT_RIGHT,
        "mac": TokenType.MAC,
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
            while self.current_char() and self.current_char() != '\n':
                self.advance()
        elif self.current_char() == '/' and self.peek_char() == '*':
            self.advance()
            self.advance()
            while self.current_char():
                if self.current_char() == '*' and self.peek_char() == '/':
                    self.advance()
                    self.advance()
                    break
                self.advance()
    
    def read_number(self) -> Token:
        """Read a number (decimal or balanced quinary)."""
        start_line = self.line
        start_col = self.column
        
        # Check for balanced quinary notation: +2, +1, 0, -1, -2
        if self.current_char() in '+-' and self.peek_char() and self.peek_char().isdigit():
            # Balanced quinary literal starting with + or -
            value = ""
            char = self.advance()  # Skip + or -
            if char == '+':
                if self.current_char() in '12':
                    value = '+' + self.advance()
                else:
                    value = '+1'  # Default to +1
            elif char == '-':
                if self.current_char() in '12':
                    value = '-' + self.advance()
                else:
                    value = '-1'  # Default to -1
            
            # Continue reading if more balanced quinary digits
            while self.current_char() and self.current_char() in '+-012':
                char = self.current_char()
                if char == '+':
                    self.advance()
                    if self.current_char() in '12':
                        value += '+' + self.advance()
                    else:
                        value += '+1'
                elif char == '-':
                    self.advance()
                    if self.current_char() in '12':
                        value += '-' + self.advance()
                    else:
                        value += '-1'
                elif char in '012':
                    value += self.advance()
                else:
                    break
            
            # Convert balanced quinary to decimal
            decimal = self._balanced_quinary_to_decimal(value)
            return Token(TokenType.NUMBER, decimal, start_line, start_col)
        
        # Decimal number
        num_str = ""
        while self.current_char() and (self.current_char().isdigit() or self.current_char() == '.'):
            num_str += self.advance()
        
        if '.' in num_str:
            return Token(TokenType.NUMBER, float(num_str), start_line, start_col)
        else:
            return Token(TokenType.NUMBER, int(num_str), start_line, start_col)
    
    def _balanced_quinary_to_decimal(self, bq_str: str) -> int:
        """Convert balanced quinary string to decimal."""
        decimal = 0
        i = 0
        position = 0
        
        # Parse from right to left (least significant first)
        pentits = []
        while i < len(bq_str):
            if bq_str[i] == '+':
                if i + 1 < len(bq_str):
                    if bq_str[i + 1] == '2':
                        pentits.append(2)
                        i += 2
                    elif bq_str[i + 1] == '1':
                        pentits.append(1)
                        i += 2
                    else:
                        pentits.append(1)
                        i += 1
                else:
                    pentits.append(1)
                    i += 1
            elif bq_str[i] == '-':
                if i + 1 < len(bq_str):
                    if bq_str[i + 1] == '2':
                        pentits.append(-2)
                        i += 2
                    elif bq_str[i + 1] == '1':
                        pentits.append(-1)
                        i += 2
                    else:
                        pentits.append(-1)
                        i += 1
                else:
                    pentits.append(-1)
                    i += 1
            elif bq_str[i] == '0':
                pentits.append(0)
                i += 1
            elif bq_str[i] in '12':
                pentits.append(int(bq_str[i]))
                i += 1
            else:
                i += 1
        
        # Convert to decimal
        for j, pentit in enumerate(reversed(pentits)):
            decimal += pentit * (5 ** j)
        
        return decimal
    
    def read_string(self) -> Token:
        """Read a string literal."""
        start_line = self.line
        start_col = self.column
        
        quote = self.advance()
        value = ""
        
        while self.current_char() and self.current_char() != quote:
            if self.current_char() == '\\':
                self.advance()
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
            self.advance()
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
        
        token_type = self.KEYWORDS.get(value.lower(), TokenType.IDENTIFIER)
        return Token(token_type, value, start_line, start_col)
    
    def tokenize(self) -> List[Token]:
        """Tokenize the entire source code."""
        self.tokens = []
        
        while self.current_char() is not None:
            if self.current_char() in ' \t\r':
                self.skip_whitespace()
                continue
            
            if self.current_char() == '/' and self.peek_char() in ['/', '*']:
                self.skip_comment()
                continue
            
            if self.current_char() == '\n':
                self.tokens.append(Token(TokenType.NEWLINE, '\n', self.line, self.column))
                self.advance()
                continue
            
            # Numbers
            if self.current_char().isdigit():
                self.tokens.append(self.read_number())
                continue
            
            # Balanced quinary numbers starting with + or -
            if self.current_char() in '+-' and self.peek_char() and self.peek_char().isdigit():
                can_be_number = (self.pos == 0 or not self.tokens or
                                self.tokens[-1].type in [TokenType.PLUS, TokenType.MINUS, TokenType.MULTIPLY,
                                                         TokenType.DIVIDE, TokenType.ASSIGN, TokenType.LPAREN,
                                                         TokenType.LBRACKET, TokenType.COMMA, TokenType.NEWLINE,
                                                         TokenType.SEMICOLON, TokenType.EQUAL, TokenType.LESS,
                                                         TokenType.GREATER, TokenType.LESS_EQUAL, TokenType.GREATER_EQUAL])
                if can_be_number:
                    self.tokens.append(self.read_number())
                    continue
            
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
            
            raise SyntaxError(f"Unexpected character '{char}' at {self.line}:{self.column}")
        
        self.tokens.append(Token(TokenType.EOF, None, self.line, self.column))
        return self.tokens
