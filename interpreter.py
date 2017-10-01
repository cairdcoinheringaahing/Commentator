#!/usr/bin/env python3

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
            if char in "/-*<e{":
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
                acc[acc_active] += acc[(acc_active + 1) % len(acc)]
            a += 1
        if char == "--":
            acc[acc_active] = is_prime(acc[acc_active])
        if char == "/*":
            print(end=chr(acc[acc_active]))
            printed = True
        if char == "*/":
            print(end=str(acc[acc_active]))
            printed = True
        if char == '{-':
            acc_active = (acc_active + 1)
            try:
                acc[acc_active]
            except:
                acc.append(0)
        if char == '<!':
            acc[acc_active] = acc[acc_active] // acc[(acc_active + 1) % len(acc)]
        if char == 'e#':
            acc[acc_active] = 0 - acc[acc_active]
        if char == '<#':
            acc[acc_active] = acc[acc_active] ^ 1
        if char == '-}':
            acc_active = (acc_active - 1) % len(acc)
            if acc_active < 0:
                acc_active = (len(acc)+1) + acc_active
            
        if char == '!':
            acc[acc_active] = acc[acc_active] * acc[(acc_active + 1) % len(acc)]
        if char == '%':
            acc[acc_active] = acc[acc_active] % acc[(acc_active + 1) % len(acc)]
        if char == " ":
            acc[acc_active] += 1
        if char == "#":
            acc[acc_active] = 0
            
    return acc, acc_active, a, printed

def interpreter(code, *args):
    acc = [0]
    acc_active = 0
    a = 0
    printed = False
    for line in parser(code):
        if line[0] == ';':
            for i in range(acc[acc_active]):
                acc, acc_active, a, printed = run(line, acc, acc_active, a, printed, *args)
        elif line[0] == ':':
            if acc[acc_active]:
                acc, acc_active, a, printed = run(line, acc, acc_active, a, printed, *args)
        elif line[0] == '?':
            while acc[acc_active]:
                acc, acc_active, a, printed = run(line, acc, acc_active, a, printed, *args)
        else:
            acc, acc_active, a, printed = run(line, acc, acc_active, a, printed, *args)
    if not printed:
        print(acc[acc_active])
    return printed

def eval_input(args):
    final = []
    for arg in args:
        try:
            final.append(int(arg))
        except:
            continue
    return final

def REPL(helpmessage,lastcode=''):

    if helpmessage:
        print('''Welcome to Commentator REPL environment!
This allows you to enter and run Commentator code,
without having to run from the command line!

When >>> appears on the screen, this is asking you for a line of code.
This will continue to ask for code, until you enter a blank line

You can also begin a line of code with a § symbol
This will create a single line of code, and goes straight the input

Then it will ask you for inputs (a > will appear)
Please enter each input on a separate prompt

The output for the program will then be displayed below.

Enter 'exit' to quit the REPL.

''')

    code = []
    line = input('>>> ')
    if not line:
        print(line)
        REPL(False)
    if line == 'exit':
        return
    if line[0] == '§':
        code = line[1:]
        line = False
    if line == '^':
        code = last_code
    
    while line:
        code.append(line)
        line = input('>>> ')

    if line == '':
        code = '\n'.join(code)

    inputs = []
    for i in range(code.count('//')):
        last_in = input('> ')
        inputs.append(last_in)
    inputs = eval_input(inputs)

    if interpreter(code, *inputs):
        print()

    REPL(False,code)

if __name__ == "__main__":
    import sys
    try:
        program = sys.argv[1]
        args = eval_input(sys.argv[2:])
        if program.endswith(".txt"):
            program = open(program).read()
    except:
        if sys.argv[0] != '.code.tio':
            REPL(True)
            
    try:
        interpreter(program, *args)
    except:
        pass
