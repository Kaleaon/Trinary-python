"""
Main entry point for running TritLang programs.
"""

import sys
import os
from .lexer import Lexer
from .parser import Parser
from .interpreter import Interpreter


def run_file(filename: str):
    """Run a TritLang source file."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            source = f.read()
        
        run(source)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def run(source: str):
    """Run TritLang source code."""
    try:
        # Tokenize
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        
        # Parse
        parser = Parser(tokens)
        ast = parser.parse()
        
        # Interpret
        interpreter = Interpreter()
        interpreter.interpret(ast)
    except SyntaxError as e:
        print(f"Syntax Error: {e}", file=sys.stderr)
        sys.exit(1)
    except RuntimeError as e:
        print(f"Runtime Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


def repl():
    """Run TritLang REPL (Read-Eval-Print Loop)."""
    print("TritLang REPL - Type 'exit' or 'quit' to exit")
    print("Using balanced ternary: + (1), 0, - (-1)")
    print()
    
    interpreter = Interpreter()
    
    while True:
        try:
            line = input("trit> ")
            
            if line.strip() in ['exit', 'quit', 'q']:
                break
            
            if not line.strip():
                continue
            
            # Tokenize
            lexer = Lexer(line)
            tokens = lexer.tokenize()
            
            # Parse
            parser = Parser(tokens)
            ast = parser.parse()
            
            # Interpret
            result = interpreter.interpret(ast)
            
            if result is not None:
                print(result.value)
        
        except EOFError:
            break
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)


def main():
    """Main entry point."""
    if len(sys.argv) > 1:
        if sys.argv[1] == '-i' or sys.argv[1] == '--interactive':
            repl()
        else:
            run_file(sys.argv[1])
    else:
        repl()


if __name__ == "__main__":
    main()
