from string import ascii_letters as alphabet

variables = dict()


def calculate(expression: list) -> None:
    result = int(expression[0])
    for i in range(1, len(expression) - 1, 2):
        sign = expression[i]
        number = int(expression[i + 1])
        if sign == '+':
            result += number
        if sign == '-':
            result -= number

    return result


def format_to_expr(string: str) -> list or str:
    blocks = string.split()
    if len(blocks) % 2 == 0:
        return None
    expression = []
    try:
        for value in blocks:
            if '+' in value or '-' in value:
                sign = sign_fix(value)
                if sign == "+" or sign == "-":
                    expression.append(sign)
                else:
                    expression.append(int(sign))
            else:
                if check_naming(value):
                    if value in variables.keys():
                        expression.append(variables[value])
                    else:
                        print("Unknown variable")
                        return None
                else:
                    number = int(value)
                    expression.append(number)
    except ValueError:
        return None
    else:
        return expression


def sign_fix(sign: str) -> str:
    minus_counter = 0
    for char in sign:
        if char == '-':
            minus_counter += 1
        elif char != '+':
            return sign
    if minus_counter % 2 == 0:
        return '+'
    else:
        return '-'


def check_naming(string: str) -> bool:
    for letter in string:
        if letter not in alphabet:
            return False
    return True


def add_variable(string: str):
    global variables
    elements = string.split('=', 1)
    variable = elements[0].strip()
    value = elements[1].strip()
    # check identifier
    if check_naming(variable):
        # check if it's a pointer to existing var
        if check_naming(value):
            keys = variables.keys()
            if value in keys:
                variables[variable] = variables[value]
            else:
                print("Unknown variable")
        else:
            # check if is a number
            try:
                number = int(value)
            except ValueError:
                print("Invalid assignment")
            else:
                variables[variable] = number
    else:
        print("Invalid identifier")


def process(string: str) -> None:
    if '=' in string:
        add_variable(string)
    else:
        expr = format_to_expr(string)
        if expr is None:
            return
        else:
            print(calculate(expr))


while True:
    command = input()
    if len(command) == 0:
        continue
    elif command.startswith('/'):
        if command == '/help':
            print("The program calculates the sum of numbers")
            continue
        elif command == '/exit':
            print("Bye!")
            break
        else:
            print("Unknown command")
    else:
        process(command)
