while True:
    try:
        ints1 = [int(x) for x in input().split(" ")]
        break
    except:
        print("Invalid input.")

while True:
    try:
        ints2 = [int(x) for x in input().split(" ")]
        break
    except:
        print("Invalid input.")
print(*map(lambda x , y: x + y ,ints1, ints2))