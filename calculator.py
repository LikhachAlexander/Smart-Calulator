def calculate(string: str) -> None:
    expression = format_to_expr(string)
    if isinstance(expression, str):
        print("Invalid expression")
        return
    result = int(expression[0])
    for i in range(1, len(expression) - 1, 2):
        sign = expression[i]
        number = int(expression[i + 1])
        if sign == '+':
            result += number
        if sign == '-':
            result -= number

    print(result)


def format_to_expr(string: str) -> list or str:
    blocks = string.split()
    if len(blocks) % 2 == 0:
        return "Error"
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
                number = int(value)
                expression.append(number)
    except ValueError:
        return "Error"
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
        calculate(command)
