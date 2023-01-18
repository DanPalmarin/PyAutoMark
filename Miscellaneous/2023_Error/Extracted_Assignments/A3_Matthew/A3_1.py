while True:
    try:
        ints = input()
        print("List:", [int(x) for x in ints.split(", ")])
        print("Tuple:", tuple(int(x) for x in ints.split(", ")))
        print("Set:", {int(x) for x in ints.split(", ")})
        break
    except:
        print("Invalid input.")