inputs = input().split(", ")
fs = 0
for x in inputs:
    try:
        float(x)
        try:
            int(x)
        except:
            fs += 1
    except:
        continue

print(f"Number of floats: {fs}")