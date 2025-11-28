#!/usr/bin/env python3
"""
Command-line interface for TritLang.
"""

import sys
from .__main__ import run_file, run, repl

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] in ['-i', '--interactive', 'repl']:
            repl()
        elif sys.argv[1] in ['-h', '--help']:
            print("TritLang - A programming language for LLMs and ML using balanced ternary")
            print()
            print("Usage:")
            print("  tritlang <file>     Run a TritLang source file")
            print("  tritlang -i          Start interactive REPL")
            print("  tritlang --help     Show this help message")
        else:
            run_file(sys.argv[1])
    else:
        repl()
