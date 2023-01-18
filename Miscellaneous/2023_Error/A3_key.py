

assignment_num = 3

Q1 = {
    ("sam, jacob, Marley","3, 5, 7, 23") : ("Invalid input.","[3, 5, 7, 23]","(3, 5, 7, 23)","{"),
    ("Frodo, Sam, Pippin, Merry","87, 71, 99, 7") : ("Invalid input.","[87, 71, 99, 7]","(87, 71, 99, 7)","{")
}

##Q1 = {
##    ("sam, jacob, Marley","3, 5, 7, 23") : ("Invalid input.","[3, 5, 7, 23]","(3, 5, 7, 23)","{3, 23, 5, 7}"),
##    ("Frodo, Sam, Pippin, Merry","87, 71, 99, 7") : ("Invalid input.","[87, 71, 99, 7]","(87, 71, 99, 7)","{99, 7, 71, 87}")
##}

Q2 = {
    ("thirteen, eleventy -one, four, seven", "13, 111 , 4, 7","Frodo, Sam, Pippin, Merry") :
    ("Invalid input.","[13, 111, 4, 7]","(13, 111, 4, 7)","{","{'Frodo': 13, 'Sam': 111, 'Pippin': 4, 'Merry': 7}"),
    ("-55, 107, -5, 44","Aragorn, Strider, Ellesar, King") :
    ("[-55, 107, -5, 44]","(-55, 107, -5, 44)","{","{'Aragorn': -55, 'Strider': 107, 'Ellesar': -5, 'King': 44}"),
    ("3, 5, 7, 23","Frodo Sam Pippin Merry","Frodo, Sam, Pippin, Merry") :
    ("Invalid input.","[3, 5, 7, 23]","(3, 5, 7, 23)","{","{'Frodo': 3, 'Sam': 5, 'Pippin': 7, 'Merry': 23}")
}

##Q2 = {
##    ("thirteen, eleventy -one, four, seven", "13, 111 , 4, 7","Frodo, Sam, Pippin, Merry") :
##    ("Invalid input.","[13, 111, 4, 7]","(13, 111, 4, 7)","{7, 4, 13, 111}","{'Frodo': 13, 'Sam': 111, 'Pippin': 4, 'Merry': 7}"),
##    ("-55, 107, -5, 44","Aragorn, Strider, Ellesar, King") :
##    ("[-55, 107, -5, 44]","(-55, 107, -5, 44)","{-55, 107, 44, -5}","{'Aragorn': -55, 'Strider': 107, 'Ellesar': -5, 'King': 44}"),
##    ("3, 5, 7, 23","Frodo Sam Pippin Merry","Frodo, Sam, Pippin, Merry") :
##    ("Invalid input.","[3, 5, 7, 23]","(3, 5, 7, 23)","{3, 5, 7, 23}","{'Frodo': 3, 'Sam': 5, 'Pippin': 7, 'Merry': 23}")
##}

Q3 = {
    "88 90 46 22" : "Invalid input.",
    ("88, 90, 97, 82","English Math Computer Science History") : "Invalid input.",
    ("88, 90, 97, 82","English, Math, Computer Science, History") :
    ("[('English', 88), ('Math', 90), ('Computer Science', 97), ('History', 82)]","[('History', 82), ('English', 88), ('Math', 90), ('Computer Science', 97)]"),
    ("55, 62, 98, 70","Calculus, Chemistry, Photography, Biology") :
    ("[('Calculus', 55), ('Chemistry', 62), ('Photography', 98), ('Biology', 70)]","[('Calculus', 55), ('Chemistry', 62), ('Biology', 70), ('Photography', 98)]")
}

Q4 = {
    "3, 4, five, 2, one" : "Invalid input.",
    "3 4 5 2 1" : "3 4 1 2 5",
    "4 5 33 4 5 6 2 34" : "4 5 33 4 5 6 34 2"
}

Q5 = "{'Matthew Vega': (6.2, 70)}"

Q6 = {
    ("uno, due, tre, quattro, cinque, sei, sette", "1, 2, 3, 4, 5, 6, 7, 8, 9, 10") : ("Invalid input.","2, 4, 6, 8, 10","1, 3, 5, 7, 9"),
    ("2 4 1 5525 4352 3 22 3 17","2, 4, 1, 5525, 4352, 3, 22, 3, 17") : ("Invalid input.","2, 4, 4352, 22","1, 5525, 3, 3, 17")
}

Q7 = {
    ("I am the Senate.","1 2 3","Execute order 66.","4 5 6") : ("Invalid input.","Invalid input.","5 7 9"),
    ("1 99 -5","-105 33 0") : "-104 132 -5"
}

Q8 = {
    ("09:03:32 2022-02-22","2022 -02 -22 09:03:32","2022-02-22 09:03:32") : ("Invalid input.","Invalid input.","2022\n2\n22\n09:03:32"),
    "2022-03-19 15:50:23" : "2022\n3\n19\n15:50:23"
}

Q9 = {
    ("php w3r Python abcd Java aaa","php, w3r, Python, abcd, Java, aaa") : ("Invalid input.","php, aaa"),
    "Frodo, Sam, Pippin, SaS, Gollum" : "SaS"
}

Q10 = {
    "two, four, seven" : "Invalid input.",
    "2, 4, -6, -9, 11, -12, 14, -5, 17" : (-32,48),
    "-55, 0, 105, 27" : (-55,132)
}

Q11 = {
    "1, 'abcd ', 3.12 , 1.2 , 4, 'xyz ', 5, 'pqr ', 7, -5, -12.22" : 3,
    "55, 107.5, -55.4, 'Dan'" : 2
}

Q12 = {
    ("Wc3","wc3forlife","Wc3forlife") : ("Invalid input.","Invalid input.","Valid string."),
    ("Sauron","SauronTheCursed1") : ("Invalid input.","Valid string.")
}

Q13 = {
    "1, 2, 3, 4, 5, 6, 7" : "[3, 6, 9, 12, 15, 18, 21]",
    ("99, 35, 5 33","42, -53") : ("Invalid input.","[126, -159]")
}

Q14 = "['red pink', 'white black', 'orange green']\n['Sheridan Gentry', 'Laila Mckee', 'Ahsan Rivas']"

Q15 = {
    "'f', 'b', 'U', 'i', 'E', 'a', 'B', 'u'" : "[('A', 'a'), ('B', 'b'), ('E', 'e'), ('F', 'f'), ('I', 'i'), ('U', 'u')]",
    "'a', 'F', 'Z', 'z'" : "[('A', 'a'), ('F', 'f'), ('Z', 'z')]"
}
Q_weight = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
Q_flexible = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
#Q_all = [Q1,Q2,Q3,Q4,Q5,Q6,Q7,Q8,Q9,Q10,Q11,Q12,Q13,Q14,Q15]

##Q_weight = [1,1,1,1,1,1,1,1,1,1,1,1,1,1]
##Q_flexible = [1,2,3,4,5,6,7,8,9,10,11,12,13,14]
Q_all = [Q1,Q2]















