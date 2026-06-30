from sys import argv

import rich

undefined = object()

def log(obj):
    if obj == undefined:
        rich.print(r"[yellow]undefined")
    else:
        rich.print(r"[blue]" + obj)
def main(instructions: list[list[str]]) -> None:
    stack = dict()
    
    for instruction in instructions:
        match instruction[0]:
            case "def":
                stack[instruction[1]] = undefined
            case "set":
                stack[instruction[1]] = instruction[2]
            case "log":
                log(stack[instruction[1]])
                

if __name__ == "__main__":
    instructions: list[list[str]] = []
    with open(argv[1], "r") as bytecode:
        for line in bytecode:
            if line.strip():
                instructions.append(line.split())
        # print(instructions)

    main(instructions)