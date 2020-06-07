from collections import deque
from math import pi, e
from math import sin, cos, log


class Calculator:
    operators = ['^', '+', '-', '*', '/']
    parentheses = ['(', ')']
    numbers = "0123456789"

    def __init__(self):
        # variable storage
        self.variables = {
            "PI": pi,
            "e": e
        }
        self.functions = {
            "fact": Calculator.fact,
            "exp": Calculator.exp,
            "sin": sin,
            "cos": cos,
            "log": log
        }
        self.string = ""

    # split string by operands
    @staticmethod
    def format_to_infix(word: str) -> list:
        string = word.replace(" ", "")
        result = []
        temp = ""
        for letter in string:
            if letter not in Calculator.operators and letter not in Calculator.parentheses:
                temp += letter
            else:
                if temp != "":
                    result.append(temp)
                    temp = ""
                result.append(letter)
        if temp != "":
            result.append(temp)
        return result

    @staticmethod
    def is_number(string: str) -> bool:
        for letter in string:
            if letter not in Calculator.numbers + '.':
                return False
        return True

    @staticmethod
    def is_int(string) -> bool:
        for letter in string:
            if letter not in Calculator.numbers:
                return False
        return True

    def fill_values(self, array):
        result = []
        var_names = self.variables.keys()
        func_names = self.functions.keys()
        function = False
        counter = 0
        for i in range(len(array)):
            item = array[i]
            if not function:
                if item in self.operators or item in self.parentheses:
                    result.append(item)
                elif item in var_names:
                    result.append(self.variables[item])
                elif item in func_names:
                    argument = array[i + 2]
                    if Calculator.is_number(argument):
                        number = self.functions[item](float(argument))
                        result.append(number)
                        function = True
                        counter = 4
                    elif argument in var_names:
                        number = self.functions[item](self.variables[argument])
                        result.append(number)
                        function = True
                        counter = 4
                    else:
                        print("Invalid argument!")
                        return None
                elif Calculator.is_number(item):
                    result.append(float(item))
                else:
                    print("Unknown variable!")
                    return None

            if function:
                counter -= 1
                if counter == 0:
                    function = False
        return result

    @staticmethod
    def process_signs(array) -> list or None:
        result = []
        minus_counter = 0
        plus_bool = False
        for item in array:
            if item == '+':
                plus_bool = True
                if minus_counter > 0:
                    print("Invalid operators")
                    return None
            elif item == '-':
                minus_counter += 1
                if plus_bool:
                    print("Invalid operators")
                    return None
            else:
                if plus_bool:
                    result.append('+')
                    plus_bool = False
                if minus_counter > 0:
                    # append sign
                    if minus_counter % 2 == 0:
                        result.append('+')
                    else:
                        result.append('-')
                    minus_counter = 0
                result.append(item)
        if result[0] == '-':
            result[1] = result[1] * -1
            expr = result[1:]
        else:
            expr = result

        end_res = []
        left_par = False
        minus = False
        for item in expr:
            if item == '(':
                left_par = True
                end_res.append(item)
            elif item == '-' and left_par:
                minus = True
                left_par = False
            elif minus:
                end_res.append(float(item) * -1)
                minus = False
                left_par = False
            else:
                end_res.append(item)
                left_par = False
        return end_res

    @staticmethod
    def count_parenthesis(array) -> bool:
        stack = deque()
        for item in array:
            if item == '(':
                stack.append('(')
            elif item == ')':
                if len(stack) > 0:
                    stack.pop()
                else:
                    return False
        if len(stack) > 0:
            return False
        else:
            return True

    @staticmethod
    def precedence(char: str) -> int:
        if char == '^':
            return 3
        elif char == '*' or char == '/':
            return 2
        elif char == '+' or char == '-':
            return 1
        else:
            return 0

    def expression_to_infix(self, string) -> list or None:
        expr = Calculator.format_to_infix(string)
        expr1 = self.fill_values(expr)
        if expr1 is not None:
            expr2 = self.process_signs(expr1)
            return expr2
        else:
            return None

    def convert_to_postfix(self, array: list) -> deque or None:
        array.append(')')
        postfix = deque()
        stack = deque()
        stack.append('(')
        for item in array:
            if item not in self.operators and item not in self.parentheses:
                # is operand
                postfix.append(item)
            elif item == '(':
                stack.append(item)
            elif item == ')':
                while len(stack) > 0 and stack[-1] != '(':
                    a = stack.pop()
                    postfix.append(a)
                if len(stack) > 0 and stack[-1] != '(':
                    return None
                else:
                    stack.pop()

            # is operator
            elif item in self.operators:
                while len(stack) > 0 and Calculator.precedence(item) <= Calculator.precedence(stack[-1]):
                    postfix.append(stack.pop())
                stack.append(item)
        while len(stack) > 0:
            postfix.append(stack.pop())

        return postfix

    def calculate_expression(self, postfix: deque):
        stack = deque()
        for item in postfix:
            if item not in self.operators:
                if item is not None:
                    stack.append(float(item))
            else:
                if len(stack) > 1:
                    a = stack.pop()
                    b = stack.pop()
                    operator = item
                    value = Calculator.binary_operation(b, a, operator)
                    if value is not None:
                        stack.append(value)
                    else:
                        print("Zero division!")
                        return None
                else:
                    print("Invalid expression")
                    return None
        return stack.pop()

    @staticmethod
    def binary_operation(a, b, operator):
        if operator == '+':
            return a + b
        elif operator == '-':
            return a - b
        elif operator == '*':
            return a * b
        elif operator == '/':
            if b != 0:
                return a / b
            else:
                return None
        elif operator == '^':
            return a ** b

    def calculate(self, expression_string):
        expr = Calculator.format_to_infix(expression_string)
        # fill values
        expr1 = self.fill_values(expr)
        if expr1 is not None:
            # count signs
            expr2 = self.process_signs(expr1)
            if expr2 is not None:
                # count ()
                is_valid = self.count_parenthesis(expr2)
                if is_valid:
                    # count it
                    postfix = self.convert_to_postfix(expr2)
                    value = self.calculate_expression(postfix)
                    if value is not None:
                        return value
                else:
                    print("Invalid expression")
                    return None

    def add_variable(self, string: str) -> None:
        str_1, str_2 = string.split('=', 1)
        var_name = str_1.strip()
        for letter in var_name:
            if letter in self.numbers:
                print("Invalid name!")
                return None
        assignment = str_2.strip()
        value = self.calculate(assignment)
        if value is not None:
            self.variables[var_name] = value
        else:
            print("Invalid assignment")

    def process(self, string: str):
        if '=' not in string:
            # calculate expression
            result = self.calculate(string)
            if result is not None:
                print(result)
        else:
            self.add_variable(string)

    def run_command(self, commandlet):
        commands = {
            '/variables': 'variables\n\t' + '\n\t'.join(['"' + key + '": ' + str(name) for key, name in self.variables.items()]) ,
            '/help': 'This is complex expression calculator.\n'
                     'Type "/commands" to view available commands',
            '/functions': 'functions\n\t' + '\n\t'.join(self.functions.keys())
        }
        if commandlet in commands.keys():
            print(commands[commandlet])
        elif commandlet == '/commands':
            for item in commands.keys():
                print('\t', item)
            print('\t', '/exit')
        else:
            print('Unknown command\nType "/help"')

    # calculation functions
    @staticmethod
    def fact(n: float) -> float:
        if n <= 1:
            return 1
        else:
            return n * Calculator.fact(n - 1)

    @staticmethod
    def exp(x: float) -> float:
        return e ** x


calculator = Calculator()

while True:
    command = input('>')
    if len(command) == 0:
        continue
    elif command.startswith('/'):
        if command == '/exit':
            print("Bye!")
            break
        else:
            calculator.run_command(command)
    else:
        calculator.process(command)
