while True:
    try:
        ints = [int(x) for x in input().split(", ")]
        
        break
    except:
        print("Invalid input.")
while True:
    try:
        names = input().split(", ")
        if(len(names) != len(ints)):
            raise Exception
        print("List:", ints)
        print("Tuple:", tuple(ints))
        print("Set:", set(ints))
        print("Dictionary:", {names[x]:ints[x] for x in range(len(ints))})
        break
    except:
        print("Invalid input.")