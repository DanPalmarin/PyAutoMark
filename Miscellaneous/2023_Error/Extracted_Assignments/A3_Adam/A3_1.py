while 1:
    try:
        numbers = [int(x) for x in input("Numbers: ").split(" ")]
        print(numbers)
        print(tuple(int(x) for x in numbers))
        print({int(x) for x in numbers})
        break
    except:
        print("Invalid input.")