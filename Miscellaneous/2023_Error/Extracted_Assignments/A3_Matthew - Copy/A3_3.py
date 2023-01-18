try:
    ints = [int(x) for x in input().split(", ")]
    names = input().split(", ")
    if(len(names) != len(ints)):
        raise Exception
    pair = lambda x , y: (x,y)
    grades = [pair(n, i) for i, n in zip(ints,names)]
    print(grades)
    print(sorted(grades, key = lambda x : x[1]))
except:
    print("Invalid input.")