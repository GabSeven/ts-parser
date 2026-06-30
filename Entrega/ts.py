from enum import Enum, auto
from collections import ChainMap
from typing import Literal
from sys import argv

import rich
from lark import Lark, Token, Tree
from lark.visitors import Transformer_InPlaceRecursive, Visitor, Interpreter

debug = False
use_strict = True
# do que foi percebido, a única diferença dentro do contexto do que foi implentado
# é que o use strict faz com que function's sejam block scoped e não function scoped
# -- apesar disso, não é possível deixar False: é preciso adicionar a dependência em
# -- algumas partes do código

class SymbolType(Enum):
    FUNCTION = auto()
    VAR = auto()
    LET = auto()

class ErroSemantico(Exception):
    def __init__(self, tree, *args):
        super().__init__(*args)
        self.tree = tree
        tree = self.tree
        self.linha = 0
        self.coluna = 0
        if type(tree) == Tree and type(tree.children[0]) == Token:
                token = tree.children[0]
                self.linha = token.line
                self.coluna = token.column

    def __str__(self):
        return super().__str__()
        
FUNCTION = SymbolType.FUNCTION
VAR = SymbolType.VAR
LET = SymbolType.LET

undefined = object()
void = object()

any_type = {"number", "void"}

def typeof(value: Tree):
    print(value)
    return value.data

class Variable():
    def __init__(self, kind: Literal[SymbolType.VAR, SymbolType.LET], value = undefined, datatype = any_type):
        self._kind = kind
        self._value = value
        self._datatype = datatype
        self._assigned = False
        self.declared = False

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value: Tree):
        if self._datatype == any_type or typeof(value) in self._datatype:
            self._assigned = True
            self._value = value.children[0].value
        else: 
            raise ErroSemantico(value, "erro, tipos diferentes")

    @property
    def assigned(self):
        return self._assigned
    
    @assigned.setter
    def assigned(self, value: bool):
        self._assigned = value

    def __repr__(self):
        value = self.value
        datatype = self._datatype
        
        if value == undefined:
            value = "undefined"
        if datatype == any_type:
            datatype = "any"
        return f" {self._kind.name} - {value} - {datatype}"
    
    def __str__(self):
        value = self.value
        if value == undefined:
            value = r"undefined"
        return str(value)        

class Function():
    def __init__(self, return_datatype, params: list[Variable] = []):
        self.return_datatype = return_datatype
        self.params: list[Variable] =  params
    
    # def new_scope(self, scope) -> dict:
    #     for param in self.params:
    #         param.
    #     return {
    #         "__scope__": scope,
    #         "__blocks__": 0,
        # }
            
def function_scope(st: SymbolTable, name: str) -> str:
    if not use_strict and st["__type__"] == "block":
        return function_scope(st.parents, name)
    elif st["__type__"] == "global":
        return f"function-{name}"
    else:
        return f"{st["__scope__"]}-function-{name}"

def block_scope(scope: str, block_amount: int)-> str:
    if scope == "global":
        return f"block-{block_amount}"
    else: 
        return f"{scope}-block-{block_amount}"


class SymbolTable(ChainMap):
    def att(self, name: str, value: Tree) -> None:
        if name in self:
            dict_atual = self
            while dict_atual.maps[0]:
                if name in dict_atual.maps[0]:
                    variable: Variable = dict_atual[name]
                    variable.value = value
                    variable.assigned = True
                    variable.declared = True
                    break
                dict_atual = dict_atual.parents

    def def_var(self, tree: Tree[Token])-> None:
        name = tree.children[0].value
        data_type = any_type
        # value_tree = next((t for t in tree.children if isinstance(t, Tree) and t.data == "value"), None)
        # type_value = typeof(value_tree) if value_tree is not None else any_type

        # for t in tree.children:
        #     if isinstance(t, Tree) and hasattr(t.data, "value") and t.data.value == "type":
        #         data_type = {_.value for _ in t.children}
        #         if "any" in data_type:
        #             data_type = any_type 
        # print(data_type)
        # print(type_value)

        # if type_value != data_type or type_value not in data_type:
        #     raise ErroSemantico(tree, f"Type '{type_value}' is not assignable to type '{data_type}'")

        if name in self:
            symbol = self[name]
            if type(symbol) == Variable and symbol._kind == LET:
                raise ErroSemantico(" ", f"Cannot redeclare block-scoped variable {name}.")
            elif type(symbol) == Variable and not (data_type == symbol._datatype or data_type in symbol._datatype):
                raise ErroSemantico(" ", "aa")
                
            elif type(symbol) != Variable: 
                raise ErroSemantico(" ", f"Duplicate identifier {name}")

        

        dict_atual = self
        while dict_atual.maps[0]["__type__"] == "block":
            dict_atual = dict_atual.parents

        dict_atual[name] = Variable(VAR, datatype=data_type)

    def def_let(self, tree: Tree[Token], data_type = any_type)-> None:
        name = tree.children[0].value
        if name in self.maps[0]:
            symbol = self[name]
            if type(symbol) == Variable and symbol._kind == LET:
                raise ErroSemantico(name, f"Cannot redeclare block-scoped variable {name}.")
            else: 
                raise ErroSemantico(name, f"Duplicate identifier {name}")
        self[name] = Variable(LET, datatype=data_type)

    def def_fun(self, name: str, scope: str, tree: Tree[Token]) -> None:
        return_type = any_type
        for child in tree.children:
            if isinstance(child, Tree) and child.data == "type":
                return_type = {t.value for t in child.children}

        dict_atual = self
        while not use_strict and dict_atual.maps[0]["__type__"] == "block":
            dict_atual = dict_atual.parents

        dict_atual[name] = {
            "__scope__": scope, 
            "__tree__": tree,
            "__return_type__": return_type
            } 
        
    def set_declared(self, name: str):
        if name in self:
            dict_atual = self
            while dict_atual.maps[0]:
                if name in dict_atual.maps[0]:
                    variable: Variable = dict_atual[name]
                    variable.declared = True
                    break
                dict_atual = dict_atual.parents
        else:
            raise RuntimeError("Algo de muito errado ocorrey, deveria estar definido. Verificar se symboltable foi contruida - Builder().visit(tree)")

    def __missing__(self, key):
        raise ErroSemantico("a", f"{key} is not defined")

symbol_table = SymbolTable({"__scope__": "global", "console": {"log":"teste"}, "__blocks__": 0, "__type__":"global"})
scope_symbol_table: dict[str, ChainMap] = {"global":symbol_table}

class Builder(Interpreter):
    def function(self, tree: Tree[Token]):
        global symbol_table
        function_name = tree.children[0].value

        if function_name in symbol_table.maps[0]:
            if type(symbol_table[function_name]) == Variable:
                raise ErroSemantico(tree, f"Duplicate identifier '{function_name}'.")
            else:
                raise ErroSemantico(tree, "Duplicate function implementation")

        # eh a melhor forma?
        scope = function_scope(symbol_table, function_name)
        
        symbol_table.def_fun(function_name, scope, tree)
        
        symbol_table = symbol_table.new_child({"__scope__": scope, "__blocks__": 0, "__type__":"function"})
        scope_symbol_table.update({scope: symbol_table})

        self.visit_children(tree)

        symbol_table = symbol_table.parents

    def block(self, tree: Tree[Token]):
        global symbol_table
        symbol_table.update({"__blocks__": symbol_table["__blocks__"] + 1})

        scope = block_scope(symbol_table["__scope__"], symbol_table["__blocks__"])
        
        symbol_table = symbol_table.new_child({"__scope__": scope, "__blocks__": 0, "__type__":"block"})
        scope_symbol_table.update({scope: symbol_table})
        
        self.visit_children(tree)
        # symbol_table.update({"__blocks__": 0})

        symbol_table = symbol_table.parents

    def v_def(self, tree: Tree[Token]):
        global symbol_table
        symbol_table.def_var(tree)
        
    def v_att(self, tree):
        self.v_def(tree)

    def l_def(self, tree: Tree[Token]):
        global symbol_table
        symbol_table.def_let(tree)

    def l_att(self, tree):
        self.l_def(tree)

    # def check_names(self, tree):
    #     variable_acess = [t for t in tree.children if type(t) is Tree and t.data in ["test", "attribution"]]
    #     # vals = [t.value for t in node.children if type(t) is lark.Token]
    #     # t not in scope_symboltable[scope..]: raise
    #     # for child in node.children:
    #     #     if type(child) is lark.Tree:
    #     #         self.visit(child)        
    #     pass

class Walker(Interpreter):
    def NUMBER(self, tok): return int(tok)
    def NAME(self, tok): return str(tok)

    def __init__(self):
        global symbol_table
        symbol_table.update({"__blocks__":0})
    
    def call(self, tree: Tree[Token]):
        global symbol_table

        function_name = tree.children[0].value
        
        symbol_table_og = symbol_table
        scope = symbol_table[function_name]["__scope__"]
        function_tree = symbol_table[function_name]["__tree__"]
        symbol_table = scope_symbol_table[scope]
        
        symbol_table.update({"__blocks__": 0})
        
        self.visit_children(function_tree)

        symbol_table = symbol_table_og

    def function(self, tree: Tree[Token]):
        global symbol_table   
        function_name = tree.children[0].value
        expected_return_type = symbol_table[function_name]["__return_type__"]
        
        has_return = any(isinstance(t, Tree) and t.data == "return" and t.children for t in tree.children)
        
        if expected_return_type not in (any_type, "void") and not has_return:
            raise ErroSemantico(tree, "A function whose declared type is neither 'undefined', 'void', nor 'any' must return a value.")
        
        if expected_return_type != any_type:
            for t in tree.children:
                if isinstance(t, Tree) and t.data == "return":
                    return_value: Token =  t.children[0]
                    if return_value.type.lower() not in expected_return_type:
                        raise ErroSemantico(tree, "A function whose declared type is neither 'undefined', 'void', nor 'any' must return a value.")
            


    def block(self, tree: Tree[Token]):
        global symbol_table
        symbol_table.update({"__blocks__": symbol_table["__blocks__"] + 1})
        
        symbol_table_og = symbol_table
        scope = block_scope(symbol_table["__scope__"], symbol_table["__blocks__"])
        
        symbol_table = scope_symbol_table[scope]
        
        symbol_table.update({"__blocks__": 0})

        self.visit_children(tree)
        
        symbol_table = symbol_table_og

    def v_def(self, tree: Tree[Token]):
        global symbol_table
        symbol_table.set_declared(tree.children[0].value)

    def v_att(self, tree: Tree[Token]):
        global symbol_table
        items = tree.children
        symbol_table.att(items[0], items[1])
 
    def l_def(self, tree: Tree[Token]):
        global symbol_table
        symbol_table.set_declared(tree.children[0].value)

    def l_att(self, tree: Tree[Token]):
        global symbol_table
        items = tree.children
        symbol_table.att(items[0], items[1])

    def attribution(self, tree:Tree[Token]):
        global symbol_table

        items = tree.children
        for i in range(0, len(items), 2):
            symbol_table.att(items[i], items[i+1])

    def access(self, tree: Tree[Token]) -> Variable:
        global symbol_table
        v: Token = tree.children[0]
        variable: Variable = symbol_table[v.value]
        if variable._kind == LET and not variable.declared:
            raise ErroSemantico(tree, f"Block-scoped variable used before its declarations")
        elif variable._kind == VAR and not variable.declared and not variable.assigned:
            raise ErroSemantico(tree, f"Variable '{v}' is used before being assigned.")
        return variable

    def print(self, tree: Tree[Token]):
        rich.print(self.access(tree))

def main():
    parser = Lark.open("typeScript-grammar.lark", parser="lalr")

    with open(argv[1], "r") as program:
        tree = parser.parse(program.read())

    Builder().visit(tree)
    Walker().visit(tree)

if __name__ == "__main__" and len(argv) == 2:
    try:
        main()
    except ErroSemantico as e:
        print(e)
        rich.print(f"File[magenta]\"{argv[1]}\"[/magenta], line [magenta]{e.linha}[/magenta]")
        
