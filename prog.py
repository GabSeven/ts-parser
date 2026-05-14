import rich

# Example program

program = """
var a
main {
    var a
    var b
    a = 5
    b = 6
}
# comment
"""

# Grammar:
#  program: definition* attribution*
#  definition: "var" NAME
#  attribution: NAME "=" NUMBER

global_symbol_table = []
local_symbol_table = []

for line in program.split("\n"):
    # line = line.strip()

    # if not line:
    #     continue
    inside_main = False
    match line.strip().split():
        case ["main", "{"]:
            inside_main = True
        case ["}"]:
            inside_main = False
        case ["var", NAME]:
            if not inside_main and NAME not in global_symbol_table:
                global_symbol_table.append(NAME)
            elif inside_main and NAME not in local_symbol_table:
                local_symbol_table.append(NAME)
                print("def:", NAME)
            else:
                print("err: redefined variable", NAME)
        case [NAME, "=", NUMBER]:
            if not inside_main and NAME in global_symbol_table:
                print("att glo: ", NAME, NUMBER)
            elif inside_main and NAME in local_symbol_table:
                print("att loc: ", NAME, NUMBER)
            else:
                print("err: unknow variable", NAME)
        case _:
            print("unknown:", line)
