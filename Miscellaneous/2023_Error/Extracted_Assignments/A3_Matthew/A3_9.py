while True:
    try:
        i = input()
        if ("," not in i):
            raise Exception
        inputs = i.split(", ")
        break
    except:
        print("Invalid input.")

print("Palindromes: ",", ".join(list(filter(lambda x : x == x[::-1], inputs))))