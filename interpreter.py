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
            if char in "/-*<e":
                char += line[c+1]
                two_char = True
            parsed[-1].append(char)
    return parsed

def run(code, acc, acc_active, a, printed, *args):
    for char in code:
        if char == "//":
            try:
                acc[acc_active] += args[a]
            except:
                acc[acc_active] += acc[1^acc_active]
            a += 1
        if char == "--":
            acc[acc_active] = is_prime(acc[acc_active])
        if char == "/*":
            acc[acc_active] = 0
        if char == "*/":
            print(end=acc[acc_active])
            printed = True
        if char == '<#':
            acc_active = 1 ^ acc_active
        if char == '<!':
            acc[acc_active] = acc[acc_active] // acc[acc_active]
        if char == 'e#':
            acc[acc_active] = 0 - acc[acc_active]
        if char == '{-':
            acc[acc_active] = acc[acc_active] ^ 1
            
        if char == '!':
            acc[acc_active] = acc[acc_active] * acc[1^acc_active]
        if char == '%':
            acc[acc_active] = acc[acc_active] % acc[1^acc_active]
        if char == " ":
            acc[acc_active] += 1
        if char == "#":
            print(end=chr(acc[acc_active]))
            printed = True
            
    return acc, acc_active, a, printed

def interpreter(code, *args):
    acc = [0,0]
    acc_active = 0
    a = 0
    printed = False
    for line in parser(code):
        if line[0] == ';':
            for i in range(acc[active]):
                acc, acc_active, a, printed = run(line, acc, acc_active, a, printed, *args)
        elif line[0] == ':':
            if acc[active]:
                acc, acc_active, a, printed = run(line, acc, acc_active, a, printed, *args)
        elif line[0] == '?':
            while acc[acc_active]:
                acc, acc_active, a, printed = run(line, acc, acc_active, a, printed, *args)
        else:
            acc, acc_active, a, printed = run(line, acc, acc_active, a, printed, *args)
    if not printed:
        print(chr(acc[acc_active]))
        
def eval_input(args):
    final = []
    for arg in args:
        try:
            final.append(int(arg))
        except:
            continue
    return final

if __name__ == "__main__":
    import sys
    program = sys.argv[1]
    args = eval_input(sys.argv[2:])
    if program.endswith(".txt"):
        program = open(program).read()
    interpreter(program, *args)
