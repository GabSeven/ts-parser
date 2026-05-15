import collections
from sys import argv

import rich
from lark import Lark, Token, Tree



symbol_table = collections.ChainMap({"scope": "global"})

class Walker:
    def program(self):
        print("oi")

def main():
    parser = Lark.open("typeScript-grammar.lark")

    with open(argv[1], "r") as program:
        tree = parser.parse(program.read())

    # rich.print(tree)

    # # Walker().visit(tree)
    # rich.print(symbol_table)



if __name__ == "__main__" and len(argv) == 2:
    main()
