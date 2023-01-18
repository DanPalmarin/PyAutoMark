while 1:
    try:
        nums = [int(x) for x in input("Nums please and thank you: ").split(" ")]
        break
    except:
        print("Invalid input.")
bignum, lilnum = nums.index(max(nums)), nums.index(min(nums))
nums[bignum], nums[lilnum] = nums[lilnum], nums[bignum]
print(*nums)