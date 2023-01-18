while 1:
    try:
        marks = [int(x) for x in input("marks:").split(" ")]
        break
    except:
        print("Invalid Input.")
courses = input("courses:").split(" ")
maker = lambda key, value : [(key[x], value[x]) for x in range(len(key))]
transcript = maker(courses, marks)
transcript.sort(key = lambda x : x[1])
print(transcript)
