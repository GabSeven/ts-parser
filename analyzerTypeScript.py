from enum import Enum, auto
from collections import ChainMap
from sys import argv

import rich
from lark import Lark, Token, Tree

def funcion_scope(scope: str, name: str) -> str:
    if scope == "__global__":
        return f"function-{name}"
    else:
        return f"{scope}-function-{name}"

def block_scope(scope: str, block_amount: int)-> str:
    if scope == "__global__":
        return f"block-{block_amount}"
    else: 
        return f"{scope}-block-{block_amount}"
    
class SymbolTable(ChainMap):
    def att(self, name, value):
        if name in self:
            dict_atual = self
            while dict_atual.maps[0]:
                if name in dict_atual.maps[0]:
                    dict_atual.update({name:value})
                    break
                dict_atual = dict_atual.parents


symbol_table = SymbolTable({"__scope__": "global", "console": {"log":"teste"}, "__blocks__": 0})
scope_symbol_table: dict[str, ChainMap] = {"global":symbol_table}


class Builder:
    def function(self, NAME):
        global symbol_table
        scope = funcion_scope(symbol_table["__scope__"], NAME)
        symbol_table = symbol_table.new_child({"__scope__": scope, "__blocks__": 0})
        scope_symbol_table.update({scope: symbol_table})

    def block(self):
        global symbol_table
        symbol_table.update({"__blocks__": symbol_table["__blocks__"] + 1})
        scope = block_scope(symbol_table["__scope__"], symbol_table["__blocks__"])
        symbol_table = symbol_table.new_child({"__scope__": scope, "__blocks__": 0})
        scope_symbol_table.update({scope: symbol_table})

    def end(self):
        global symbol_table
        rich.print(symbol_table)
        symbol_table = symbol_table.parents

    def build_symbol_table(self, node):
        vals = [t.value for t in node.children if type(t) is Token]

        if hasattr(self, node.data):
            if node.data in ["v_def", "v_att", "l_def", "l_att"]:
                if node.data[0] == 'v':
                    self.v_def(*vals)
                else: 
                    self.l_def(*vals)
            else: 
                getattr(self, node.data)(*vals)

        for child in node.children:
            if type(child) is Tree:
                self.build_symbol_table(child)

class Walker:
    def NUMBER(self, tok): return int(tok)
    def NAME(self, tok): return str(tok)
    # def function(self, NAME):
    #     global symbol_table
    #     scope = funcion_scope(symbol_table["__scope__"], NAME)
    #     symbol_table = scope_symbol_table[scope]

    def block(self):
        global symbol_table
        symbol_table.update({"__blocks__": symbol_table["__blocks__"] + 1})
        scope = block_scope(symbol_table["__scope__"], symbol_table["__blocks__"])
        symbol_table = scope_symbol_table[scope]

    def end(self):
        global symbol_table
        rich.print(symbol_table)
        symbol_table = symbol_table.parents

    def attribution(self, *items):
        global symbol_table
        print(items)
        for i in range(0, len(items), 2):
            symbol_table.att(items[i], items[i+1])

    def print(self, NAME):
        global symbol_table
        print(symbol_table[NAME])

    # def call(self, NAME):
        
    def visit(self, node):
        vals = [t.value for t in node.children if type(t) is Token]
        if hasattr(self, node.data):
            getattr(self, node.data)(*vals)
        for child in node.children:
            if type(child) is Tree:
                self.visit(child)

def main():
    parser = Lark.open("typeScript-grammar.lark")

    with open(argv[1], "r") as program:
        tree = parser.parse(program.read())

    # rich.print(tree)

    Builder().build_symbol_table(tree)
    Walker().visit(tree)
    rich.print(scope_symbol_table)



if __name__ == "__main__" and len(argv) == 2:
    main()
