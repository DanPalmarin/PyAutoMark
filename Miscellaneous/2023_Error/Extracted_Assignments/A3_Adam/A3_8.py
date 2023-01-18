while 1:
    try:
        balls = input("ayyyyy: ")
        split = lambda x : [x.split(" ")[0].split("-"), x.split(" ")[1]]
        print(split(balls)[0][0])
        print(split(balls)[0][1])
        print(split(balls)[0][2])
        print(split(balls)[1])
        break
    except:
        print("Invalid input.")