def calculate(string: str):
    expression = format_to_expr(string)
    result = int(expression[0])
    for i in range(1, len(expression) - 1, 2):
        sign = expression[i]
        number = int(expression[i + 1])
        if sign == '+':
            result += number
        if sign == '-':
            result -= number
    return result


def format_to_expr(string: str):
    blocks = string.split()
    expression = []
    for value in blocks:
        if '+' in value or '-' in value:
            expression.append(sign_fix(value))
        else:
            expression.append(value)
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


while True:
    command = input()
    if len(command) == 0:
        continue
    elif command == '/help':
        print("The program calculates the sum of numbers")
        continue
    elif command == '/exit':
        print("Bye!")
        break
    else:
        print(calculate(command))
