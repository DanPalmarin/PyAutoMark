while True:
    try:
        date = input()
        day = date.split(" ")[0].split("-")
        time = date.split(" ")[1]
        year = int(day[0])
        month = int(day[1])
        day = int(day[2])
        print(year)
        print(month)
        print(day)
        print(time)
        break
    except:
        print("Invalid input.")