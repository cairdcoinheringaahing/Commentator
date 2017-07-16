def is_prime(x):
    for i in range(2,x):
        if x % i == 0:
            return 0
    return 1

def parser(code):
    code = code.split("\n")
    parsed = []
    two_char = False

    for line in code:
        parsed.append([])
        for c in range(len(line)):
            if two_char:
                two_char = False
                continue
            char = line[c]
            if char in "/-*":
                char += line[c+1]
                two_char = True
            parsed[-1].append(char)
    return parsed

def run(code, acc, a, printed, *args):
    for char in code:
        if char == " ":
            acc += 1
        if char == "#":
            print(chr(acc))
            printed = True
        if char == "//":
            try:
                acc += args[a]
            except:
                acc += 1
            a += 1
        if char == "--":
            acc = is_prime(acc)
        if char == "/*":
            acc = 0
        if char == "*/":
            print(acc)
            printed = True
    return acc, a, printed

def interpreter(code, *args):
    acc = 0
    a = 0
    ln = 0
    printed = False
    for line in parser(code):
        ln ^= 1
        if ln == 0 and line[0] == ";":
            for i in range(acc):
                acc, a, printed = run(line, acc, a, printed, *args)
        else:
            acc, a, printed = run(line, acc, a, printed, *args)
    if not printed:
        print(chr(acc))

if __name__ == "__main__":
    import sys
    program = sys.argv[1]
    args = list(map(int, sys.argv[2:]))
    if program.endswith(".txt"):
        program = open(program).read()
    interpreter(program, *args)
