# write your code here
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
        words = command.split()
        if len(words) > 0:
            numbers = [int(word) for word in words]
            print(sum(numbers))
        else:
            print(words[0])
