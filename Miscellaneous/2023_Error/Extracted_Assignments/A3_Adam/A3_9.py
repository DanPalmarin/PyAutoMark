while 1:
    try:
        balls = [x for x in input("ayyy: ").split(", ")]
        print("Palindromes: " + ", ".join(list(filter(lambda x : x == x[::-1], balls))))
        break
    except:
        print("Invalid input.")