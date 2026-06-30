from enum import Enum, auto
from collections import ChainMap
from sys import argv

import rich
from lark import Lark, Token, Tree

reserved_symbols: {"let", "var"}
symbol_table = ChainMap({"__scope__": "global", "console": {"log":"teste"}, "__blocks__": 0})


class SymbolType(Enum):
    FUNCTION = auto()
    VAR = auto()
    LET = auto()

type FUNCTION = SymbolType.FUNCTION
type VAR = SymbolType.VAR
type LET = SymbolType.LET

undefined = object()
any = object()

class Type(Enum):
    NUMBER = "number"

NUMBER = Type.NUMBER


def typeof(value):
    # atualmente só tem esse tipo
    return NUMBER

class Variable():
    def __init__(self, symbol_type: VAR | LET, value = undefined, type = any):
        self._symbol_type = symbol_type
        self._value = value
        self._type = type

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if self._type == any or typeof(value) in self._type:
            self._value = value
        else: 
            raise Exception()

    def __repr__(self):
        value = self.value
        type = self._type
        
        if value == undefined:
            value = "undefined"
        if type == any:
            type = "any"
        return f"{value} : {self._type}"

class Function():
    def __init__(self, return_type):
        self.return_type = return_type


class Walker:
    def function(self, NAME):
        if symbol_table["__scope__"] != "global":
            symbol_table.maps.insert(0, {"__scope__": f"{symbol_table["__scope__"]} - function-" + NAME, "__blocks__": 0})
        else:
            symbol_table.maps.insert(0, {"__scope__": "function" + NAME, "__block__": 0})

    def block(self):
        symbol_table.update({"__blocks__": symbol_table["__blocks__"] + 1})

        if symbol_table["__scope__"] != "global":
            symbol_table.maps.insert(0, {"__scope__": f"{symbol_table["__scope__"]} - block-{symbol_table["__blocks__"]}", "__blocks__": 0})
        else:
            symbol_table.maps.insert(0, {"__scope__": f"block-{symbol_table["__blocks__"]}", "__blocks__": 0})
    

    def end(self):
        rich.print(symbol_table)
        symbol_table.maps.pop(0)

    def visit(self, node):
        vals = [t.value for t in node.children if type(t) is Token]
        if hasattr(self, node.data):
            getattr(self, node.data)(*vals)
        for child in node.children:
            if type(child) is Tree:
                self.visit(child)
            
    def build_symbol_table(self, node):
        vals = [t.value for t in node.children if type(t) is Token]

        if hasattr(self, node.data) and node.data in ["v_def", "v_att", "l_def", "l_att"]:
            if node.data[0] == 'v':
                self.v_def(*vals)
            else: 
                self.l_def(*vals)

        for child in node.children:
            if type(child) is Tree:
                self.build_symbol_table(child)
    
def main():
    parser = Lark.open("typeScript-grammar.lark")

    with open(argv[1], "r") as program:
        tree = parser.parse(program.read())

    rich.print(tree)

    Walker().build_symbol_table(tree)
    rich.print(symbol_table)



if __name__ == "__main__" and len(argv) == 2:
    main()
