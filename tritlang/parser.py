"""
Parser for TritLang programming language.

Parses tokens into an Abstract Syntax Tree (AST).
"""

from typing import List, Optional, Any
from .lexer import Token, TokenType


class ASTNode:
    """Base class for all AST nodes."""
    pass


class Program(ASTNode):
    """Root node representing the entire program."""
    def __init__(self, statements: List[ASTNode]):
        self.statements = statements


class NumberLiteral(ASTNode):
    """Number literal node."""
    def __init__(self, value: Any):
        self.value = value


class StringLiteral(ASTNode):
    """String literal node."""
    def __init__(self, value: str):
        self.value = value


class BooleanLiteral(ASTNode):
    """Boolean literal node (True, False, Maybe)."""
    def __init__(self, value: Any):  # 1, 0, or -1
        self.value = value


class Identifier(ASTNode):
    """Identifier/variable name node."""
    def __init__(self, name: str):
        self.name = name


class BinaryOp(ASTNode):
    """Binary operation node."""
    def __init__(self, left: ASTNode, op: TokenType, right: ASTNode):
        self.left = left
        self.op = op
        self.right = right


class UnaryOp(ASTNode):
    """Unary operation node."""
    def __init__(self, op: TokenType, operand: ASTNode):
        self.op = op
        self.operand = operand


class Assignment(ASTNode):
    """Variable assignment node."""
    def __init__(self, name: str, value: ASTNode, op: TokenType = TokenType.ASSIGN):
        self.name = name
        self.value = value
        self.op = op


class VariableDeclaration(ASTNode):
    """Variable declaration node (let/var)."""
    def __init__(self, name: str, value: Optional[ASTNode], mutable: bool = False):
        self.name = name
        self.value = value
        self.mutable = mutable  # var is mutable, let is immutable


class IfStatement(ASTNode):
    """If-elif-else statement node."""
    def __init__(self, condition: ASTNode, then_branch: List[ASTNode], 
                 elif_branches: List[tuple] = None, else_branch: List[ASTNode] = None):
        self.condition = condition
        self.then_branch = then_branch
        self.elif_branches = elif_branches or []
        self.else_branch = else_branch or []


class WhileStatement(ASTNode):
    """While loop node."""
    def __init__(self, condition: ASTNode, body: List[ASTNode]):
        self.condition = condition
        self.body = body


class ForStatement(ASTNode):
    """For loop node."""
    def __init__(self, var_name: str, iterable: ASTNode, body: List[ASTNode]):
        self.var_name = var_name
        self.iterable = iterable
        self.body = body


class FunctionCall(ASTNode):
    """Function call node."""
    def __init__(self, name: ASTNode, args: List[ASTNode]):
        self.name = name
        self.args = args


class FunctionDef(ASTNode):
    """Function definition node."""
    def __init__(self, name: str, params: List[str], body: List[ASTNode]):
        self.name = name
        self.params = params
        self.body = body


class ReturnStatement(ASTNode):
    """Return statement node."""
    def __init__(self, value: Optional[ASTNode]):
        self.value = value


class VectorLiteral(ASTNode):
    """Vector literal node [a, b, c, ...]."""
    def __init__(self, elements: List[ASTNode]):
        self.elements = elements


class IndexAccess(ASTNode):
    """Index access node (array/vector access)."""
    def __init__(self, obj: ASTNode, index: ASTNode):
        self.obj = obj
        self.index = index


class MemberAccess(ASTNode):
    """Member access node (object.property)."""
    def __init__(self, obj: ASTNode, member: str):
        self.obj = obj
        self.member = member


class Parser:
    """Parses tokens into an AST."""
    
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0
    
    def current_token(self) -> Optional[Token]:
        """Get the current token."""
        if self.pos >= len(self.tokens):
            return None
        return self.tokens[self.pos]
    
    def peek_token(self, offset: int = 1) -> Optional[Token]:
        """Peek ahead at a token."""
        pos = self.pos + offset
        if pos >= len(self.tokens):
            return None
        return self.tokens[pos]
    
    def advance(self) -> Optional[Token]:
        """Move to the next token."""
        if self.pos < len(self.tokens):
            token = self.tokens[self.pos]
            self.pos += 1
            return token
        return None
    
    def expect(self, token_type: TokenType, error_msg: str = None) -> Token:
        """Expect a specific token type, raise error if not found."""
        token = self.current_token()
        if token and token.type == token_type:
            return self.advance()
        error = error_msg or f"Expected {token_type.name}, got {token.type.name if token else 'EOF'}"
        raise SyntaxError(f"{error} at {token.line}:{token.column if token else '?'}")
    
    def skip_newlines(self):
        """Skip newline tokens."""
        while self.current_token() and self.current_token().type == TokenType.NEWLINE:
            self.advance()
    
    def parse(self) -> Program:
        """Parse the entire program."""
        statements = []
        
        while self.current_token() and self.current_token().type != TokenType.EOF:
            self.skip_newlines()
            if self.current_token() and self.current_token().type != TokenType.EOF:
                stmt = self.parse_statement()
                if stmt:
                    statements.append(stmt)
        
        return Program(statements)
    
    def parse_statement(self) -> ASTNode:
        """Parse a single statement."""
        token = self.current_token()
        if not token:
            return None
        
        # Variable declaration
        if token.type in [TokenType.LET, TokenType.VAR]:
            return self.parse_variable_declaration()
        
        # Function definition
        if token.type == TokenType.FUNCTION:
            return self.parse_function_def()
        
        # Return statement
        if token.type == TokenType.RETURN:
            return self.parse_return()
        
        # Control flow
        if token.type == TokenType.IF:
            return self.parse_if()
        if token.type == TokenType.WHILE:
            return self.parse_while()
        if token.type == TokenType.FOR:
            return self.parse_for()
        
        # Expression statement (including function calls like print())
        expr = self.parse_expression()
        
        # Skip newline or semicolon if present
        if self.current_token() and self.current_token().type in [TokenType.NEWLINE, TokenType.SEMICOLON]:
            self.advance()
        
        return expr
    
    def parse_variable_declaration(self) -> VariableDeclaration:
        """Parse variable declaration (let/var)."""
        token = self.current_token()
        mutable = token.type == TokenType.VAR
        self.advance()  # Skip let/var
        
        name_token = self.expect(TokenType.IDENTIFIER, "Expected variable name")
        name = name_token.value
        
        value = None
        if self.current_token() and self.current_token().type == TokenType.ASSIGN:
            self.advance()  # Skip =
            value = self.parse_expression()
        
        return VariableDeclaration(name, value, mutable)
    
    def parse_function_def(self) -> FunctionDef:
        """Parse function definition."""
        self.advance()  # Skip function/fn
        
        name_token = self.expect(TokenType.IDENTIFIER, "Expected function name")
        name = name_token.value
        
        self.expect(TokenType.LPAREN, "Expected (")
        
        params = []
        if self.current_token() and self.current_token().type != TokenType.RPAREN:
            while True:
                param_token = self.expect(TokenType.IDENTIFIER, "Expected parameter name")
                params.append(param_token.value)
                
                if self.current_token() and self.current_token().type == TokenType.COMMA:
                    self.advance()
                else:
                    break
        
        self.expect(TokenType.RPAREN, "Expected )")
        self.expect(TokenType.LBRACE, "Expected {")
        
        body = []
        while self.current_token() and self.current_token().type != TokenType.RBRACE:
            self.skip_newlines()
            if self.current_token() and self.current_token().type != TokenType.RBRACE:
                body.append(self.parse_statement())
        
        self.expect(TokenType.RBRACE, "Expected }")
        
        return FunctionDef(name, params, body)
    
    def parse_return(self) -> ReturnStatement:
        """Parse return statement."""
        self.advance()  # Skip return
        
        value = None
        if self.current_token() and self.current_token().type != TokenType.NEWLINE:
            value = self.parse_expression()
        
        return ReturnStatement(value)
    
    def parse_if(self) -> IfStatement:
        """Parse if-elif-else statement."""
        self.advance()  # Skip if
        
        condition = self.parse_expression()
        self.expect(TokenType.LBRACE, "Expected {")
        
        then_branch = []
        while self.current_token() and self.current_token().type != TokenType.RBRACE:
            self.skip_newlines()
            if self.current_token() and self.current_token().type != TokenType.RBRACE:
                then_branch.append(self.parse_statement())
        
        self.expect(TokenType.RBRACE, "Expected }")
        
        elif_branches = []
        else_branch = []
        
        while self.current_token() and self.current_token().type == TokenType.ELIF:
            self.advance()  # Skip elif
            elif_condition = self.parse_expression()
            self.expect(TokenType.LBRACE, "Expected {")
            
            elif_body = []
            while self.current_token() and self.current_token().type != TokenType.RBRACE:
                self.skip_newlines()
                if self.current_token() and self.current_token().type != TokenType.RBRACE:
                    elif_body.append(self.parse_statement())
            
            self.expect(TokenType.RBRACE, "Expected }")
            elif_branches.append((elif_condition, elif_body))
        
        if self.current_token() and self.current_token().type == TokenType.ELSE:
            self.advance()  # Skip else
            self.expect(TokenType.LBRACE, "Expected {")
            
            while self.current_token() and self.current_token().type != TokenType.RBRACE:
                self.skip_newlines()
                if self.current_token() and self.current_token().type != TokenType.RBRACE:
                    else_branch.append(self.parse_statement())
            
            self.expect(TokenType.RBRACE, "Expected }")
        
        return IfStatement(condition, then_branch, elif_branches, else_branch)
    
    def parse_while(self) -> WhileStatement:
        """Parse while loop."""
        self.advance()  # Skip while
        
        condition = self.parse_expression()
        self.expect(TokenType.LBRACE, "Expected {")
        
        body = []
        while self.current_token() and self.current_token().type != TokenType.RBRACE:
            self.skip_newlines()
            if self.current_token() and self.current_token().type != TokenType.RBRACE:
                body.append(self.parse_statement())
        
        self.expect(TokenType.RBRACE, "Expected }")
        
        return WhileStatement(condition, body)
    
    def parse_for(self) -> ForStatement:
        """Parse for loop."""
        self.advance()  # Skip for
        
        var_token = self.expect(TokenType.IDENTIFIER, "Expected variable name")
        var_name = var_token.value
        
        self.expect(TokenType.IN, "Expected 'in'")
        
        iterable = self.parse_expression()
        self.expect(TokenType.LBRACE, "Expected {")
        
        body = []
        while self.current_token() and self.current_token().type != TokenType.RBRACE:
            self.skip_newlines()
            if self.current_token() and self.current_token().type != TokenType.RBRACE:
                body.append(self.parse_statement())
        
        self.expect(TokenType.RBRACE, "Expected }")
        
        return ForStatement(var_name, iterable, body)
    
    def parse_expression(self) -> ASTNode:
        """Parse an expression."""
        return self.parse_assignment()
    
    def parse_assignment(self) -> ASTNode:
        """Parse assignment expression."""
        left = self.parse_or()
        
        if self.current_token() and self.current_token().type in [TokenType.ASSIGN, TokenType.PLUS_ASSIGN, TokenType.MINUS_ASSIGN]:
            op = self.current_token().type
            self.advance()
            
            if not isinstance(left, Identifier):
                raise SyntaxError("Left side of assignment must be an identifier")
            
            right = self.parse_assignment()
            return Assignment(left.name, right, op)
        
        return left
    
    def parse_or(self) -> ASTNode:
        """Parse OR expression."""
        left = self.parse_and()
        
        while self.current_token() and self.current_token().type == TokenType.OR:
            op = self.current_token().type
            self.advance()
            right = self.parse_and()
            left = BinaryOp(left, op, right)
        
        return left
    
    def parse_and(self) -> ASTNode:
        """Parse AND expression."""
        left = self.parse_comparison()
        
        while self.current_token() and self.current_token().type == TokenType.AND:
            op = self.current_token().type
            self.advance()
            right = self.parse_comparison()
            left = BinaryOp(left, op, right)
        
        return left
    
    def parse_comparison(self) -> ASTNode:
        """Parse comparison expression."""
        left = self.parse_additive()
        
        while self.current_token() and self.current_token().type in [
            TokenType.EQUAL, TokenType.NOT_EQUAL,
            TokenType.LESS, TokenType.LESS_EQUAL,
            TokenType.GREATER, TokenType.GREATER_EQUAL
        ]:
            op = self.current_token().type
            self.advance()
            right = self.parse_additive()
            left = BinaryOp(left, op, right)
        
        return left
    
    def parse_additive(self) -> ASTNode:
        """Parse additive expression."""
        left = self.parse_multiplicative()
        
        while self.current_token() and self.current_token().type in [TokenType.PLUS, TokenType.MINUS]:
            op = self.current_token().type
            self.advance()
            right = self.parse_multiplicative()
            left = BinaryOp(left, op, right)
        
        return left
    
    def parse_multiplicative(self) -> ASTNode:
        """Parse multiplicative expression."""
        left = self.parse_unary()
        
        while self.current_token() and self.current_token().type in [TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO]:
            op = self.current_token().type
            self.advance()
            right = self.parse_unary()
            left = BinaryOp(left, op, right)
        
        return left
    
    def parse_unary(self) -> ASTNode:
        """Parse unary expression."""
        if self.current_token() and self.current_token().type in [TokenType.MINUS, TokenType.NOT]:
            op = self.current_token().type
            self.advance()
            operand = self.parse_unary()
            return UnaryOp(op, operand)
        
        return self.parse_power()
    
    def parse_power(self) -> ASTNode:
        """Parse power expression."""
        left = self.parse_primary()
        
        while self.current_token() and self.current_token().type == TokenType.POWER:
            op = self.current_token().type
            self.advance()
            right = self.parse_unary()
            left = BinaryOp(left, op, right)
        
        return left
    
    def parse_primary(self) -> ASTNode:
        """Parse primary expression."""
        token = self.current_token()
        if not token:
            raise SyntaxError("Unexpected end of input")
        
        # Literals
        if token.type == TokenType.NUMBER:
            self.advance()
            return NumberLiteral(token.value)
        
        if token.type == TokenType.STRING:
            self.advance()
            return StringLiteral(token.value)
        
        if token.type in [TokenType.TRUE, TokenType.FALSE, TokenType.MAYBE]:
            self.advance()
            value = 1 if token.type == TokenType.TRUE else (0 if token.type == TokenType.FALSE else -1)
            return BooleanLiteral(value)
        
        # Identifier or keyword used as identifier (like print, len)
        if token.type == TokenType.IDENTIFIER or token.type in [TokenType.PRINT, TokenType.LEN]:
            if token.type in [TokenType.PRINT, TokenType.LEN]:
                # Convert keyword to identifier for function calls
                name = Identifier(token.value.lower())
                self.advance()
            else:
                self.advance()
                name = Identifier(token.value)
            
            # Function call
            if self.current_token() and self.current_token().type == TokenType.LPAREN:
                return self.parse_function_call(name)
            
            # Member access
            if self.current_token() and self.current_token().type == TokenType.DOT:
                self.advance()
                # Allow keywords as member names (like .len)
                member_token = self.current_token()
                if member_token and (member_token.type == TokenType.IDENTIFIER or member_token.type in [TokenType.LEN]):
                    if member_token.type == TokenType.LEN:
                        member_name = "len"
                        self.advance()
                    else:
                        member_name = member_token.value
                        self.advance()
                    member_access = MemberAccess(name, member_name)
                    
                    # Check if it's a method call (member.function())
                    if self.current_token() and self.current_token().type == TokenType.LPAREN:
                        return self.parse_function_call(member_access)
                    
                    return member_access
                else:
                    raise SyntaxError(f"Expected member name at {member_token.line if member_token else '?'}:{member_token.column if member_token else '?'}")
            
            # Index access
            if self.current_token() and self.current_token().type == TokenType.LBRACKET:
                self.advance()
                index = self.parse_expression()
                self.expect(TokenType.RBRACKET, "Expected ]")
                return IndexAccess(name, index)
            
            return name
        
        # Vector literal
        if token.type == TokenType.LBRACKET:
            vec = self.parse_vector()
            # Check for index access after vector
            if self.current_token() and self.current_token().type == TokenType.LBRACKET:
                self.advance()
                index = self.parse_expression()
                self.expect(TokenType.RBRACKET, "Expected ]")
                return IndexAccess(vec, index)
            return vec
        
        # Parenthesized expression
        if token.type == TokenType.LPAREN:
            self.advance()
            expr = self.parse_expression()
            self.expect(TokenType.RPAREN, "Expected )")
            # Check for index access after parentheses
            if self.current_token() and self.current_token().type == TokenType.LBRACKET:
                self.advance()
                index = self.parse_expression()
                self.expect(TokenType.RBRACKET, "Expected ]")
                return IndexAccess(expr, index)
            return expr
        
        raise SyntaxError(f"Unexpected token {token.type.name} at {token.line}:{token.column}")
    
    def parse_function_call(self, name: ASTNode) -> FunctionCall:
        """Parse function call."""
        self.advance()  # Skip (
        
        args = []
        if self.current_token() and self.current_token().type != TokenType.RPAREN:
            while True:
                self.skip_newlines()  # Allow newlines in function arguments
                args.append(self.parse_expression())
                
                if self.current_token() and self.current_token().type == TokenType.COMMA:
                    self.advance()
                elif self.current_token() and self.current_token().type == TokenType.RPAREN:
                    break
                elif self.current_token() and self.current_token().type == TokenType.NEWLINE:
                    # Allow newline before closing paren
                    self.skip_newlines()
                    if self.current_token() and self.current_token().type == TokenType.RPAREN:
                        break
                    else:
                        raise SyntaxError(f"Unexpected token after argument at {self.current_token().line}:{self.current_token().column}")
                else:
                    break
        
        self.expect(TokenType.RPAREN, "Expected )")
        
        return FunctionCall(name, args)
    
    def parse_vector(self) -> VectorLiteral:
        """Parse vector literal."""
        self.advance()  # Skip [
        
        elements = []
        if self.current_token() and self.current_token().type != TokenType.RBRACKET:
            while True:
                elements.append(self.parse_expression())
                
                if self.current_token() and self.current_token().type == TokenType.COMMA:
                    self.advance()
                elif self.current_token() and self.current_token().type == TokenType.RBRACKET:
                    break
                else:
                    raise SyntaxError("Expected , or ]")
        
        self.expect(TokenType.RBRACKET, "Expected ]")
        
        return VectorLiteral(elements)
