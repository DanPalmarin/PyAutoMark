lets = [x.replace("'","") for x in input().split(", ")]

lets = sorted(list(set(map(lambda x: (x.upper(), x.lower()), lets))))

print(lets)