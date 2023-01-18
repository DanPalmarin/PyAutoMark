while 1:
    try:
        nums = [int(x) for x in input("help: ").split(", ")]
        god = list(filter(lambda x : x % 2 == 0, nums))
        damn = list(filter(lambda x : x % 2 != 0, nums))
        god = [str(x) for x in god]
        damn = [str(x) for x in damn]
        god = ", ".join(god)
        damn = ", ".join(damn)
        print("Even: " + god)
        print("Odd: " + damn)
        break
    except:
        print("Invalid input.")