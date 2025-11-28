"""
Interpreter for PentLang programming language.

Executes the AST and manages the runtime environment optimized for PNPU.
"""

from typing import Dict, List, Any, Optional, Callable
from .parser import *
from .runtime import PentValue, PentVector, PentMatrix
from .lexer import TokenType


class Interpreter:
    """Interprets and executes TritLang AST."""
    
    def __init__(self):
        self.variables: Dict[str, PentValue] = {}
        self.functions: Dict[str, FunctionDef] = {}
        self.scopes: List[Dict[str, PentValue]] = [{}]
        self.return_value: Optional[PentValue] = None
        self.return_flag = False
    
    def interpret(self, program: Program) -> Any:
        """Interpret a program."""
        self.return_value = None
        self.return_flag = False
        
        for statement in program.statements:
            self.execute(statement)
            if self.return_flag:
                break
        
        return self.return_value
    
    def execute(self, node: ASTNode) -> Any:
        """Execute a single AST node."""
        if isinstance(node, Program):
            return self.interpret(node)
        
        elif isinstance(node, NumberLiteral):
            return PentValue(node.value)
        
        elif isinstance(node, StringLiteral):
            return PentValue(node.value)
        
        elif isinstance(node, BooleanLiteral):
            return PentValue(node.value)
        
        elif isinstance(node, Identifier):
            return self.get_variable(node.name)
        
        elif isinstance(node, BinaryOp):
            return self.execute_binary_op(node)
        
        elif isinstance(node, UnaryOp):
            return self.execute_unary_op(node)
        
        elif isinstance(node, Assignment):
            return self.execute_assignment(node)
        
        elif isinstance(node, VariableDeclaration):
            return self.execute_variable_declaration(node)
        
        elif isinstance(node, IfStatement):
            return self.execute_if(node)
        
        elif isinstance(node, WhileStatement):
            return self.execute_while(node)
        
        elif isinstance(node, ForStatement):
            return self.execute_for(node)
        
        elif isinstance(node, FunctionCall):
            return self.execute_function_call(node)
        
        elif isinstance(node, FunctionDef):
            self.functions[node.name] = node
            return None
        
        elif isinstance(node, ReturnStatement):
            value = self.execute(node.value) if node.value else None
            self.return_value = value
            self.return_flag = True
            return value
        
        elif isinstance(node, VectorLiteral):
            elements = [self.execute(e) for e in node.elements]
            return PentVector(elements)
        
        elif isinstance(node, IndexAccess):
            return self.execute_index_access(node)
        
        elif isinstance(node, MemberAccess):
            return self.execute_member_access(node)
        
        else:
            raise RuntimeError(f"Unknown node type: {type(node)}")
    
    def execute_binary_op(self, node: BinaryOp) -> PentValue:
        """Execute a binary operation."""
        left = self.execute(node.left)
        right = self.execute(node.right)
        
        if node.op == TokenType.PLUS:
            return left + right
        elif node.op == TokenType.MINUS:
            return left - right
        elif node.op == TokenType.MULTIPLY:
            return left * right
        elif node.op == TokenType.DIVIDE:
            return left / right
        elif node.op == TokenType.MODULO:
            return left % right
        elif node.op == TokenType.POWER:
            return left ** right
        elif node.op == TokenType.EQUAL:
            return left == right
        elif node.op == TokenType.NOT_EQUAL:
            return left != right
        elif node.op == TokenType.LESS:
            return left < right
        elif node.op == TokenType.LESS_EQUAL:
            return left <= right
        elif node.op == TokenType.GREATER:
            return left > right
        elif node.op == TokenType.GREATER_EQUAL:
            return left >= right
        elif node.op == TokenType.AND:
            # Three-state AND: both must be truthy, if either is -1 (maybe), result is -1
            if isinstance(left.value, (int, float)) and isinstance(right.value, (int, float)):
                if left.value == -1 or right.value == -1:
                    return PentValue(-1)  # Maybe
                return PentValue(1 if (left.is_truthy() and right.is_truthy()) else 0)
            return PentValue(1 if (left.is_truthy() and right.is_truthy()) else 0)
        elif node.op == TokenType.OR:
            # Three-state OR
            if isinstance(left.value, (int, float)) and isinstance(right.value, (int, float)):
                if left.value == -1 or right.value == -1:
                    return PentValue(-1)  # Maybe
                return PentValue(1 if (left.is_truthy() or right.is_truthy()) else 0)
            return PentValue(1 if (left.is_truthy() or right.is_truthy()) else 0)
        else:
            raise RuntimeError(f"Unknown binary operator: {node.op}")
    
    def execute_unary_op(self, node: UnaryOp) -> PentValue:
        """Execute a unary operation."""
        operand = self.execute(node.operand)
        
        if node.op == TokenType.MINUS:
            return PentValue(-operand.value)
        elif node.op == TokenType.NOT:
            # Three-state NOT
            if isinstance(operand.value, (int, float)):
                if operand.value == -1:
                    return PentValue(-1)  # NOT Maybe = Maybe
                return PentValue(1 if not operand.is_truthy() else 0)
            return PentValue(1 if not operand.is_truthy() else 0)
        else:
            raise RuntimeError(f"Unknown unary operator: {node.op}")
    
    def execute_assignment(self, node: Assignment) -> PentValue:
        """Execute an assignment."""
        value = self.execute(node.value)
        
        if node.op == TokenType.ASSIGN:
            self.set_variable(node.name, value)
        elif node.op == TokenType.PLUS_ASSIGN:
            current = self.get_variable(node.name)
            self.set_variable(node.name, current + value)
        elif node.op == TokenType.MINUS_ASSIGN:
            current = self.get_variable(node.name)
            self.set_variable(node.name, current - value)
        else:
            raise RuntimeError(f"Unknown assignment operator: {node.op}")
        
        return value
    
    def execute_variable_declaration(self, node: VariableDeclaration) -> PentValue:
        """Execute a variable declaration."""
        value = None
        if node.value:
            value = self.execute(node.value)
        else:
            value = PentValue(0)  # Default to 0
        
        self.set_variable(node.name, value)
        return value
    
    def execute_if(self, node: IfStatement) -> Any:
        """Execute an if statement."""
        condition = self.execute(node.condition)
        
        if condition.is_truthy():
            return self.execute_block(node.then_branch)
        else:
            # Check elif branches
            for elif_condition, elif_body in node.elif_branches:
                elif_cond = self.execute(elif_condition)
                if elif_cond.is_truthy():
                    return self.execute_block(elif_body)
            
            # Execute else branch if present
            if node.else_branch:
                return self.execute_block(node.else_branch)
        
        return None
    
    def execute_while(self, node: WhileStatement) -> Any:
        """Execute a while loop."""
        while True:
            condition = self.execute(node.condition)
            if not condition.is_truthy():
                break
            
            result = self.execute_block(node.body)
            if self.return_flag:
                break
        
        return None
    
    def execute_for(self, node: ForStatement) -> Any:
        """Execute a for loop."""
        iterable = self.execute(node.iterable)
        
        if isinstance(iterable, PentVector):
            for element in iterable.elements:
                self.set_variable(node.var_name, element)
                result = self.execute_block(node.body)
                if self.return_flag:
                    break
        elif isinstance(iterable.value, (list, tuple)):
            for element in iterable.value:
                self.set_variable(node.var_name, PentValue(element))
                result = self.execute_block(node.body)
                if self.return_flag:
                    break
        else:
            raise RuntimeError(f"Cannot iterate over {type(iterable)}")
        
        return None
    
    def execute_function_call(self, node: FunctionCall) -> Any:
        """Execute a function call."""
        # Check if it's a method call (MemberAccess)
        if isinstance(node.name, MemberAccess):
            obj = self.execute(node.name.obj)
            method_name = node.name.member
            return self.execute_method_call(obj, method_name, node.args)
        
        if isinstance(node.name, Identifier):
            func_name = node.name.name
            
            # Built-in functions
            if func_name == "print":
                args = [self.execute(arg) for arg in node.args]
                values = []
                for arg in args:
                    if isinstance(arg, (PentVector, PentMatrix)):
                        values.append(str(arg))
                    elif isinstance(arg, PentValue):
                        values.append(str(arg.value))
                    else:
                        values.append(str(arg))
                print(" ".join(values))
                return PentValue(None)
            
            if func_name == "len":
                if len(node.args) != 1:
                    raise RuntimeError("len() takes exactly 1 argument")
                arg = self.execute(node.args[0])
                if isinstance(arg, PentVector):
                    return PentValue(len(arg))
                elif isinstance(arg.value, (list, tuple, str)):
                    return PentValue(len(arg.value))
                else:
                    raise RuntimeError(f"Cannot get length of {type(arg)}")
            
            # User-defined function
            if func_name not in self.functions:
                raise RuntimeError(f"Function '{func_name}' is not defined")
            
            func_def = self.functions[func_name]
            
            if len(node.args) != len(func_def.params):
                raise RuntimeError(f"Function '{func_name}' expects {len(func_def.params)} arguments, got {len(node.args)}")
            
            # Create new scope
            self.scopes.append({})
            
            # Set parameters
            for param_name, arg in zip(func_def.params, node.args):
                arg_value = self.execute(arg)
                self.set_variable(param_name, arg_value)
            
            # Execute function body
            self.return_flag = False
            result = self.execute_block(func_def.body)
            
            # Restore scope
            self.scopes.pop()
            
            return_value = self.return_value if self.return_flag else None
            self.return_flag = False
            
            return return_value if return_value is not None else PentValue(None)
        
        raise RuntimeError(f"Cannot call {type(node.name)}")
    
    def execute_index_access(self, node: IndexAccess) -> Any:
        """Execute index access."""
        obj = self.execute(node.obj)
        index = self.execute(node.index)
        
        if isinstance(obj, PentVector):
            idx = int(index.value)
            return obj[idx]
        elif isinstance(obj.value, (list, tuple, str)):
            idx = int(index.value)
            return PentValue(obj.value[idx])
        else:
            raise RuntimeError(f"Cannot index {type(obj)}")
    
    def execute_member_access(self, node: MemberAccess) -> Any:
        """Execute member access."""
        obj = self.execute(node.obj)
        
        if isinstance(obj, PentVector):
            if node.member == "sum":
                return obj.sum()
            elif node.member == "mean":
                return obj.mean()
            elif node.member == "len" or node.member == "length":
                return PentValue(len(obj))
            else:
                raise RuntimeError(f"Vector has no member '{node.member}'")
        elif isinstance(obj, PentMatrix):
            if node.member == "transpose":
                return obj.transpose()
            elif node.member == "height":
                return PentValue(obj.height)
            elif node.member == "width":
                return PentValue(obj.width)
            else:
                raise RuntimeError(f"Matrix has no member '{node.member}'")
        else:
            raise RuntimeError(f"Cannot access member '{node.member}' of {type(obj)}")
    
    def execute_method_call(self, obj: Any, method_name: str, args: List[ASTNode]) -> Any:
        """Execute a method call (obj.method(args))."""
        # Execute arguments
        arg_values = [self.execute(arg) for arg in args]
        
        if isinstance(obj, PentVector):
            if method_name == "sum":
                if len(arg_values) != 0:
                    raise RuntimeError("sum() takes no arguments")
                return obj.sum()
            elif method_name == "mean":
                if len(arg_values) != 0:
                    raise RuntimeError("mean() takes no arguments")
                return obj.mean()
            else:
                raise RuntimeError(f"Vector has no method '{method_name}'")
        elif isinstance(obj, PentMatrix):
            if method_name == "transpose":
                if len(arg_values) != 0:
                    raise RuntimeError("transpose() takes no arguments")
                return obj.transpose()
            else:
                raise RuntimeError(f"Matrix has no method '{method_name}'")
        else:
            raise RuntimeError(f"Cannot call method '{method_name}' on {type(obj)}")
    
    def execute_block(self, statements: List[ASTNode]) -> Any:
        """Execute a block of statements."""
        for statement in statements:
            self.execute(statement)
            if self.return_flag:
                break
        return None
    
    def get_variable(self, name: str) -> PentValue:
        """Get a variable value."""
        # Check scopes from innermost to outermost
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        
        # Check global variables
        if name in self.variables:
            return self.variables[name]
        
        raise RuntimeError(f"Variable '{name}' is not defined")
    
    def set_variable(self, name: str, value: PentValue):
        """Set a variable value."""
        # Set in current scope (innermost)
        self.scopes[-1][name] = value
