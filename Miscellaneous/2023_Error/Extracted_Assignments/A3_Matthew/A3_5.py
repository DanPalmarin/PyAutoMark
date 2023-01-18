specs = {'Matthew Vega': (6.2, 70),'Alden Cantrell': (5.9,65),'Corden Gentry': (6.0, 68),'Pierre Cox': (5.8, 66)}

filteredKeys = list(filter(lambda x: specs[x][0] >= 6 and specs[x][1] >= 70, specs))

print({x:specs[x] for x in filteredKeys})
