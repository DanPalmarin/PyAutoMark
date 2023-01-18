while True:
    try:
        ints = [int(x) for x in input().split(", ")]
        break
    except:
        print("Invalid input.")
print("Even: ", ", ".join([str(x) for x in list(filter(lambda x : x % 2 == 0, ints))]))
print("Odd: ", ", ".join([str(x) for x in list(filter(lambda x : x % 2 == 1, ints))]))