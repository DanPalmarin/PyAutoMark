while 1:
    try:
        balls = input("here: ")
        ballsBALLS = lambda x : not x.islower() and not x.isupper() and len(x) >= 6
        if ballsBALLS(balls) == True:
            print("Valid string.")
            break
        else:
            raise Exception("balls")
    except:
        print("Invalid input.")