"""Submodule for parsing themes"""
from washr.parser import ast, grammar

def parse(source):
    """Parses and builds an AST for the passed in code"""
    return ast.parse(grammar.parse(source))
