try:
    ints = [int(x) for x in input().split(", ")]
    neg = list(filter(lambda x : x < 0, ints))
    pos = list(filter(lambda x : x > 0, ints))
    print(f"Sum of the negative numbers: {sum(neg)}")
    print(f"Sum of the positive numbers: {sum(pos)}")
except:
    print("Invalid input.")