import emoji

def main():
    Input = input("Input: ")
    print("Output: ",emoji.emojize(Input, language="alias"))

main()