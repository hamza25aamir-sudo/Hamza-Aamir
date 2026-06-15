def main():
    user_input = input("Input: ")
    vowels = "aeiouAEIOU"
    print("Output: ", end="")
    for letter in user_input:
        if letter not in vowels:
            print(letter, end="")
    print()
main()