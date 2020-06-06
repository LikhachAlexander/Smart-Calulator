from string import ascii_letters as alphabet
from math import pi, e


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


class Calculator:
    operands = ['+', '-', '*', '/', '(', ')']

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
            if letter not in Calculator.operands:
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
            if letter in alphabet:
                return False
        return True

    @staticmethod
    def is_int(string) -> bool:
        for letter in string:
            if letter in alphabet or letter == '.':
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
                if item in self.operands:
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
        print(calculator.fill_values(Calculator.format_to_infix(command)))
