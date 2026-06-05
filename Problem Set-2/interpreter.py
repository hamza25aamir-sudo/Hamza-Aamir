def split():
    expression = input("Expression: ").strip()
    x, y, z = expression.split(" ")
    x = int(x)
    z = int(z)

    return x, y, z

def main():

    x, y, z = split()

    if y == "+":
        result = x + z
    elif y == "-":
        result = x - z
    elif y == "*":
        result = x * z
    elif y == "/":
        result = x / z
        
    print(f"{result:.1f}")

main()