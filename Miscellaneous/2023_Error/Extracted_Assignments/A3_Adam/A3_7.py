while 1:
    try:
        nums = [int(x) for x in input("Hey: ").split(" ")]
        nums2 = [int(x) for x in input("Hey: ").split(" ")]
        break
    except:
        print("Invalid input.")

print(list(*map(lambda x, y : x + y, nums, nums2)))