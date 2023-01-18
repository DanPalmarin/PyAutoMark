while 1:
    try:
        balls = [int(x) for x in input("ayyy: ").split(", ")]
        print(f"Sum of the positive numbers: {sum(list(filter(lambda x : x >= 0 , balls)))}")
        print(f"Sum of the negative numbers: {sum(list(filter(lambda x : x < 0 , balls)))}")
        break
    except:
        print("Invalid input.")