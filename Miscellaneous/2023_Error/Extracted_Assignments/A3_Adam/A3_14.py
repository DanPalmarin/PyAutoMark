colours = [( 'red', 'pink'), ('white', 'black'), ('orange', 'green')]
names = [( 'Sheridan','Gentry'), ('Laila','Mckee'), ('Ahsan','Rivas')]

colours = list(map(lambda x : f"{x[0]} {x[1]}", colours))
names = list(map(lambda x : f"{x[0]} {x[1]}", names))

print(colours)
print(names)