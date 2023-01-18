while 1:
    try:
        balls = [int(x) for x in input("nums:").split(", ")]
        break
    except:
        print("Invalid input.")

trips = list(map(lambda x : x * 3, balls))
print(trips)