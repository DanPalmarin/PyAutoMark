try:
    ints = [int(x) for x in input().split(" ")]
    maxindex = ints.index(max(ints))
    minindex = ints.index(min(ints))
    ints[maxindex], ints[minindex] = min(ints), max(ints)
    print(*ints)
except:
    print("Invalid input.")