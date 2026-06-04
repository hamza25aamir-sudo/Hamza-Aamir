def einstein(num1):
    c = 300000000
    return num1 * (c ** 2)
def main():
    num1 = int(input("m: "))
    e = einstein(num1)
    print(f"E: {e}")
main()