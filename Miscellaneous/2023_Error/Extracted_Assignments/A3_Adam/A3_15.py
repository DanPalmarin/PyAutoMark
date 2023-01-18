while 1 :
    try:
        balls = {x.lower() for x in input("yup:").split(", ")}
        print(balls)
        break
    except:
        print("Invalid input.")
    
tups = list(map(lambda x : (x.upper()[1: -1], x.lower()[1: -1]), balls))
print(tups)