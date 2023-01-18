while True:
    try:
        ints = [int(x) for x in input().split(", ")]
        ints = list(map(lambda x : x*3, ints))
        break
    except:
        print("Invalid input.")
print(ints)