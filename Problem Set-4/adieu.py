names = []
 
while True:
    try:
        name = input("Name: ")
        names.append(name)
    except EOFError:
        break
 
if len(names) == 1:
    farewell = names[0]
elif len(names) == 2:
    farewell = f"{names[0]} and {names[1]}"
else:
    farewell = ", ".join(names[:-1]) + f", and {names[-1]}"
 
print(f"Adieu, adieu, to {farewell}")
