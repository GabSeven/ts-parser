import lark
import rich

# grammar V1a
grammar = r"""
program:     definition* main
main:        "main" start "{" definition* attribution* "}"
start:
definition:  "var" NAME
attribution: NAME "=" NUMBER

NAME:   /\w+/
NUMBER: /\d+/

%import common.WS
%ignore WS
"""

# example program
program = """
var a

main {
  var a
  var b
  var b
  a = 5
  b = 6
}
"""

# parse program
parser = lark.Lark(grammar, start='program')
tree = parser.parse(program)
rich.print(tree)

inside_main = False
global_symbol_table = []
local_symbol_table = []

class Walker(lark.visitors.Visitor_Recursive):
  def start(self, node):
    global inside_main
    inside_main = True

  def definition(self, node):
    NAME = node.children[0].value
    if not inside_main and NAME not in global_symbol_table:
      global_symbol_table.append(NAME)
      print('def glo:', NAME)
    elif inside_main and NAME not in local_symbol_table:
      local_symbol_table.append(NAME)
      print('def loc:', NAME)
    else:
      rich.print('[red]error  : redefined variable', NAME)
    
  def attribution(self, node):
    NAME = node.children[0].value
    NUMBER = node.children[1].value
    if not inside_main and NAME in global_symbol_table:
      print('att glo:', NAME, NUMBER)
    elif inside_main and NAME in local_symbol_table:
      print('att loc:', NAME, NUMBER)
    else:
      rich.print('[red]error  : unknown variable', NAME)

Walker().visit(tree)

