from collections import deque
from math import pi, e


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
            "exp": Calculator.exp
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
                        if number is None:
                            print("Invalid argument")
                            return None
                        result.append(number)
                        function = True
                        counter = 4
                    elif argument in var_names:
                        number = self.functions[item](self.variables[argument])
                        if number is None:
                            print("Invalid argument")
                            return None
                        result.append(number)
                        function = True
                        counter = 4
                    else:
                        print("Invalid naming!")
                        return None
                elif Calculator.is_number(item):
                    result.append(float(item))
                else:
                    print("Invalid naming!")
                    return None

            if function:
                counter -= 1
                if counter == 0:
                    function = False
        return result

    @staticmethod
    def process_signs(array) -> list:
        result = []
        minus_counter = 0
        plus_bool = False
        for item in array:
            if item == '+':
                plus_bool = True
            elif item == '-':
                minus_counter += 1
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
        return result

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

    def expression_to_infix(self, string) -> list:
        expr = Calculator.format_to_infix(string)
        expr1 = self.fill_values(expr)
        if expr1 is not None:
            expr2 = self.process_signs(expr1)
            return expr2
        else:
            return None

    def convert_to_postfix(self, array: list) -> deque:
        array.append(')')
        print(array)
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


    # calculation functions
    @staticmethod
    def fact(n):
        if n <= 1:
            return 1
        else:
            return n * Calculator.fact(n - 1)

    @staticmethod
    def exp(x):
        return e ** x


calculator = Calculator()

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
        print(calculator.convert_to_postfix( calculator.expression_to_infix(command)))
