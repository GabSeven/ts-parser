import collections
import lark
import rich

# version 4 [nested functions]
grammar = r"""
program:     definition* function* call*
function:    NAME "{" statement* "}" end
end:
?statement:  definition | attribution | function | call
definition:  "var" NAME
attribution: NAME "=" NUMBER
call:        NAME "()"

NAME:   /\w+/
NUMBER: /\d+/
%ignore /[ \t\n\r]+/
"""

program = """
var a
f {
  var c
  c = 1
  g {
     var e
     a = 2
     c = 3
     e = 4
  }
  g()
}
f()
"""

parser = lark.Lark(grammar, start='program')
tree = parser.parse(program)
#rich.print(tree)
symbol_table = collections.ChainMap({'scope': 'global'})

class Walker:
  def function(self, NAME):
    symbol_table.maps.insert(0, {'scope': NAME+'()'})

  def end(self):
    #rich.print(symbol_table)
    symbol_table.maps.pop(0)

  def call(self, NAME):
    emit(f'sub {NAME}()')

  def definition(self, NAME):
    if NAME not in symbol_table.maps[0]:
      symbol_table[NAME] = 'int'
      #print('def:', NAME)
    else:
      rich.print('[red]error: redefined variable', NAME)

  def attribution(self, NAME, NUMBER):
    for s in symbol_table.maps:
      if NAME in s:
        emit(f"set {s['scope']}:{NAME} {NUMBER}")
        break
    else:
      rich.print('[red]error: unknown variable', NAME)

  def visit(self, node):
    vals = [t.value for t in node.children if type(t) is lark.Token]
    if hasattr(self, node.data):
        getattr(self, node.data)(*vals)
    for child in node.children:
      if type(child) is lark.Tree:
        self.visit(child)

# collect emitted bytecode
bytecode = collections.defaultdict(str)
def emit(instruction):
  bytecode[symbol_table.maps[0]['scope']] += instruction + '\n'

Walker().visit(tree)
#rich.print(symbol_table)

# output bytecode grouped by scope
for k,v in bytecode.items():
  print(f'fun {k}\n{v}ret\n')

