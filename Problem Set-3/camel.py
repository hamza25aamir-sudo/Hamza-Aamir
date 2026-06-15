def main():
    camel_case = input("camelCase: ")
    print("snake_case: ", end="")
    
    for char in camel_case:
        if char.isupper():
            print("_" + char.lower(), end="")
        else:
            print(char, end="")
            
    print()

main()