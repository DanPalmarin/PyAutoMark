def cnvrt(yurt):
    if "." in yurt:
        try:
            yurt = float(yurt)
            return yurt
        except:
            pass

while 1:
    try:
        balls = [x for x in input("ayyy: ").split(", ")]
        balls = list(filter(lambda x : cnvrt(x), balls))
        print(f"Number of floats: {len(balls)}")
        break
    except:
        print("Invalid input.")
