while 1:
    try:
        numbers = [int(x) for x in input("Numbers: ").split(" ")]
        names = input("Names:").split(" ")
        print(numbers)
        print(tuple(int(x) for x in numbers))
        print({int(x) for x in numbers})
        print({names[k]:numbers[k] for k in range(len(names))})
        break
    except:
        print("Invalid input.")

##NEEDS FIXING LMAOOOOOOOO
